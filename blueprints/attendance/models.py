# from enum import Enum

from alembic.environment import TYPE_CHECKING
from sqlalchemy import INT, Date, DateTime, ForeignKey, UniqueConstraint, Enum, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date as PyDate, datetime

from core.enums import AttendanceStatus, DayType
from core.extensions import db

# Esto SOLO lo lee VS Code para quitar los warnings y darte autocompletado, y evitar tener entre comillas las clases requeridas
if TYPE_CHECKING:
    from blueprints.employees.models import Employee


class Attendance(db.Model):
    __tablename__ = "Attendance"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employeeId: Mapped[int] = mapped_column(ForeignKey("Employee.id"), nullable=False)
    date: Mapped[PyDate] = mapped_column(Date, nullable=False)
    checkIn: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    checkOut: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[AttendanceStatus] = mapped_column(
        Enum(AttendanceStatus, values_callable=lambda obj: [e.value for e in obj]),
        default=AttendanceStatus.PRESENT,
        server_default=text(f"'{AttendanceStatus.PRESENT.value}'"),
        nullable=True
    )
    workingHours: Mapped[int] = mapped_column(INT, nullable=True)
    dayType: Mapped[DayType] = mapped_column(
        Enum(DayType, values_callable=lambda obj: [e.value for e in obj]),
        nullable=True
    )
    # createdAt: Mapped[datetime] = mapped_column(db.DateTime, nullable=False, default=lambda: datetime.now())
    # updatedAt: Mapped[datetime] = mapped_column(db.DateTime, nullable=False, default=lambda: datetime.now(), onupdate=lambda: datetime.now())
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    employee: Mapped[Employee] = relationship("Employee", back_populates="attendance")
    
    # Configuración de restricciones a nivel de tabla 
    __table_args__ = (
        UniqueConstraint(
            "employeeId", 
            "date", 
            name="uq_attendance_employee_date"
        ),
    )
    

    # id = db.Column(db.Integer, primary_key = True)
    # employeeId =  db.Column(db.Integer, db.ForeignKey("Employee.id"), nullable=False)
    # date = db.Column(db.Date, nullable = False)
    # checkIn = db.Column(db.DateTime, nullable = True)
    # checkOut = db.Column(db.DateTime, nullable = True)
    # status = db.Column(db.Enum(
    #     AttendanceStatus,
    #     values_callable=lambda obj: [e.value for e in obj]
    # ), nullable = True, default=AttendanceStatus.PRESENT)
    # workingHours = db.Column(db.Integer, nullable = True)
    # dayType = db.Column(db.Enum(
    #     DayType,
    #     values_callable=lambda obj: [e.value for e in obj]
    # ), nullable = True)
    # employee = db.relationship("Employee", back_populates="attendance", lazy=True, uselist=False)

    # UniqueConstraint(
    #     "employeeId",
    #     "date",
    #     name="uq_attendance_employee_date"
    # )