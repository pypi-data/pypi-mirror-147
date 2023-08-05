from django.shortcuts import render
from django.conf import settings

def homepage(request):
    print(settings.FAVICON_URL)
    return render(
        request,
        'store/homepage.html'
    )