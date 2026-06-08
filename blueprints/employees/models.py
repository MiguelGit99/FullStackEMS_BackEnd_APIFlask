
from decimal import Decimal
from typing import List

from alembic.environment import TYPE_CHECKING
import logging
from sqlalchemy import DateTime, Enum, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
#from enum import Enum
from core.enums import EmploymentStatus, Departments
from datetime import UTC, date, date, datetime
from core.extensions import db

# Esto SOLO lo lee VS Code para quitar los warnings y darte autocompletado, y evitar tener entre comillas las clases requeridas
if TYPE_CHECKING:
    from blueprints.auth.models import User  # Ajusta la ruta a donde esté tu modelo realmente
    from blueprints.attendance.models import Attendance
    from blueprints.leave_application.models import LeaveApplication
    from blueprints.payslip.models import Payslip

logger = logging.getLogger(__name__)

class Employee(db.Model):
    __tablename__ = "Employee"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    userId: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("User.id"), nullable=False, unique=True)
    firstName: Mapped[str] = mapped_column(db.String(100), nullable=False)
    lastName: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(50), nullable=False)
    position: Mapped[str] = mapped_column(db.String(100), nullable=False)
    basicSalary: Mapped[Decimal] = mapped_column(db.Numeric(10, 2), nullable=False, default=0)
    allowances: Mapped[Decimal] = mapped_column(db.Numeric(10, 2), nullable=False, default=0)
    deductions: Mapped[Decimal] = mapped_column(db.Numeric(10, 2), nullable=False, default=0)
    employmentStatus: Mapped[EmploymentStatus] = mapped_column(
        Enum(EmploymentStatus, values_callable=lambda obj: [e.value for e in obj]),
        default=EmploymentStatus.ACTIVE,
        server_default=text(f"'{EmploymentStatus.ACTIVE.value}'"),
        nullable=False
    )
    joinDate: Mapped[date] = mapped_column(db.Date, nullable=False)
    isDeleted: Mapped[bool] = mapped_column(db.Boolean, nullable=False, default=False)
    bio: Mapped[str] = mapped_column(db.Text, nullable=False, default="")
    department: Mapped[Departments] = mapped_column(
        Enum(Departments, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False
    )
    # createdAt: Mapped[datetime] = mapped_column(db.DateTime, nullable=False, default=lambda: datetime.now())
    # updatedAt: Mapped[datetime] = mapped_column(db.DateTime, nullable=False, default=lambda: datetime.now(), onupdate=lambda: datetime.now())
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
   
    user: Mapped[User] = relationship("User", back_populates="employee", lazy=True, uselist=False)
    attendance: Mapped[List[Attendance]] = relationship("Attendance", back_populates="employee", lazy=True, uselist=False)
    leave_application: Mapped[List[LeaveApplication]] = relationship("LeaveApplication", back_populates="employee", lazy=True, uselist=False)
    payslip: Mapped[List[Payslip]] = relationship("Payslip", back_populates="employee", lazy=True, uselist=False)
    
    # id = db.Column(db.Integer, primary_key = True)
    # userId = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False, unique=True)
    # firstName = db.Column(db.String(100), nullable=False)
    # lastName = db.Column(db.String(100), nullable=False)
    # email = db.Column(db.String(255), nullable=False)
    # phone = db.Column(db.String(50), nullable=False)
    # position = db.Column(db.String(100), nullable=False)
    # basicSalary = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    # allowances = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    # deductions = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    # employmentStatus = db.Column(db.Enum(
    #     EmploymentStatus,
    #     values_callable=lambda obj: [e.value for e in obj]
    # ), nullable=False, default=EmploymentStatus.ACTIVE)
    # joinDate = db.Column(db.Date, nullable=False)
    # isDeleted = db.Column(db.Boolean, nullable=False, default=False)
    # bio = db.Column(db.Text, nullable=False, default="")
    # department = db.Column(db.Enum(
    #     Departments,
    #     values_callable=lambda obj: [e.value for e in obj]
    # ), nullable=False)
    # createdAt = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    # updatedAt = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(), onupdate=lambda: datetime.now(UTC))
    # user = db.relationship("User", back_populates="employee", lazy=True, uselist=False)