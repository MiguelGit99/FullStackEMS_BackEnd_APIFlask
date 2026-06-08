from datetime import datetime
from decimal import Decimal
from alembic.environment import TYPE_CHECKING
from sqlalchemy import INT, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from blueprints.employees.models import Employee
from core.extensions import db

# Esto SOLO lo lee VS Code para quitar los warnings y darte autocompletado, y evitar tener entre comillas las clases requeridas
if TYPE_CHECKING:
    from blueprints.employees.models import Employee

class Payslip(db.Model):
    __tablename__ = "Payslip"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employeeId: Mapped[int] = mapped_column(ForeignKey("Employee.id"), nullable=False)
    month: Mapped[int] = mapped_column(INT, nullable=False)
    year: Mapped[int] = mapped_column(INT, nullable=False)
    basicSalary: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    allowances: Mapped[Decimal] = mapped_column(db.Numeric(10, 2), nullable=True, default=0)
    deductions: Mapped[Decimal] = mapped_column(db.Numeric(10, 2), nullable=True, default=0)
    netSalary: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    # createdAt: Mapped[datetime] = mapped_column(db.DateTime, nullable=False, default=lambda: datetime.now())
    # updatedAt: Mapped[datetime] = mapped_column(db.DateTime, nullable=False, default=lambda: datetime.now(), onupdate=lambda: datetime.now())

    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
   
    employee: Mapped[Employee] = relationship("Employee", back_populates="payslip")
    
