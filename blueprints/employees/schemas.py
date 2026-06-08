# Usando Schemas con Pydantic para validar y serializar datos de productos y marcas
# Schemas se usa para los Response o envío de modelos de datos del FronEnd al BackEnd, mientras que los Models se usan para la representación de la base de datos
# Esto ayuda a mantener el código limpio y a manejar correctamente tipos de datos complejos como Decimal
from decimal import Decimal
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator
from blueprints.auth.schemas import UserResponseSchema, UserSchema, UserUpdateSchema
from core.enums import Departments, EmploymentStatus

class EmployeeSearchSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    department: str | None = Field(default=None, examples=["Sales", "HR", "Engineering"])
    
class EmployeeCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    userId: int | None = Field(default=None, examples=[2])
    firstName: str = Field(...) # Requeridos
    lastName: str = Field(...) # Requeridos 
    email: EmailStr = Field(...) # Requeridos
    phone: str | None = Field(default=None, examples=["8115578863"])
    position: str | None = Field(default=None, examples=["Director"])
    basicSalary: Decimal = Field(default=0, examples=[10000])
    allowances: Decimal = Field(default=0, examples=[5000])
    deductions: Decimal = Field(default=0, examples=[3000])
    employmentStatus: EmploymentStatus | None = Field(default=None, examples=[EmploymentStatus.ACTIVE])
    joinDate: date | None = Field(default=None, examples=["2026-05-12"])
    bio: str | None = Field(default=None, examples=["Biography text"])
    department: Departments | None = Field(default=None, examples=[Departments.SALES])
    user: UserSchema | None = None

    @field_validator("firstName", "lastName", "email")
    @classmethod
    def validate_names(cls, value):
        if value is None or len(value.strip()) <= 0:
            raise ValueError(
                "Missing required fields"
            )

        return value.strip()
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is not None and not value.isdigit():
            raise ValueError(
                "Phone must contain only digits"
            )

        if len(value) != 10:
            raise ValueError(
                "Phone must be 10 digits"
            )

        return value
    
    @field_validator("basicSalary")
    @classmethod
    def validate_salary(cls, value):
        if value is not None and value < 0:
            raise ValueError(
                "Salary cannot be negative"
            )

        return value
    
    @model_validator(mode="after")
    def validate_salary_totals(self):
        if self.deductions > self.basicSalary:
            raise ValueError(
                "Deductions cannot exceed salary"
            )

        return self

class EmployeeUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int | None = Field(default=None, examples=[1])
    userId: int | None = Field(default=None, examples=[2])
    firstName: str = Field(...) # Requeridos
    lastName: str = Field(...) # Requeridos 
    email: EmailStr = Field(...) # Requeridos
    phone: str | None = Field(default=None, examples=["8115578863"])
    position: str | None = Field(default=None, examples=["Director"])
    basicSalary: Decimal = Field(default=0, examples=[10000])
    allowances: Decimal = Field(default=0, examples=[5000])
    deductions: Decimal = Field(default=0, examples=[3000])
    employmentStatus: EmploymentStatus | None = Field(default=None, examples=[EmploymentStatus.ACTIVE])
    joinDate: date | None = Field(default=None, examples=["2026-05-12"])
    bio: str | None = Field(default=None, examples=["Biography text"])
    department: Departments | None = Field(default=None, examples=[Departments.SALES])
    user: UserUpdateSchema | None = None

    @field_validator("firstName", "lastName", "email")
    @classmethod
    def validate_names(cls, value):
        if value is None or len(value.strip()) <= 0:
            raise ValueError(
                "Missing required fields"
            )

        return value.strip()
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is not None and not value.isdigit():
            raise ValueError(
                "Phone must contain only digits"
            )

        if len(value) != 10:
            raise ValueError(
                "Phone must be 10 digits"
            )

        return value
    
    @field_validator("basicSalary")
    @classmethod
    def validate_salary(cls, value):
        if value is not None and value < 0:
            raise ValueError(
                "Salary cannot be negative"
            )

        return value
    
    @model_validator(mode="after")
    def validate_salary_totals(self):
        if self.deductions > self.basicSalary:
            raise ValueError(
                "Deductions cannot exceed salary"
            )

        return self
    
    
# Hereda de EmployeeSchema para incluir el usuario asociado en la respuesta del endpoint de creación de empleado
class EmployeeResponseSchema(EmployeeUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    isDeleted: bool | None = Field(default=None, examples=[False])
    user: UserResponseSchema | None = None

class EmployeeShortResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = Field(default=None, examples=[1])
    firstName: str = Field(...) # Requeridos
    lastName: str = Field(...) # Requeridos 
    isDeleted: bool | None = Field(default=None, examples=[False])
    