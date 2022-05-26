
from datetime import date, datetime
from os import stat 
from typing import List
from typing_extensions import Annotated

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import ForeignKey, null
from sqlalchemy.orm import Session
from uuid import UUID

import models
from database import engine, SessionLocal


app = FastAPI(
 title = 'Employee Details'
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()


class Employee(BaseModel):
    emp_name: str = Field(min_length = 2)

Employees = []



class TimeSheet(BaseModel):
    date: datetime = Field(..., example="2019-04-01T00:00:00.000Z", description="ISO 8601 format")
    actual_hrs: Annotated[str, Field(max_length= 10)]
    # emp_id: int = Field(ForeignKey("employees.emp_id"))

TimeSheets = []    


@app.get("/")
def Landing_page():
    return {"Welcome": "Employee Details FASTAPI"}


### to fetch all the employee details
@app.get("/all_employees/")
def read_emp(db: Session = Depends(get_db)):
    return db.query(models.Employees).all()


### to fetch the employee details by employee id
@app.get("/all_employees/{emp_id}")
def read_emp(emp_id: int, db: Session = Depends(get_db)):
    emp_details = db.query(models.Employees).filter(models.Employees.emp_id==emp_id).first()
    if emp_details is None:
        raise HTTPException(status_code= 404,  detail= "employee id doesn't exists")
    return emp_details
    


@app.post("/add_emp")
def create_new(employee: Employee, db: Session = Depends(get_db)):
    emp_model = models.Employees()
    emp_model.emp_name = employee.emp_name

    db.add(emp_model)
    db.commit()
    db.refresh(emp_model)

    return employee


@app.get("/all_timesheet/")
def read_timesheet(db: Session = Depends(get_db)):
    return db.query(models.TimeSheet).all()


''' To Create the Time Sheets for the employees'''
@app.post("/add_timesheet")
def create_new_timesheet(emp_id: int, timesheet: TimeSheet, db: Session = Depends(get_db)):
    ts_model = models.TimeSheet(employee_id =emp_id)
    ts_model.date = timesheet.date
    ts_model.actual_hrs = timesheet.actual_hrs

    db.add(ts_model)
    db.commit()
    db.refresh(ts_model)

    return ts_model


''' to fetch the timesheet by employee id'''

@app.get("/all_timesheet/{emp_id}")
def read_emp(emp_id: int, db: Session = Depends(get_db)):
    ts = db.query(models.TimeSheet).filter(models.TimeSheet.employee_id==emp_id).first()
    if ts is None:
        raise HTTPException(status_code= 404,  detail= "employee id doesn't exists")
    return ts

''' to fetch the timehseets by for the given date and employee id'''
@app.get("/all_timesheet/{by_date}/{emp_id}")
def read_emp(emp_id: int, by_date: date, db: Session = Depends(get_db)):
    ts_details = db.query(models.TimeSheet).filter(models.TimeSheet.employee_id==emp_id or models.TimeSheet.date == by_date).first()
    if ts_details is None:
        raise HTTPException(status_code= 404,  detail= "employee id and date doesn't exists")
    return ts_details        