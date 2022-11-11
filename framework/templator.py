###########OLD IMPORTS###########################
# from jinja2 import Template
# from os.path import join

from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    env = Environment()
    # indicating the folder for template search
    env.loader = FileSystemLoader(folder)
    # finding template in environment
    template = env.get_template(template_name)
    return template.render(**kwargs)


#########################OLD RENDERER#############################################
# def render(template_name, folder='templatez', **kwargs):
#     """
#     :param template_name: template name
#     :param folder: folder where to look for template
#     :param kwargs: parameters
#     :return:
#     """
#     file_path = join(folder, template_name)
#     # Open template using its name
#     with open(file_path, encoding='utf-8') as f:
#         # Reading it
#         template = Template(f.read())
#     # Rendering template with parameters
#     return template.render(**kwargs)
