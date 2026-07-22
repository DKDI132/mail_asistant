from sqlalchemy import select
from entity import Email
from typing import List, Optional
from datetime import datetime


class Email_repo:
    db = None
    def __init__(self,con):
        self.db = con

    def get_by_id(self, email_id: str) -> Optional[Email]:
        return self.db.query(Email).filter(Email.id == email_id).first()

    def get_all(self) -> List[Email]:
        return self.db.query(Email).all()

    def get_emails_since(self, since_date: datetime) -> List[Email]:
        return self.db.query(Email).filter(Email.created_at >= since_date).all()

    def create(self, email_obj: Email) -> Email:
        self.db.add(email_obj)
        self.db.commit()
        self.db.refresh(email_obj)
        return email_obj

    def save_multiple(self, emails: List[Email]) -> int:
        self.db.add_all(emails)
        self.db.commit()
        return len(emails)