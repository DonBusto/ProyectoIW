from django.shortcuts import render
from .models import Usuario, Ropa, Marca
from .filters import RopaFilter
import logging


# Create your views here.

def index(request):
    a = list(get_all_clothes())

    masculino = get_by_genre(a, 'masculino')
    femenino = get_by_genre(a, 'femenino')
    unisex = get_by_genre(a, 'unisex')

    context = {'my_ropa': order_by_disccount(a),
               'marcas': get_all_brands(a),
               'my_ropa_masculino': order_by_disccount(masculino),
               'my_ropa_femenino': order_by_disccount(femenino),
               'my_ropa_unisex': order_by_disccount(unisex),
               }
    return render(request, 'inditde/index.html', context)


def clothe(request, id_clothe):
    a = list(get_all_clothes())
    context = {
            'id': id_clothe,
            'listaRopa' : list(get_all_clothes()),
            'prenda' : Ropa.objects.get(id=id_clothe),
            'marcas': get_all_brands(a),
            'id': id_clothe
        }
    return render(request, 'inditde/single-product.html', context)


def brand(request, brand_name):
    brand = Marca.objects.get(nombre=brand_name)
    ropa = get_by_brand(list(get_all_clothes()), brand)
    context = {'my_ropa': ropa, 'marca': brand, 'marcas': get_all_brands(list(get_all_clothes()))}
    return render(request, 'inditde/single-blog.html', context)


def order_by_disccount(ropas):
    return sorted(ropas, key=lambda x: (x.pvp - x.pfinal), reverse=True)


def get_all_clothes():
    ropas = Ropa.objects.all()
    return ropas

def category(request):
    filtro = RopaFilter(request.GET, queryset=  get_all_clothes())
    return render(request, 'inditde/category.html', {'marcas': get_all_brands( get_all_clothes()),'filter':filtro})
    
def get_all_categories(ropas):
    my_categorias = []
    for i in ropas:
        print(i.nombre)
        if i.categoria not in my_categorias:
            print(i.categoria)
            my_categorias.append(i.categoria)
    return my_categorias


def get_all_brands(ropas):
    my_brands = []
    for i in ropas:
        if i.marca not in my_brands:
            my_brands.append(i.marca)
    return my_brands


def get_by_genre(ropas, genero):
    my_ropa = []
    for i in ropas:
        if (i.genero == genero):
            my_ropa.append(i)
    return my_ropa


def get_by_brand(ropas, marca):
    my_ropa = []
    for i in ropas:
        if (i.marca.nombre == marca.nombre):
            my_ropa.append(i)
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
#def new_suggestion(request):
#        Sugerencia = Sugerencia()
#    return render(request, 'poner_url', {'Sugerencia': Sugerencia})
