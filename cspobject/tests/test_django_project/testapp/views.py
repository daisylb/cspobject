from django.http import HttpResponse

def basic_view(request):
    return HttpResponse("Hello!")
