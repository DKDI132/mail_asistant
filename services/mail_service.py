import imaplib
import email
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta, timezone


def get_emails_last_90_minutes(email_user, email_pass):
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(email_user, email_pass)
    mail.select("inbox")

    yesterday = (datetime.now(timezone.utc) - timedelta(days=1))
    imap_date_format = yesterday.strftime("%d-%b-%Y")

    status, messages = mail.search(None, f'SINCE "{imap_date_format}"')
    if status != "OK" or not messages[0]:
        print("Brak wiadomości z tego okresu na serwerze.")
        return []
    mail_ids = messages[0].split()


    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=1.5)

    new_emails_to_process = []
    for mail_id in reversed(mail_ids):
        status, data = mail.fetch(mail_id, "(BODY[HEADER.FIELDS (DATE MESSAGE-ID)])")
        if status != "OK":
            continue

        header_text = data[0][1].decode("utf-8", errors="ignore")
        msg = email.message_from_string(header_text)

        date_str = msg.get("Date")
        message_id = msg.get("Message-ID")

        if not date_str:
            continue

        try:
            email_time = parsedate_to_datetime(date_str)
            if email_time.tzinfo is None:
                email_time = email_time.replace(tzinfo=timezone.utc)
            else:
                email_time = email_time.astimezone(timezone.utc)
        except Exception as e:
            print(f"Błąd parsowania daty: {e}")
            continue
        if email_time >= cutoff_time:
            new_emails_to_process.append({
                "imap_id": mail_id,
                "message_id": message_id,
                "time": email_time
            })
        else:
            break

    return new_emails_to_process

def mail_analizer():
    maile = get_emails_last_90_minutes()
    for mail in maile:

