from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Tariff(Base):
    __tablename__ = "tariffs"

    id: Mapped[int] = mapped_column(primary_key=True)
    bezug_ct_per_kwh: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)
    einspeisung_ct_per_kwh: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)
    mitgliedsbeitrag_eur_per_year: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    valid_from: Mapped[date] = mapped_column(Date, nullable=False)
