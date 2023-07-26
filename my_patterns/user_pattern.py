

class User:
    pass


class Teacher(User):
    pass

class Student(User):
    pass


# порождающий паттерн Фабричный метод
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()