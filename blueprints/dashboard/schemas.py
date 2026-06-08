from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from blueprints.employees.schemas import EmployeeResponseSchema
from blueprints.payslip.schemas import PayslipSchema
from core.enums import UserRole

class DashboardAdminResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    role: UserRole = Field(..., examples=[UserRole.ADMIN])
    totalEmployees: int = Field(..., examples=[1000])
    totalDepartments: int = Field(..., examples=[1000])
    todayAttendance: int = Field(..., examples=[1000])
    pendingLeaves: int = Field(..., examples=[1000])

class DashboardEmployeeResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    role: UserRole = Field(..., examples=[UserRole.EMPLOYEE])
    employeeId: int = Field(..., examples=[1])
    employee: EmployeeResponseSchema | None = Field(default=None)
    currentMonthAttendance: int = Field(..., examples=[1])
    pendingLeaves: int = Field(..., examples=[10])
    latestPayslip: PayslipSchema | None = Field(default=None)

# Definimos un esquema maestro de unión
class DashboardUnionResponseSchema(BaseModel):
    # APIFlask leerá este esquema y documentará ambas estructuras en Swagger
    admin_view: DashboardAdminResponseSchema | None = Field(
        default=None, 
        description="Response schema when user role is ADMIN"
    )
    employee_view: DashboardEmployeeResponseSchema | None = Field(
        default=None, 
        description="Response schema when user role is EMPLOYEE"
    )