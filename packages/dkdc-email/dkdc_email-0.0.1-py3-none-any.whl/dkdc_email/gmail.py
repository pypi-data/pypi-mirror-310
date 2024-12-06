# imports
import os
import json
import base64

from rich import print

from dateutil import parser
from datetime import datetime

from email.header import decode_header
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from dkdc_util import get_dkdc_dir


def _get_flow() -> InstalledAppFlow:
    creds_path = os.path.join(get_dkdc_dir(), "app.json")

    # Initialize the flow with client secrets and required scopes
    flow = InstalledAppFlow.from_client_secrets_file(
        creds_path,
        scopes=[
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/calendar.events",
        ],
        redirect_uri="urn:ietf:wg:oauth:2.0:oob",  # Use out-of-band (OOB) for manual URL
    )
    # creds = flow.run_local_server(access_type="offline", port=8099)

    return flow


def get_auth_url() -> str:
    flow = _get_flow()

    # Generate the authorization URL
    auth_url, _ = flow.authorization_url(prompt="consent")

    return auth_url


def creds_from_code(code: str) -> Credentials:
    flow = _get_flow()
    flow.fetch_token(code=code)
    return flow.credentials


def creds_from_bytes(data: bytes) -> Credentials:
    json_data = json.loads(data.decode())
    creds = Credentials.from_authorized_user_info(json_data)
    return creds


def update_creds(creds: Credentials) -> Credentials:
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return creds


def email_id_from_creds(creds: Credentials) -> str:
    """Get user email id from the credentials."""
    try:
        service = build("gmail", "v1", credentials=creds)
        profile = service.users().getProfile(userId="me").execute()

        return profile["emailAddress"]

    except HttpError as error:
        print(f"An error occurred: {error}")


def ingest_inbox(creds: Credentials) -> list[dict]:
    """Ingest inbox."""

    to_return = []

    def decode_mime_words(s):
        """Decodes a string that may contain MIME-encoded words."""
        if not s:
            return ""
        decoded_strings = []
        for encoded_word, encoding in decode_header(s):
            if isinstance(encoded_word, bytes):
                decoded_strings.append(
                    encoded_word.decode(encoding or "utf-8", errors="replace")
                )
            else:
                decoded_strings.append(encoded_word)
        return "".join(decoded_strings)

    creds = update_creds(creds)

    try:
        service = build("gmail", "v1", credentials=creds)

        # Fetch messages from the inbox
        results = (
            service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()
        )
        messages = results.get("messages", [])

        for message in messages:
            msg_id = message["id"]
            print(f"Processing email {msg_id}...")

            msg = (
                service.users()
                .messages()
                .get(userId="me", id=msg_id, format="full")
                .execute()
            )

            # Extract headers
            headers = msg["payload"]["headers"]
            headers_dict = {
                header["name"].lower(): header["value"] for header in headers
            }

            # Decode headers
            subject = decode_mime_words(headers_dict.get("subject", "[No Subject]"))
            from_ = decode_mime_words(headers_dict.get("from", "[Unknown Sender]"))
            to = decode_mime_words(
                headers_dict.get("to")
                or headers_dict.get("delivered-to")
                or "[No Recipient]"
            )
            sent_at = headers_dict.get("date", "")
            thread_id = msg.get("threadId", "")

            # Parse 'Date' into ISO format
            if sent_at:
                sent_at_parsed = parser.parse(sent_at).isoformat()
            else:
                sent_at_parsed = datetime.now().isoformat()
                print(
                    f"Email {msg_id} is missing a Date header. Using current timestamp."
                )

            # Initialize variables
            body_plain = ""
            body_html = ""
            attachments = []

            # Function to parse email parts
            def parse_parts(parts):
                nonlocal body_plain, body_html, attachments
                for part in parts:
                    mime_type = part.get("mimeType", "")
                    filename = part.get("filename", "")
                    body = part.get("body", {})
                    data = body.get("data", "")
                    attachment_id = body.get("attachmentId")

                    if mime_type == "text/plain" and data:
                        decoded_data = base64.urlsafe_b64decode(data).decode(
                            "utf-8", errors="replace"
                        )
                        body_plain += decoded_data
                    elif mime_type == "text/html" and data:
                        decoded_data = base64.urlsafe_b64decode(data).decode(
                            "utf-8", errors="replace"
                        )
                        body_html += decoded_data
                    elif filename and attachment_id:
                        attachment = (
                            service.users()
                            .messages()
                            .attachments()
                            .get(
                                userId="me",
                                messageId=msg_id,
                                id=attachment_id,
                            )
                            .execute()
                        )
                        _file_data = base64.urlsafe_b64decode(
                            attachment.get("data", "")
                        )
                        _content_type = mime_type
                        _size = int(body.get("size", 0))
                        attachments.append(attachment_id)
                    elif "parts" in part:
                        parse_parts(part["parts"])

            # Parse the email parts
            payload = msg["payload"]
            if "parts" in payload:
                parse_parts(payload["parts"])
            else:
                # Single-part email
                data = payload.get("body", {}).get("data", "")
                if data:
                    body_plain = base64.urlsafe_b64decode(data).decode(
                        "utf-8", errors="replace"
                    )

            # convert empty strings to None
            body_plain = body_plain or None
            body_html = body_html or None

            # Append the email to the list
            to_return.append(
                {
                    "id": msg_id,
                    "thread_id": thread_id,
                    "from": from_,
                    "to": to,
                    "subject": subject,
                    "sent_at": sent_at_parsed,
                    "body_plain": body_plain,
                    "body_html": body_html,
                    "attachments": attachments,
                }
            )

        return to_return

    except HttpError as error:
        print(f"An error occurred: {error}")


def send_email(
    creds: Credentials,
    to: str,
    subject: str,
    body: str,
    from_: str = None,
    thread_id: str = None,
    original_message_id: str = None,
    original_message: str = None,
    original_from: str = None,
    original_time: str = None,
    attachments: list = None,  # TODO: add Attachment class
):
    """Sends an email and properly replies to threads, including the original message like a normal email client."""
    try:
        service = build("gmail", "v1", credentials=creds)

        message = MIMEMultipart()
        message["to"] = to
        message["from"] = from_
        message["subject"] = subject

        if thread_id and original_message:
            # Include quoted original message in the body
            # Use the original sender and date if provided
            original_from = original_from or "[sender]"
            original_time = original_time or "[time]"

            # Format the quoted original message
            reply_body = (
                f"\n\nAt {original_time}, {original_from} wrote:\n> "
                + "\n> ".join(original_message.split("\n"))
            )
            body += reply_body

            # If you have the original Message-ID and References, you can set them here
            # message['In-Reply-To'] = original_message_id
            # message['References'] = references

        if original_message_id:
            message["In-Reply-To"] = original_message_id

        # Attach the email body
        message.attach(MIMEText(body, "plain"))

        # Attach files if any
        if attachments:
            for attachment_obj in attachments:
                filename = attachment_obj.filename
                file_data = attachment_obj.data

                attachment_part = MIMEBase("application", "octet-stream")
                attachment_part.set_payload(file_data)
                encoders.encode_base64(attachment_part)
                attachment_part.add_header(
                    "Content-Disposition", f'attachment; filename="{filename}"'
                )
                message.attach(attachment_part)

        # Encode and send the message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": raw_message}

        if thread_id:
            create_message["threadId"] = thread_id

        sent_message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )
        print(f"Message Id: {sent_message['id']} sent successfully.")

    except HttpError as error:
        print(f"An error occurred: {error}")
