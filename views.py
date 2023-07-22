from framework.templator import render

menu_dict = {"Home": "/index",
             "Examples": "/examples",
             "Page": "/page",
             "Another Page": "another_page",
             "Contact Us": "/contact"}

class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None), title='Home', menu_dict=menu_dict)

class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', date=request.get('date', None), title='Contact Us', menu_dict=menu_dict)

class Page:
    def __call__(self, request):
        return '200 OK', render('page.html', date=request.get('date', None), title='Page', menu_dict=menu_dict)

class AnotherPage:
    def __call__(self, request):
        return '200 OK', render('another_page.html', date=request.get('date', None), title='Another Page', menu_dict=menu_dict)

class Examples:
    def __call__(self, request):
        return '200 OK', render('examples.html', date = request.get('date', None), title='Examples', menu_dict=menu_dict )
