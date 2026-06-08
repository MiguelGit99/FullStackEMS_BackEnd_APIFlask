# Usando Schemas con Pydantic para validar y serializar datos de productos y marcas
# Schemas se usa para los Response o envío de modelos de datos del FronEnd al BackEnd, mientras que los Models se usan para la representación de la base de datos
# Esto ayuda a mantener el código limpio y a manejar correctamente tipos de datos complejos como Decimal
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

from core.enums import UserRole

class UserResponseSchema(BaseModel):
    id: int | None = Field(default=None, examples=[1])
    email: EmailStr | None = Field(default=None, examples=["testemail@mail.com"])
    role: UserRole | None = Field(default=None, examples=[UserRole.EMPLOYEE])

    model_config = ConfigDict(from_attributes=True)

    @field_validator("email", "role")
    @classmethod
    def validate_fields(cls, value):
        if value is None or len(value.strip()) <= 0:
            raise ValueError(
                "Missing required fields"
            )

        return value.strip()


# Hereda de UserResponseSchema para incluir el usuario asociado en la respuesta del endpoint de creación de empleado
class UserSchema(UserResponseSchema):
    model_config = ConfigDict(from_attributes=True)

    password: str = Field(...) # Requeridos

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if value is None or len(value.strip()) <= 0:
            raise ValueError(
                "Missing required fields"
            )

        return value.strip()

class UserUpdateSchema(UserResponseSchema):
    model_config = ConfigDict(from_attributes=True)

    password: str | None = Field(default=None) 
    
class LoginSchema(BaseModel):
    email: EmailStr = Field(default=None, examples=["testemail@mail.com"]) # Requeridos
    password: str = Field(...) # Requeridos

    model_config = ConfigDict(from_attributes=True)

    # TODO: Centralizar este tipo de validaciones
    @field_validator("email", "password")
    @classmethod
    def validate_fields(cls, value):
        if value is None or len(value.strip()) <= 0:
            raise ValueError(
                "Missing required fields"
            )

        return value.strip()

class LoginResponseSchema(BaseModel):
    isValid: bool = Field(..., examples=[False]) # Requeridos
    user: UserResponseSchema | None = None
    access_token: str | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)

class ChangePasswordSchema(BaseModel):
    currentPassword: str = Field(...) # Requeridos
    newPassword: str = Field(...) # Requeridos

    @field_validator("currentPassword", "newPassword")
    @classmethod
    def validate_fields(cls, value):
        if value is None or len(value.strip()) <= 0:
            raise ValueError(
                "Missing required fields"
            )

        return value.strip()

    # @model_validator(mode="after")
    # def validate_equal_passwords(self):
    #     if self.currentPassword != self.newPassword:
    #         raise ValueError(
    #             "Passwords do not match."
    #         )

    #     return self

    model_config = ConfigDict(from_attributes=True)