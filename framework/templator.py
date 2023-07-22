from jinja2 import Template
from os.path import join
from jinja2 import  FileSystemLoader
from jinja2.environment import Environment


TEMPLATE_FOLDER = 'templates'

def render(template_name, **kwargs):
    """
    Минимальный пример работы с шаблонизатором
    :param template_name: имя шаблона
    :param kwargs: параметры для передачи в шаблон
    :return:
    """
    # template_path = join(TEMPLATE_FOLDER, template_name)
    # print('template_path:', template_path)
    #
    # with open(template_path, encoding='utf-8') as f:
    #     template = Template(f.read())

    # создаем объект окружения
    env = Environment()
    # указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(TEMPLATE_FOLDER)
    # находим шаблон в окружении
    template = env.get_template(template_name)
    # рендерим шаблон с параметрами
    return template.render(**kwargs)

if __name__ == '__main__':
    # Пример использования
    # TEMPLATE_FOLDER = ''
    output_test = render('test_template.html', object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
    print(output_test)