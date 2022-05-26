
from enum import unique
from operator import index
from tkinter.tix import Tree

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from database import Base
from sqlalchemy.orm import relationship

employee_timesheet = Table('employee_timesheet', Base.metadata,
    Column('emp_id', ForeignKey('employees.emp_id'), primary_key=True),
    Column('id', ForeignKey('timesheet.id'), primary_key=True))

class Employees(Base):
    __tablename__ = 'employees'

    emp_id = Column(Integer, primary_key = True, index = True)
    emp_name = Column(String)

    timesheet = relationship("TimeSheet", secondary="employee_timesheet",  back_populates="employees", lazy = True)


class TimeSheet(Base):
    __tablename__ = "timesheet"    

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index = True)
    actual_hrs = Column(Integer)
    employee_id = Column(Integer, ForeignKey("employees.emp_id"), unique = True)

    employees = relationship("Employees", secondary="employee_timesheet", back_populates="timesheet",  lazy = True)
