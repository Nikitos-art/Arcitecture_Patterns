
from wsgiref.simple_server import make_server
from framework.my_framework import Framework
#from urls import routes, fronts
from views import routes


#application = Framework(routes, fronts)
application = Framework(routes)

with make_server('', 8080, application) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()
