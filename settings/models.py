from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class HistoryRequests(Base):
    __tablename__ = 'history_requests'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    brand: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    years: Mapped[str] = mapped_column(nullable=False)
    mileage: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[str] = mapped_column(nullable=False)
    date_request: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    user_id: Mapped[int]
    username: Mapped[str]


class BrandModels(Base):
    __tablename__ = 'brands_nodels'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    brand_name: Mapped[str] = mapped_column(nullable=False)
    brand_id: Mapped[int] = mapped_column(nullable=False)
    model_name: Mapped[str] = mapped_column(nullable=False)
    model_id: Mapped[int] = mapped_column(nullable=False)
