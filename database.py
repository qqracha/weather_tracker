from datetime import datetime
from sqlalchemy import create_engine, Integer, String, Numeric, Text, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

class Base(DeclarativeBase):
    pass

class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    requested_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    response: Mapped["Response"] = relationship(back_populates="request", uselist=False)

class Response(Base):
    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("requests.id", ondelete="CASCADE"), nullable=False)
    temperature: Mapped[float | None] = mapped_column(Numeric(5, 2))
    feels_like: Mapped[float | None] = mapped_column(Numeric(5, 2))
    humidity: Mapped[int | None] = mapped_column(Integer)
    description: Mapped[str | None] = mapped_column(String(255))
    wind_speed: Mapped[float | None] = mapped_column(Numeric(6, 2))
    raw_json: Mapped[str | None] = mapped_column(Text)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    request: Mapped["Request"] = relationship(back_populates="response")

def init_db() -> None:
    Base.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)