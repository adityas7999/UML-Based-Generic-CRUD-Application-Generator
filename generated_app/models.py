class Assignment:
    def __init__(self, id, assignmentId, description, dueDate, maxScore):
        self.id = id
        self.assignmentId = assignmentId
        self.description = description
        self.dueDate = dueDate
        self.maxScore = maxScore

    def to_dict(self):
        return {
            "id": self.id,
            "assignmentId": self.assignmentId,
            "description": self.description,
            "dueDate": self.dueDate,
            "maxScore": self.maxScore
        }
class Course:
    def __init__(self, id, courseCode, title, credits, status):
        self.id = id
        self.courseCode = courseCode
        self.title = title
        self.credits = credits
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "courseCode": self.courseCode,
            "title": self.title,
            "credits": self.credits,
            "status": self.status
        }
class Department:
    def __init__(self, id, deptId, name, buildingCode):
        self.id = id
        self.deptId = deptId
        self.name = name
        self.buildingCode = buildingCode

    def to_dict(self):
        return {
            "id": self.id,
            "deptId": self.deptId,
            "name": self.name,
            "buildingCode": self.buildingCode
        }
class Person:
    def __init__(self, id, firstName, lastName, email):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email
        }
class Professor:
    def __init__(self, id, title, salary):
        self.id = id
        self.title = title
        self.salary = salary

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "salary": self.salary
        }
class Student:
    def __init__(self, id, enrollmentDate, gpa):
        self.id = id
        self.enrollmentDate = enrollmentDate
        self.gpa = gpa

    def to_dict(self):
        return {
            "id": self.id,
            "enrollmentDate": self.enrollmentDate,
            "gpa": self.gpa
        }
class Submission:
    def __init__(self, id, submissionId, submissionDate, score, feedback):
        self.id = id
        self.submissionId = submissionId
        self.submissionDate = submissionDate
        self.score = score
        self.feedback = feedback

    def to_dict(self):
        return {
            "id": self.id,
            "submissionId": self.submissionId,
            "submissionDate": self.submissionDate,
            "score": self.score,
            "feedback": self.feedback
        }
