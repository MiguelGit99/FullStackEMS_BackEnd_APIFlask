from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    EMPLOYEE = "EMPLOYEE"
    
class Departments(str, Enum):
    ENGINEERING = "Engineering"
    HUMAN_RESOURCES = "Human Resources"
    MARKETING = "Marketing"
    SALES = "Sales"
    FINANCE = "Finance"
    OPERATIONS = "Operations"
    IT_SUPPORT = "IT Support"
    CUSTOMER_SUCCESS = "Customer Success"
    PRODUCT_MANAGEMENT = "Product Management"
    DESIGN = "Design"

class EmploymentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class AttendanceStatus(str, Enum):
    PRESENT = "Present"
    ABSENT = "Absent"
    LATE = "Late"

class DayType (str, Enum):
    FULL_DAY = "Full Day"
    THREE_QUARTER_DAY = "Three Quarter Day"
    HALF_DAY = "Half Day"
    SHORT_DAY = "Short Day"

class LeaveType(str, Enum):
    SICK = "Sick"
    CASUAL = "Casual"
    ANNUAL = "Annual"

class LeaveStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
