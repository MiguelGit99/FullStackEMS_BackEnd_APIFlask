from datetime import UTC, date, datetime
# from enum import Enum

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blueprints.employees.models import Employee
from core.enums import LeaveStatus, LeaveType
from core.extensions import db

class LeaveApplication(db.Model):
    __tablename__ = "LeaveApplication"

    # 1. Llave primaria explícita e incremental
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # 2. Clave foránea obligatoria (required: true)
    employeeId: Mapped[int] = mapped_column(ForeignKey("Employee.id"), nullable=False)
    # 3. Enums y campos obligatorios (Al usar Mapped[tipo] sin Optional, asume nullable=False)
    type: Mapped[LeaveType] = mapped_column(
        Enum(LeaveType, values_callable=lambda obj: [e.value for e in obj])
    )
    
    startDate: Mapped[date] = mapped_column(Date)
    endDate: Mapped[date] = mapped_column(Date)
    reason: Mapped[str] = mapped_column(String(500))
    
    # 4. Status obligatorio pero con valor por defecto si no se envía
    status: Mapped[LeaveStatus] = mapped_column(
        Enum(LeaveStatus, values_callable=lambda obj: [e.value for e in obj]),
        default=LeaveStatus.PENDING,
        server_default=text(f"'{LeaveStatus.PENDING.value}'")
    )

    # 5. Timestamps automáticos delegados a SQL Server (func.now())
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # 6. Relación moderna con tipado (Equivalente al .populate)
    # Nota: Asegúrate de que en tu modelo Employee la relación se llame "leave_application"
    employee: Mapped["Employee"] = relationship("Employee", back_populates="leave_application")

    
    
    
    
    # employeeId = db.Column(db.Integer, db.ForeignKey("Employee.id"), primary_key = True, autoincrement=False)
    # type = db.Column(db.Enum(
    #     LeaveType,
    #     values_callable=lambda obj: [e.value for e in obj]
    # ), nullable = True)
    # startDate = db.Column(db.Date, nullable=True)
    # endDate = db.Column(db.Date, nullable=True)
    # reason = db.Column(db.String, nullable=True)
    # status = db.Column(db.Enum(
    #     LeaveStatus,
    #     values_callable=lambda obj: [e.value for e in obj]
    # ), nullable = True, default=LeaveStatus.PENDING)
    # createdAt = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    # updatedAt = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(), onupdate=lambda: datetime.now())
    # employee = db.relationship("Employee", back_populates="leave_application", lazy=True, uselist=False)


    
    