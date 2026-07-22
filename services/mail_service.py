import imaplib
import email
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta, timezone
from repo.email_repository import Email_repo
from entity.email import Email
from services.ai import skrot
from email import policy
from services.notify import send_push_notification

async def get_emails_last_90_minutes(email_user, email_pass, db_repo):
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(email_user, email_pass)
    mail.select("inbox")

    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%d-%b-%Y")
    status, messages = mail.search(None, f'SINCE "{yesterday}"')
    if status != "OK" or not messages[0]:
        return []
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=1.5)
    new_emails = []

    for mail_id in reversed(messages[0].split()):

        _, data = mail.fetch(mail_id, "(BODY[HEADER.FIELDS (DATE MESSAGE-ID)])")
        msg_header = email.message_from_bytes(data[0][1])

        date_str = msg_header.get("Date")
        message_id = msg_header.get("Message-ID")
        if not date_str or not message_id:
            continue

        email_time = parsedate_to_datetime(date_str).astimezone(timezone.utc)
        if email_time < cutoff_time:
            break

        if db_repo.get_by_id(message_id):
            continue

        _, full_data = mail.fetch(mail_id, "(RFC822)")
        msg = email.message_from_bytes(full_data[0][1], policy=policy.default)

        sender = str(msg.get("From", ""))
        subject = str(msg.get("Subject", ""))


        body_part = msg.get_body(preferencetype='plain')
        body = body_part.get_content() if body_part else ""
        new_emails.append({
            "message_id": message_id,
            "sender": sender,
            "subject": subject,
            "body": body,
            "date": date_str
        })
    mail.logout()
    return new_emails

async def mail_analizer(db_repo,user,passw,ntfy_key):
    maile = await get_emails_last_90_minutes(user,passw,db_repo)
    for mail in maile:
        analize = await skrot(f"subject: {mail['subject']} \n body: {mail['body']}")
        nowy = Email(id = mail["message_id"],sender=mail["sender"],subject=mail["subject"],body=mail["body"],snippet=analize["summary"],date=mail["date"],is_important=analize["importance"])
        db_repo.create(nowy)
        if nowy.is_important:
            await send_push_notification(nowy.subject,nowy.snippet,nowy.sender,ntfy_key)

    return True





