from django.http import HttpResponse
from django.template import loader

from django.contrib.auth import logout

def homepage(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def user_logout(request):
    logout(request)
    print("logged out")
    print(request.user.is_authenticated)

    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def incorrect_user(request):
    template = loader.get_template('incorrect_user.html')
    return HttpResponse(template.render())