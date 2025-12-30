from typing import List, Optional
from sqlalchemy import String, Integer, Enum, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column 
from api.db.base_model import BaseModel
import uuid


class UserRole(str,Enum):
    landlord = "landlord"
    tenant = "tenant"
    admin = "admin"


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key = True, default=uuid.uuid4, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str | None] = mapped_column(Text)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), name="user_role", nullable=False, default=UserRole.tenant)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
