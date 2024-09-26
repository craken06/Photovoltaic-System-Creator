from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def index(request):
    """The home page"""

    return render(request, 'index.html')