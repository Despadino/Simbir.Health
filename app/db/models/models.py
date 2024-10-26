import uuid
from sqlalchemy import ForeignKey, String, UUID, Boolean, DateTime
import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base

class Users(Base):
    __tablename__ = 'Users'
    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    lastName: Mapped[str] = mapped_column(String, nullable=False)
    firstName: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    tokens: Mapped[str] = mapped_column(String, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    employee_roles: Mapped[list["EmployeeRoles"]] = relationship("EmployeeRoles", back_populates="user")
    timetables: Mapped[list["Timetable"]] = relationship("Timetable", back_populates="doctor")
    appointments: Mapped[list["Appointment"]] = relationship("Appointment", back_populates="user")

class Roles(Base):
    __tablename__ = 'Roles'
    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    Name: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    employee_roles: Mapped[list["EmployeeRoles"]] = relationship("EmployeeRoles", back_populates="role")



class EmployeeRoles(Base):
    __tablename__ = 'EmployeeRoles'
    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(UUID, ForeignKey('Users.id'), nullable=False)
    roles_id: Mapped[str] = mapped_column(UUID, ForeignKey('Roles.id'), nullable=False)

    # Relationships
    user: Mapped["Users"] = relationship("Users", back_populates="employee_roles")
    role: Mapped["Roles"] = relationship("Roles", back_populates="employee_roles")





class Hospitals(Base):
    __tablename__ = 'Hospitals'
    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    contactPhone: Mapped[str] = mapped_column(String, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    rooms: Mapped[list["Rooms"]] = relationship("Rooms", back_populates="hospital")
    timetables: Mapped[list["Timetable"]] = relationship("Timetable", back_populates="hospital")
    

class Rooms(Base):
    __tablename__ = 'Rooms'
    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    hospitals_id: Mapped[str] = mapped_column(UUID, ForeignKey('Hospitals.id'), nullable=False)

    hospital: Mapped["Hospitals"] = relationship("Hospitals", back_populates="rooms")



class Timetable(Base):
    __tablename__ = 'Timetable'
    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    hospital_id: Mapped[str] = mapped_column(UUID, ForeignKey('Hospitals.id'), nullable=False)
    doctor_id: Mapped[str] = mapped_column(UUID, ForeignKey('Users.id'), nullable=False)
    from_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    to_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    room: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    hospital: Mapped["Hospitals"] = relationship("Hospitals", back_populates="timetables")
    doctor: Mapped["Users"] = relationship("Users", back_populates="timetables")
    appointments: Mapped[list["Appointment"]] = relationship("Appointment", back_populates="timetable")



class Appointment(Base):
    __tablename__ = 'Appointment'
    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    timetable_id: Mapped[str] = mapped_column(UUID, ForeignKey('Timetable.id'), nullable=False)
    user_id: Mapped[str] = mapped_column(UUID, ForeignKey('Users.id'), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relationships
    timetable: Mapped["Timetable"] = relationship("Timetable", back_populates="appointments")
    user: Mapped["Users"] = relationship("Users", back_populates="appointments")
