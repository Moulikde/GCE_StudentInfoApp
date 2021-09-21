#import dependencies
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.responses import Response

#Initialize FastAPI, template folders and static elements
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates/static"), name='static')


#finds the index.html in extend.html
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("extends/extend.html", {
        "request": request,
    })


#finds the enterDetails.html in extend_2.html
@app.get("/enterDetails")
def home(request: Request):
    return templates.TemplateResponse("extends/extend_2.html", {"request": request})


#finds the searchDetails.html in extend_3.html
@app.get("/searchDetails")
def home(request: Request):
    return templates.TemplateResponse("extends/extend_3.html", {"request": request})


#finds the allStudentsDetails.html in extend_4.html
@app.get("/allStudentsDetails")
def home(request: Request):
    return templates.TemplateResponse("extends/extend_4.html", {"request": request})


#inserts form data into MySQL Cloud DB finds the insert_success.html in extend_5.html
@app.post(path='/create')
def create_record(request: Request,sid: str = Form(...), name: str = Form(...),last_name: str = Form (...), email: str = Form(...),
                   add: str = Form(...), gpa: str = Form(...)):
    import mysql.connector
    cnx = mysql.connector.connect(user='root', host='35.193.76.49', database='StudentInfo', password='12345')
    cursor = cnx.cursor()
    query = "INSERT INTO `StudentInfo`.`Student` (`StudentId`, `FirstName`, `LastName`, `Email`, `Address`, `GPA`) VALUES ('%s', '%s','%s','%s','%s','%s');"%(sid ,name ,last_name ,email ,add ,gpa)
    print(query)
    if query is None:
        raise HTTPException(status_code=23000, detail="Student ID or email already exists, please check what you've "
                                                    "entered and retry or contact Administrator.")
    else:

        cursor.execute(query)
        cnx.commit()
        cursor.close()
        return templates.TemplateResponse("extends/extend_5.html", {"request": request})

@app.get(path='/searchstudent')
def fetch_all(request: Request):
    return templates.TemplateResponse("extends/extend_7.html", {"request": request})

#Searches Studentid, first name or last name iin DB and returns Json Array, if not found returns the mentioned string.
@app.get(path='/search')
def search_record(request:Request, StudentId: str, fname: str, lname: str):
    print(lname)
    import mysql.connector
    cnx = mysql.connector.connect(user='root', host='35.193.76.49', database='StudentInfo', password='12345')
    cursor = cnx.cursor()

    if lname == '':
        query = " Select * from `StudentInfo`.`Student` where StudentId = '%s' and FirstName = '%s';"%(StudentId, fname)
    else:
        query = " Select * from `StudentInfo`.`Student` where StudentId = '%s' and LastName = '%s';"%(StudentId, lname)
    print(query)
    cursor.execute(query)
    data = cursor.fetchone()
    print(data)
    if data is None:
        return templates.TemplateResponse("extends/extend_6.html", {"request": request})
    return data

@app.get(path='/all')
def fetch_all(request: Request):
    return templates.TemplateResponse("extends/extend_4.html", {"request": request})

#Returns json array of all the students in the DB
@app.get(path='/checkdatabase')
def fetch_all(request: Request):
    import mysql.connector
    cnx = mysql.connector.connect(user='root', host='35.193.76.49', database='StudentInfo', password='12345')
    cursor = cnx.cursor()
    query = 'Select * from `StudentInfo`.`Student`;'
    cursor.execute(query)
    data = cursor.fetchall()
    return data

#http://127.0.0.1:8000/
