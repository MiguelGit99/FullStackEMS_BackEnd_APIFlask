from datetime import date as PyDate, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator

from core.enums import AttendanceStatus, DayType

class AttendanceLimitSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    limit: int | None = Field(default=30, examples=[30])
    

class AttendanceResponseSchema(BaseModel):
    employeeId: int | None = Field(default=None, examples=[1])
    
    # REEMPLAZA EL OPERADOR '|' POR 'Optional' ÚNICAMENTE EN LAS FECHAS para que no cause error en Swagger
    date: PyDate | None = Field(default=None, examples=["2026-05-16T08:00:00"])
    #date: Optional[date] = None
    # checkIn: Optional[datetime] = None
    # checkOut: Optional[datetime] = None
    
    checkIn: datetime | None = Field(default=None, examples=["2026-05-16T08:00:00"])
    checkOut: datetime | None = Field(default=None, examples=["2026-05-17T08:00:00"])
    
    status: AttendanceStatus | None = Field(default=None, examples=[AttendanceStatus.PRESENT])
    workingHours: Decimal | None = Field(default=None, examples=[8.5])
    dayType: DayType | None = Field(default=None, examples=[DayType.FULL_DAY])

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_checkIn_checkOut(self):
        if self.checkIn and self.checkOut and self.checkIn > self.checkOut:
            raise ValueError(
                "ChekOut must be a date greather than checkIn"
            )
        
        return self

class AttendancePlusInfoResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    attendanceList: list[AttendanceResponseSchema] | None = Field(default=[])
    employeeIsDeleted: bool = Field(..., examples=[False])
    