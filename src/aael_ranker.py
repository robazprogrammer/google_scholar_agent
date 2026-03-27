POSITIVE_KEYWORDS = {
    "adaptive learning": 14,
    "personalized learning": 10,
    "ai in education": 18,
    "artificial intelligence in education": 18,
    "generative ai": 8,
    "learning analytics": 12,
    "metacognition": 22,
    "self-regulated learning": 20,
    "self regulated learning": 20,
    "exploratory learning": 24,
    "human-ai": 14,
    "human ai": 14,
    "intelligent tutoring system": 8,
    "student engagement": 6,
    "instructional design": 8,
    "educational technology": 8,
    "edtech": 8,
    "reading comprehension": 8,
    "teacher education": 6,
    "inclusive learning": 8,
    "accessible learning": 8,
    "neurodiverse": 18,
    "neurodiversity": 18,
    "dyslexic": 16,
    "dyslexia": 16,
    "autism": 22,
    "autistic": 22,
    "special education": 18,
    "assistive technology": 8,
    "adaptive feedback": 8,
    "personalized feedback": 8,
    "ai-assisted learning": 14,
    "ai assisted learning": 14,
    "ai-powered learning": 10,
    "ai powered learning": 10,
    "student learning": 4,
    "higher education": 4,
    "mathematics education": 6,
    "adult learning": 6,
    "lifelong learning": 4,
}

NEGATIVE_KEYWORDS = {
    "policy": -10,
    "legal framework": -14,
    "fundamental rights": -12,
    "ethics": -8,
    "institutional transformation": -8,
    "iot": -30,
    "industrial": -20,
    "manufacturing": -20,
    "intrusion detection": -35,
    "cybersecurity": -15,
    "network traffic": -18,
    "smart grid": -20,
    "wireless sensor": -20,
    "predictive maintenance": -25,
    "air quality": -20,
    "fault diagnosis": -20,
    "robot arm": -20,
    "supply chain": -15,
    "agriculture": -15,
    "medical imaging": -15,
    "vehicle": -12,
    "power system": -15,
    "blockchain": -12,
    "cloud computing": -12,
    "energy consumption": -15,
}

STRONG_COMBINATIONS = [
    ("ai", "education", 8),
    ("generative ai", "learning", 6),
    ("adaptive", "learning", 8),
    ("student", "metacognition", 16),
    ("learning analytics", "student", 6),
    ("ai", "reading comprehension", 8),
    ("neurodiverse", "learning", 14),
    ("autism", "learning", 16),
    ("special education", "ai", 16),
    ("self-regulated learning", "adaptive learning", 14),
    ("exploratory", "learning", 16),
]

CORE_AAEL_TERMS = {
    "metacognition",
    "self-regulated learning",
    "self regulated learning",
    "exploratory learning",
    "human-ai",
    "human ai",
    "ai assisted learning",
    "ai-assisted learning",
    "autism",
    "autistic",
    "dyslexia",
    "dyslexic",
    "neurodiverse",
    "neurodiversity",
    "special education",
}

REQUIRES_LEARNING_CONTEXT = {
    "adaptive learning",
    "personalized learning",
    "learning analytics",
}


def _normalize_text(article):
    title = article.get("title", "") or ""
    summary = article.get("summary", "") or ""
    return f"{title} {summary}".lower()


def score_article(article):
    text = _normalize_text(article)
    score = 0
    reasons = []
    matched_positive_roots = set()

    for phrase, weight in POSITIVE_KEYWORDS.items():
        if phrase in text:
            root = phrase.replace(" systems", "").replace(" system", "")
            if root not in matched_positive_roots:
                score += weight
                reasons.append(f"+ {phrase}")
                matched_positive_roots.add(root)

    for phrase, weight in NEGATIVE_KEYWORDS.items():
        if phrase in text:
            score += weight
            reasons.append(f"- {phrase}")

    for word_a, word_b, bonus in STRONG_COMBINATIONS:
        if word_a in text and word_b in text:
            score += bonus
            reasons.append(f"+ combo: {word_a} & {word_b}")

    core_hits = [term for term in CORE_AAEL_TERMS if term in text]

    # Stricter core logic:
    # core if it contains a direct AAEL term OR if adaptive/personalized/analytics appears
    # together with explicit educational context
    has_learning_context = any(term in text for term in ["student", "learning", "education", "teaching", "instruction"])
    contextual_hits = [term for term in REQUIRES_LEARNING_CONTEXT if term in text]

    core_aael = bool(core_hits) or (len(contextual_hits) >= 2 and has_learning_context)

    if core_hits:
        bonus = min(16, 4 + (len(core_hits) * 2))
        score += bonus
        reasons.append(f"+ core AAEL terms: {', '.join(core_hits[:4])}")

    if "systematic review" in text or "meta-analysis" in text or "meta analysis" in text:
        score += 5
        reasons.append("+ review/synthesis")

    if "teacher" in text and "student" in text:
        score += 3
        reasons.append("+ teacher/student context")

    score = max(0, min(100, score))

    if score >= 82:
        label = "Strong AAEL fit"
    elif score >= 60:
        label = "Possible AAEL fit"
    elif score >= 35:
        label = "Weak AAEL fit"
    else:
        label = "Low AAEL fit"

    if core_aael and 45 <= score < 60:
        label = "Core AAEL candidate"

    reason_text = label
    if reasons:
        reason_text += " | " + "; ".join(reasons[:6])

    return score, reason_text, core_aael
