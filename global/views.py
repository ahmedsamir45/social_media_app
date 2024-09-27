from django.shortcuts import render

from django.contrib import messages

# In your view where you want to redirect after logout
def landing(request):
    return render(request, 'global/index.html')


def about(request):
    return render(request, 'global/about.html')

def contact(request):
    return render(request, 'global/contact.html')

# views.py
from django.shortcuts import render

def handler404(request, exception):
    return render(request, 'global/404.html', status=404)

def handler500(request):
    return render(request, 'global/500.html', status=500)
