from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, field_validator

from blueprints.employees.schemas import EmployeeShortResponseSchema

# class PayslipSearchSchema(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     id: int | None = Field(..., examples=[1]) 
    

class PayslipSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    # id: int | None = None
    employeeId: int = Field(..., examples=[1]) 
    month: int = Field(..., examples=[5])
    year: int = Field(..., examples=[2026])
    basicSalary: Decimal = Field(..., examples=[25000.00])
    allowances: Decimal | None = Field(default=None, examples=[1500.00])
    deductions: Decimal | None = Field(default=None, examples=[500.00])
    netSalary: Decimal | None = Field(default=None, examples=[26000.00])

    @field_validator("employeeId", "month", "year", "basicSalary")
    @classmethod
    def validate_positive_values(cls, value):
        if value <= 0:
            raise ValueError(
                "Value must be greather than zero"
            )

        return value
    
    @field_validator("month")
    @classmethod
    def validate_month_range(cls, value):
        if value < 1 or value > 12:
            raise ValueError("Month must be between 1 and 12")
        return value
    

class PayslipResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int | None = Field(default=None, examples=[1])
    employeeId: int | None = Field(default=None, examples=[2])
    month: int | None = Field(default=None, examples=[11])
    year: int | None = Field(default=None, examples=[2026])
    basicSalary: Decimal | None = Field(default=None, examples=[15000])
    allowances: Decimal | None = Field(default=None, examples=[6000])
    deductions: Decimal | None = Field(default=None, examples=[4000])
    netSalary: Decimal | None = Field(default=None, examples=[10000])

    employee: EmployeeShortResponseSchema | None = Field(default=[])
    

    
    