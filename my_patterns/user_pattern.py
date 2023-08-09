# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name

class Teacher(User):
    pass

class Student(User):
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