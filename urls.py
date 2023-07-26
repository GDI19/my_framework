from datetime import date
from views import *


# Front controller
def date_req(request):
    request['date'] = date.today()

def key_req(request):
    request['key'] = 'secret key'

fronts = [date_req, key_req]


# Page controller
routes = {
    '/': Index(),
    '/index/': Index(),
    '/contact/': Contact(),
    '/study_programs/': StudyPrograms(),
    '/courses_list/': CourseList(),
    '/create_course/': CreateCourse(),
    '/create_category/': CreateCategory(),
    '/category_list/': CategoryList(),
    '/copy_course/': CopyCourse()
    # '/page/': Page(),
    # '/another_page/': AnotherPage(),
    # '/examples/': Examples()
}