class Course:
    def __init__(self, id, courseId, title):
        self.id = id
        self.courseId = courseId
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "courseId": self.courseId,
            "title": self.title
        }
class Department:
    def __init__(self, id, deptId, deptName):
        self.id = id
        self.deptId = deptId
        self.deptName = deptName

    def to_dict(self):
        return {
            "id": self.id,
            "deptId": self.deptId,
            "deptName": self.deptName
        }
class Enrollment:
    def __init__(self, id, enrollmentId, status):
        self.id = id
        self.enrollmentId = enrollmentId
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "enrollmentId": self.enrollmentId,
            "status": self.status
        }
class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
class Professor:
    def __init__(self, id, employeeId, specialization):
        self.id = id
        self.employeeId = employeeId
        self.specialization = specialization

    def to_dict(self):
        return {
            "id": self.id,
            "employeeId": self.employeeId,
            "specialization": self.specialization
        }
class Student:
    def __init__(self, id, rollNumber, enrollmentDate):
        self.id = id
        self.rollNumber = rollNumber
        self.enrollmentDate = enrollmentDate

    def to_dict(self):
        return {
            "id": self.id,
            "rollNumber": self.rollNumber,
            "enrollmentDate": self.enrollmentDate
        }
