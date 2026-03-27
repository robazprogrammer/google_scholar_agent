import re
from bs4 import BeautifulSoup


LEADING_NOISE_PATTERNS = [
    r"^\[(?:HTML|PDF)\]\s*",
    r"^(?:\.\.\.|…)+\s*",
    r"^[\-\–\—\:;,)\]\s]+",
]


def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_title(title):
    if not title:
        return ""

    title = clean_text(title)

    for pattern in LEADING_NOISE_PATTERNS:
        title = re.sub(pattern, "", title, flags=re.IGNORECASE)

    # Remove repeated leading fragments like "... for the ..."
    title = re.sub(r"^(?:for the|of the|in the)\s+", "", title, flags=re.IGNORECASE) if title.startswith("…") else title

    # Remove residual leading ellipsis fragments again after cleanup
    title = re.sub(r"^(?:\.\.\.|…)+\s*", "", title)

    # Remove trailing punctuation noise
    title = re.sub(r"[\s\.,;:]+$", "", title)

    return title.strip()


def normalize_title(title):
    title = clean_title(title).lower()
    title = re.sub(r"[^a-z0-9\s]", "", title)
    title = re.sub(r"\s+", " ", title)
    return title.strip()


def extract_google_redirect_url(url):
    return clean_text(url)


def is_probable_title(title):
    if not title:
        return False

    title = clean_title(title)

    if len(title) < 30:
        return False

    lowered = title.lower()

    bad_exact = {
        "my alerts",
        "get alerts",
        "view all",
        "google scholar",
        "scholar articles",
        "related articles",
        "new articles",
        "email settings",
        "cancel alert",
    }

    if lowered in bad_exact:
        return False

    if lowered.startswith("http"):
        return False

    return True


def parse_from_html(html):
    articles = []

    if not html:
        return articles

    soup = BeautifulSoup(html, "html.parser")
    seen_local = set()

    for link in soup.find_all("a", href=True):
        raw_title = link.get_text(" ", strip=True)
        title = clean_title(raw_title)
        url = extract_google_redirect_url(link["href"])

        if not is_probable_title(title):
            continue

        if "scholar.google" in url.lower() and len(title) < 45:
            continue

        key = (normalize_title(title), url)
        if key in seen_local:
            continue
        seen_local.add(key)

        snippet_parts = []
        parent = link.parent

        if parent:
            parent_text = clean_text(parent.get_text(" ", strip=True))
            parent_text = parent_text.replace(raw_title, "").strip()
            parent_text = clean_text(parent_text)

            if parent_text and parent_text != title:
                snippet_parts.append(parent_text)

            next_el = parent.find_next_sibling()
            hop_count = 0

            while next_el and hop_count < 2:
                sibling_text = clean_text(next_el.get_text(" ", strip=True))
                if sibling_text:
                    snippet_parts.append(sibling_text)
                next_el = next_el.find_next_sibling()
                hop_count += 1

        summary = clean_text(" ".join(snippet_parts))
        summary = re.sub(r"^\[(?:HTML|PDF)\]\s*", "", summary, flags=re.IGNORECASE)
        if summary == title:
            summary = ""

        articles.append(
            {
                "title": title,
                "url": url,
                "summary": summary,
            }
        )

    return articles


def parse_from_text(text):
    articles = []

    if not text:
        return articles

    lines = [clean_text(line) for line in text.splitlines()]
    lines = [line for line in lines if line]

    url_pattern = re.compile(r"https?://\S+")
    seen_local = set()

    for i, line in enumerate(lines):
        line = clean_title(line)

        if not is_probable_title(line):
            continue

        urls = url_pattern.findall(line)
        if urls:
            title_candidate = re.sub(url_pattern, "", line).strip(" -:•")
            title_candidate = clean_title(title_candidate)

            if is_probable_title(title_candidate):
                key = (normalize_title(title_candidate), urls[0])
                if key not in seen_local:
                    seen_local.add(key)
                    articles.append(
                        {
                            "title": title_candidate,
                            "url": urls[0],
                            "summary": "",
                        }
                    )
            continue

        if i + 1 < len(lines) and url_pattern.search(lines[i + 1]):
            url = url_pattern.search(lines[i + 1]).group(0)
            key = (normalize_title(line), url)

            if key not in seen_local:
                seen_local.add(key)
                articles.append(
                    {
                        "title": line,
                        "url": url,
                        "summary": "",
                    }
                )

    return articles


def parse_scholar_articles(html_body, text_body=""):
    html_articles = parse_from_html(html_body)
    text_articles = parse_from_text(text_body)
    return deduplicate_articles(html_articles + text_articles)


def deduplicate_articles(articles):
    by_title = {}

    for article in articles:
        title = clean_title(article.get("title", ""))
        url = clean_text(article.get("url", ""))
        summary = clean_text(article.get("summary", ""))

        if not title or len(title) < 10:
            continue

        norm_title = normalize_title(title)
        if not norm_title:
            continue

        article_clean = {
            "title": title,
            "url": url,
            "summary": summary,
            "score": article.get("score", 0),
            "reason": article.get("reason", ""),
            "core_aael": article.get("core_aael", False),
        }

        if norm_title not in by_title:
            by_title[norm_title] = article_clean
        else:
            existing = by_title[norm_title]

            better_summary = len(summary) > len(existing.get("summary", ""))
            better_score = article_clean.get("score", 0) > existing.get("score", 0)
            better_core = article_clean.get("core_aael", False) and not existing.get("core_aael", False)

            if better_summary or better_score or better_core:
                if not article_clean["url"]:
                    article_clean["url"] = existing.get("url", "")
                if not article_clean["summary"]:
                    article_clean["summary"] = existing.get("summary", "")
                if not article_clean["reason"]:
                    article_clean["reason"] = existing.get("reason", "")
                by_title[norm_title] = article_clean

    deduped = list(by_title.values())
    deduped.sort(
        key=lambda x: (
            x.get("core_aael", False),
            x.get("score", 0),
            len(x.get("summary", "")),
            x.get("title", "").lower(),
        ),
        reverse=True,
    )
    return deduped
