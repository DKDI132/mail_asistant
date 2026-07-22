from sqlalchemy.orm import Mapped, mapped_column
from database import Base
class Email(Base):
    __tablename__ = "emails"
    id: Mapped[str] = mapped_column(primary_key=True)
    sender: Mapped[str] = mapped_column(nullable=True)
    subject: Mapped[str] = mapped_column(nullable=True)
    body: Mapped[str] = mapped_column(nullable=True)
    snippet: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[str] = mapped_column(nullable=True)
    is_read: Mapped[bool] = mapped_column(default=False)
    is_important: Mapped[bool] = mapped_column(default=False)
