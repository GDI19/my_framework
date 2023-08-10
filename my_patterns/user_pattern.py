from my_patterns.unit_of_work import DomainObject


# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name

class Teacher(User):
    pass

class Student(User, DomainObject):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)

# порождающий паттерн Фабричный метод
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)