
import logging
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash
#from enum import Enum
# from blueprints.employees.models import Employee
from core.enums import UserRole
from datetime import UTC, datetime
from core.extensions import db
# from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

# Esto SOLO lo lee VS Code para quitar los warnings y darte autocompletado, y evitar tener entre comillas las clases requeridas
if TYPE_CHECKING:
    from blueprints.employees.models import Employee  # Ajusta la ruta a donde esté tu modelo realmente

logger = logging.getLogger(__name__)

class User(db.Model):
    __tablename__ = "User"
    
    # Si se desea usar un esquema específico para esta tabla, descomentar esta línea y ajustar el nombre del esquema según sea necesario.
    # __table_args__ = { "schema": "security" } 

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, values_callable=lambda obj: [e.value for e in obj]),
        default=UserRole.EMPLOYEE,
        server_default=text(f"'{UserRole.EMPLOYEE.value}'")
    )
    # createdAt: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now())
    # updatedAt: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now())
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
   
    employee: Mapped[Employee] = relationship("Employee", back_populates="user") # type: ignore
    
    #id = db.Column(db.Integer, primary_key=True)
    #email = db.Column(db.String(255), nullable=False, unique=True)
    #password = db.Column(db.String(255), nullable=False)
    # role = db.Column(db.Enum(
    #     UserRole,
    #     values_callable=lambda obj: [e.value for e in obj]
    # ), nullable=False, default=UserRole.EMPLOYEE)
    # createdAt = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    # updatedAt = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    # employee = db.relationship("Employee", back_populates="user", lazy=True, uselist=False)

    def hash_password(self, password):
        self.password = (
            bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

    def verify_password(self, password):
        try:
            isValid = bcrypt.checkpw(
                password.encode('utf-8'),
                self.password.encode('utf-8')
            )
        except ValueError:
            logger.exception("Error al verificar la contraseña: formato de hash no válido.", 
                             exc_info=True, 
                             stack_info=True)
            isValid = False

        return isValid
            
