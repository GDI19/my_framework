from datetime import date

from framework.templator import render
from my_patterns.behavior_patterns import CreateView, ListView, EmailNotifier, SmsNotifier
from my_patterns.log_pattern import Logger
from my_patterns.main_interface import Engine
from my_patterns.unit_of_work import UnitOfWork
from my_patterns.data_mappers import MapperRegistry
from framework.my_decorators import AppRoutes, Debug




site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

routes_dict = {}


@AppRoutes(routes=routes_dict, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories, title='Home')


@AppRoutes(routes=routes_dict, url='/index/')
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories, title='Home')


@AppRoutes(routes=routes_dict, url='/contact/')
class Contact:
    @Debug(name='Contact')
    def __call__(self, request):
        return '200 OK', render('contact.html', date=request.get('date', None), title='Contact Us')


@AppRoutes(routes=routes_dict, url='/study_programs/')
class StudyPrograms:
    @Debug(name='StudyPrograms')
    def __call__(self, request):
        return '200 OK', render('study_programs.html', date=date.today(), title='Study programs')


@AppRoutes(routes=routes_dict, url='/courses_list/')
class CourseList:
    @Debug(name='CourseList')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('courses_list.html',
                                    title='Courses List',
                                    objects_list=category.courses,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', render('courses_list.html',
                                    title='Courses List',
                                    err_message='No courses have been added yet')


@AppRoutes(routes=routes_dict, url='/create_course/')
class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
                site.courses.append(course)

            return '200 OK', render('courses_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', render('create_course.html',
                                    title='Create Course',
                                    err_message='No categories have been added yet')


@AppRoutes(routes=routes_dict, url='/create_category/')
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', title='Home', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)

@AppRoutes(routes=routes_dict, url='/category_list/')
class CategoryList:
    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', title='Categories List',
                                objects_list=site.categories)


@AppRoutes(routes=routes_dict, url='/copy_course/')
class CopyCourse:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('courses_list.html',
                                    objects_list=site.courses,
                                    name=new_course.category.name)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoutes(routes=routes_dict, url='/student-list/')
class StudentListView(ListView):
    # queryset = site.students
    template_name = 'student_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


@AppRoutes(routes=routes_dict, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoutes(routes=routes_dict, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)



class PageNotFound404:
    @Debug(name='PageNotFound404')
    def __call__(self, request):
        return '404 Upps', render('not_found404.html')



# @AppRoutes(routes=routes_dict, url='/api/')
# class CourseApi:
#     @Debug(name='CourseApi')
#     def __call__(self, request):
#         return '200 OK', BaseSerializer(site.courses).save()

