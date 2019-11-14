from django.shortcuts import render
from .models import Usuario, Ropa, Marca


# Create your views here.

def index(request):
    a = list(get_all_clothes())
    context = {
        'my_ropa': get_biggest_discount(a)
    }
    return render(request, 'inditde/index.html', context)


def get_biggest_discount(ropas):
    n = len(ropas)
    for i in range(n):
        for j in range(0, n - i - 1):
            if (ropas[j].pvp - ropas[j].pfinal > ropas[j + 1].pvp - ropas[j + 1].pfinal):
                ropas[j], ropas[j + 1] = ropas[j + 1], ropas[j]

    if (n >= 5):
        my_ropa = [5]
        for z in range(0, 5):
            my_ropa.append(ropas[z])
    else:
        my_ropa = [n]
        for x in range(0, n):
            my_ropa.append(ropas[x])
    return my_ropa


def get_all_clothes():
    ropas = Ropa.objects.all()
    return ropas


def get_all_categories(ropas):
    my_categorias = []
    for i in ropas:
        if ropas[i].categoria not in my_categorias:
            my_categorias.append(ropas[i].categoria)
    return my_categorias


def get_all_brands(ropas):
    my_brands = []
    for i in ropas:
        if ropas[i].marca not in my_brands:
            my_categorias.append(ropas[i].marca)
    return my_brands


def get_by_genre(ropas, genero):
    my_ropa = []
    for i in ropas:
        if (ropas[i].genero == genero):
            my_ropa.append(ropas[i])
    return my_ropa


def get_by_brand(ropas, marca):
    my_ropa = []
    for i in ropas:
        if (ropas[i].marca == marca):
            my_ropa.append(ropas[i])
    return my_ropa


def get_by_type(ropas, tipo):
    my_ropa = []
    for i in ropas:
        if (ropas[i].tipo == tipo):
            my_ropa.append(ropas[i])
    return my_ropa


def get_by_priceRange(ropas, min, max):
    my_ropa = []
    for i in ropas:
        if (ropas[i].pfinal >= min and ropas[i].pfinal <= max):
            my_ropa.append(ropas[i])
    return my_ropa
