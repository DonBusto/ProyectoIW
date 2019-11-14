from django.shortcuts import render
from .models import Usuario, Ropa, Marca
# Create your views here.
def index(request):
    return render(request, 'inditde/index.html')

def get_biggest_discount(request):
    ropas = Ropa.objects.all()
    n = len(ropas)
    for i in range(n):
        for j in range(0, n - i -1):
            if ropas[j].pvp - ropas[j].pfinal  > ropas[j+1].pvp - ropas[j+1].pfinal:
                ropas[j], ropas[j+1] = ropas[j+1], ropas[j]

    my_ropa = []
    for z in range(0, 5):
        my_ropa[z] = ropas[z]

    return HttpResponse(my_ropa)

#def get_all_categories(request):
    #ropas = Ropa.objects.all()
    #my_categorias = []
    #for i in ropas:
        #if ropas[i].categoria in my_categorias:
