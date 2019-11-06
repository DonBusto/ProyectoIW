from django.shortcuts import render
from .models import Usuario, Ropa, Marca
# Create your views here.
def index(request):
    return render(request, 'index.html')
