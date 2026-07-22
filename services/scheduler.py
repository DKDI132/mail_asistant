import asyncio
import os

from database import SessionLocal
from repo import email_repository
from services.mail_service import mail_analizer
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("GMAIL_EMAIL")
password = os.getenv("GMAIL_APP_PASSWORD")
ntfy_key = os.getenv("NTFY_KEY")

async def scheduler():
    while True:
        with SessionLocal() as db:
            polaczenie = email_repository.Email_repo(db)
            await mail_analizer(polaczenie,user,password,ntfy_key)
        await asyncio.sleep(3600)

