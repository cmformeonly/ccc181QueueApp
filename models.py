from datetime import datetime
from decimal import Decimal

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, String, func, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class Customer(db.Model):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(120), unique=True)

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="customer")

    __table_args__ = (
        CheckConstraint("email = lower(email)", name="ck_customers_email_lowercase"),
    )


class Service(db.Model):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    avg_minutes: Mapped[int]
    active: Mapped[bool] = mapped_column(default=True, server_default=true())

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="service")

    __table_args__ = (
        CheckConstraint("avg_minutes > 0", name="ck_services_avg_minutes"),
    )


class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id", ondelete="RESTRICT"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="RESTRICT"))
    status: Mapped[str] = mapped_column(String(20), default="waiting", server_default="waiting")
    kilos_estimate: Mapped[int]
    actual_kilos: Mapped[Decimal | None] = mapped_column(Numeric(4, 1))
    care_note: Mapped[str | None] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    called_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    customer: Mapped["Customer"] = relationship(back_populates="tickets")
    service: Mapped["Service"] = relationship(back_populates="tickets")

    __table_args__ = (
        CheckConstraint(
            "status IN ('waiting', 'washing', 'called', 'served', 'left')",
            name="ck_tickets_status",
        ),
        CheckConstraint(
            "kilos_estimate BETWEEN 1 AND 15",
            name="ck_tickets_kilos_estimate",
        ),
        CheckConstraint(
            "actual_kilos > 0",
            name="ck_tickets_actual_kilos",
        ),
        CheckConstraint(
            "status NOT IN ('called', 'served') OR called_at IS NOT NULL",
            name="ck_tickets_called_at_set",
        ),
    )