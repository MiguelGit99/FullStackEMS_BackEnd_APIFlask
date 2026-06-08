from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from blueprints.employees.schemas import EmployeeResponseSchema, EmployeeShortResponseSchema
from blueprints.leave_application.models import LeaveApplication
from core.enums import LeaveStatus, LeaveType

class LeaveApplicationSearchSchema(BaseModel):
    status: LeaveStatus = Field(default=None, examples="Pending") # "Field(...)" Indica que es campo requerido y "example" le dice a Swagger como rellenar los parametros de entrada al ejecutarlo

    model_config = ConfigDict(from_attributes=True)


class LeaveApplicationUpdateStatusSchema(BaseModel):
    id: int = Field(..., examples=1)
    status: LeaveStatus = Field(..., examples="Pending") # "Field(...)" Indica que es campo requerido y "example" le dice a Swagger como rellenar los parametros de entrada al ejecutarlo

    model_config = ConfigDict(from_attributes=True)


class LeaveApplicationSchema(BaseModel):
    id: int | None = Field(default=None)
    employeeId: int = Field(...) # Requeridos
    type: LeaveType = Field(...) # Requeridos
    startDate: date = Field(...)
    endDate: date = Field(...)
    reason: str = Field(...)
    status: LeaveStatus | None = Field(default=None, examples=[LeaveStatus.PENDING])
    
    employee: Optional[EmployeeShortResponseSchema] = None           
    
    model_config = ConfigDict(from_attributes=True)

    @field_validator("reason")
    @classmethod
    def validate_names(cls, value):
        if value is None or len(value.strip()) <= 0:
            raise ValueError(
                "Missing required fields"
            )

        return value.strip()

    @model_validator(mode="after")
    def validate_startDate_endDate(self):
        if self.startDate and self.endDate:
            today = date.today()
            # if ((self.startDate <= today) or (self.endDate <= today)):
            #     raise ValueError(
            #         "Start and End date fields must be greather than today"
            #     )
            if self.startDate > self.endDate:
                raise ValueError(
                    "End date must be greather than start date"
                )
        else:
            raise ValueError(
                "Start and End date fields are required"
                )
        return self

# class LeaveResponseSchema(BaseModel):
#     employee_id: int
#     type: LeaveType | None = None
#     startDate: date | None = None
#     endDate: date | None = None
#     reason: str | None = None
#     status: LeaveStatus | None = None

#     model_config = ConfigDict(from_attributes=True)



# Estructura de salida final (Aplica las mutaciones del .map())
class LeaveApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str                                          
    type: LeaveType = Field(default=None, examples=[LeaveType.CASUAL])
    startDate: str = Field(...)
    endDate: str = Field(...)
    reason: str | None = Field(default=None, examples=["Reason text..."])
    status: LeaveStatus | None = Field(default=None, examples=[LeaveStatus.PENDING])
    createdAt: str = Field(...)
    updatedAt: str = Field(...)

    employee: Optional[EmployeeResponseSchema] = None           # Propiedad nueva con el objeto completo
    employeeId: str = Field(...) 

    @classmethod
    def transform(cls, leave: LeaveApplication) -> "LeaveApplicationResponse":
        return cls(
            id=str(leave.id),
            type=leave.leave_type,
            startDate=leave.startDate.isoformat() if leave.startDate else "",
            endDate=leave.endDate.isoformat() if leave.endDate else "",
            reason=leave.reason,
            status=leave.status,
            createdAt=leave.createdAt.isoformat() if leave.createdAt else "",
            updatedAt=leave.updatedAt.isoformat() if leave.updatedAt else "",
            employee=EmployeeResponseSchema.model_validate(leave.employee) if leave.employee else None,
            employeeId=str(leave.employeeId) if leave.employeeId else ""
        )
