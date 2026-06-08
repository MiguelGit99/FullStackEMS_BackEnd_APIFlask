from datetime import date, datetime
import logging

from apiflask import abort
from sqlalchemy import select, cast, Date
from blueprints.attendance.models import Attendance
from blueprints.employees.models import Employee
from core.enums import AttendanceStatus, DayType
from core.extensions import db

logger = logging.getLogger(__name__)

def register_clockIn(employee_id: int):
    # stmt = (
    #     select(Employee)
    #     .where(Employee.id == employee_id)  
    # )

    # db_employee = db.session.execute(stmt).scalar_one_or_none()

    db_employee = db.session.get(Employee, employee_id)

    if(db_employee is None):
        abort(404, "Employee not found")

    if (db_employee.isDeleted):
        abort(403, "Your account is deactivated. You cannot clockIn/clockOut.")
    
    stmt = (
        select(Attendance)
        .where(
            Attendance.employeeId == employee_id,
            Attendance.date == date.today()
        )
    )

    db_attendance = db.session.execute(stmt).scalar_one_or_none()

    if db_attendance is None:
        today = datetime.now()
        hour_limit = datetime(today.year, today.month, today.day, 9, 0, 0)
        isLate = today > hour_limit
        #isLate = datetime.now() > datetime(date.year, datetime.month, datetime.day, 9, 0, 0)
        db_attendance = Attendance (
            employeeId = db_employee.id,
            date = date.today(),
            checkIn = today,
            status = AttendanceStatus.LATE if isLate else AttendanceStatus.PRESENT 
        )

        #return db_attendance
    elif db_attendance.checkOut is None:
        # logger.info(f"TIPO DE DATOS EN LA RESTA:")
        # logger.info(f"datetime.now() es: {type(datetime.now())}")
        # logger.info(f"db_attendance.checkIn es: {type(db_attendance.checkIn)}")
        # print("TIPO DE DATOS EN LA RESTA:")
        # print("datetime.now() es:", type(datetime.now()))
        # print("db_attendance.checkIn es:", type(db_attendance.checkIn))
        difference_timedelta = datetime.now() - db_attendance.checkIn 
        #datetime.now().time() - datetime(db_attendance.checkIn).time()
        diffHours = round(
            (difference_timedelta.total_seconds() / 60) / 60,
            2
        )

        # logger.info(f"difference_timedelta es: {difference_timedelta}")
        # logger.info(f"difference_timedelta.total_seconds() es: {difference_timedelta.total_seconds()}")
        # logger.info(f"diffHours es: {diffHours}")
        
        
        db_attendance.checkOut = datetime.now()
        db_attendance.workingHours = diffHours

        if diffHours >= 8:
            db_attendance.dayType = DayType.FULL_DAY
        elif diffHours >= 6:
            db_attendance.dayType = DayType.THREE_QUARTER_DAY
        elif diffHours >= 4:
            db_attendance.dayType = DayType.HALF_DAY
        else:
            db_attendance.dayType = DayType.SHORT_DAY
        
    try:
        db.session.add(db_attendance)
        db.session.commit()
    except Exception as e:
        #logger.exception
        db.session.rollback()

        abort(400, "Attendance error while updating data base.")
    
    return db_attendance





def get_all_attendance(employee_id: int, limit: int):
    # stmt = (
    #     select(Employee)
    #     .where(Employee.id == employee_id)
    # )

    # db_employee = db.session.execute(stmt).scalar_one_or_none()

    db_employee = db.session.get(Employee, employee_id)

    if(db_employee is None):
        abort(404, message="Employee not found")

    limit = limit if limit else 30

    stmt = (
        select(Attendance)
        .where(Attendance.employeeId == employee_id)
        .order_by(Attendance.date.desc())
        .limit(limit)
    )

    db_history_attendance = db.session.execute(stmt).scalars().all()

    return (
        db_history_attendance, 
        db_employee.isDeleted 
    )