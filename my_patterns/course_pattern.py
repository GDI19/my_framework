from copy import deepcopy
from my_patterns.behavior_patterns import Subject
from my_patterns.user_pattern import Student


# порождающий паттерн Прототип
class CoursePrototype:
    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()

# интерактивный курс
class InteractiveCourse(Course):
    pass

#
# курс в записи
class RecordCourse(Course):
    pass

# порождающий паттерн Фабричный метод
class CourseFactory:
    types = {'interactive': InteractiveCourse,
             'record': RecordCourse}

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class Category:
    auto_id = 0

    def __init__(self, name): # +? category
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        # self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        # if self.category:
        #     result += self.category.course_count()
        return result