import os
import base64

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from scholar_parser import parse_scholar_articles, deduplicate_articles
from aael_ranker import score_article
from sitrep_writer import write_outputs

# Full Gmail scope is required for permanent delete
SCOPES = ["https://mail.google.com/"]


def gmail_authenticate():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception:
            creds = None

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)

        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service


def get_scholar_messages(service, page_size=100):
    query = 'from:scholaralerts-noreply@google.com'

    all_messages = []
    page_token = None

    while True:
        request = (
            service.users()
            .messages()
            .list(
                userId="me",
                q=query,
                maxResults=page_size,
                pageToken=page_token
            )
        )

        results = request.execute()
        messages = results.get("messages", [])
        all_messages.extend(messages)

        page_token = results.get("nextPageToken")
        if not page_token:
            break

    return all_messages


def _decode_body_data(data):
    try:
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    except Exception:
        return ""


def extract_message_bodies(service, msg_id):
    message = (
        service.users()
        .messages()
        .get(userId="me", id=msg_id, format="full")
        .execute()
    )

    payload = message.get("payload", {})
    html_body = ""
    text_body = ""

    def walk_parts(part):
        nonlocal html_body, text_body

        mime_type = part.get("mimeType", "")
        body = part.get("body", {})
        data = body.get("data")

        if mime_type == "text/html" and data and not html_body:
            html_body = _decode_body_data(data)

        elif mime_type == "text/plain" and data and not text_body:
            text_body = _decode_body_data(data)

        for child in part.get("parts", []):
            walk_parts(child)

    walk_parts(payload)

    if not html_body and payload.get("body", {}).get("data"):
        html_body = _decode_body_data(payload["body"]["data"])

    return html_body, text_body


def delete_messages(service, msg_ids):
    """
    Permanently delete processed Scholar alert emails.
    """
    for msg_id in msg_ids:
        (
            service.users()
            .messages()
            .delete(userId="me", id=msg_id)
            .execute()
        )


def main():
    print("\nAAEL Scholar Agent starting...\n")

    service = gmail_authenticate()
    print("Connected to Gmail.")

    messages = get_scholar_messages(service, page_size=100)
    print(f"Found {len(messages)} Scholar alert emails.\n")

    if not messages:
        print("No Scholar emails found.")
        return

    all_articles = []
    processed_msg_ids = []

    for idx, msg in enumerate(messages, start=1):
        msg_id = msg["id"]

        try:
            print(f"Processing email {idx} of {len(messages)}...")
            html_body, text_body = extract_message_bodies(service, msg_id)

            articles = parse_scholar_articles(html_body, text_body)

            for article in articles:
                score, reason, core_aael = score_article(article)
                article["score"] = score
                article["reason"] = reason
                article["core_aael"] = core_aael

            all_articles.extend(articles)
            processed_msg_ids.append(msg_id)

        except Exception as exc:
            print(f"Failed to process message {msg_id}: {exc}")

    deduped_articles = deduplicate_articles(all_articles)

    print(f"\nRaw extracted articles: {len(all_articles)}")
    print(f"After deduplication: {len(deduped_articles)}\n")

    if not deduped_articles:
        print("No articles extracted.")
        return

    try:
        output_paths = write_outputs(deduped_articles)

        print("Outputs created:")
        for path in output_paths:
            print(path)

        delete_messages(service, processed_msg_ids)
        print("\nProcessed Scholar alert emails were deleted.")

    except Exception as exc:
        print(f"\nOutput step failed.\nError: {exc}")


if __name__ == "__main__":
    main()
