# API Attendance BackEnd
API. Serves a frontend web app to manage Login, Roles, Employees, Attendances, Leaves, Payslips and a Dashboard. 
Allows an ADMIN employee management (CRUD employees and different data visualization), and allows each employee to register its attendance every day and to request for a Leave. Also allows to get a Payslip receipt.

Reference: https://www.youtube.com/watch?v=dlu8PmKXopU&t=23229s


# APIFlask (http://localhost:5000/docs#)
API conectado a SQL Server con SQLAlchemy con las siguientes características: 
- Login usando cookies y JWT
- Uso de parametros de API en archivo .env* 

## Technologies
APIFlask (python), SQLAlchemy

### Techniques
* Blueprints (APIBlueprint)
* Route Error Handler
* Decorators
* Logging (concurrent log handler)
* Routes
* Pydantic Schemas
* SQLAlchemy Schemas (SQL Server BD)
* Bcrypt (encrypt passwords in BD)
* Flask Cors
* Flask JWT


### 3rd party components
* Pydantic
* concurrent-log-handler
* pytest