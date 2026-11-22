def get_app_info():
    return {
        "app_name": "Student Management API",
        "version": "1.0.0"
    }

def get_student_not_found():
    return {
        "error": "Student not found",
        "message": "The requested student does not exist."
    }

class StudentNotFoundException(Exception):
    pass