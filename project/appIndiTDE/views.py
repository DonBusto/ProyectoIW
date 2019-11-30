from django.shortcuts import render, redirect
from .models import Usuario, Ropa, Marca, Sugerencia, Comentario
from django.core.mail import send_mail
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.conf import settings
from .filters import RopaFilter
from .forms import fSugerencia
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


def login(request):
    if request.method=="POST":
        username = request['username']
        password = request['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Usuario no valido')
            return redirect('/')

    else:
        return render(request, 'inditde/login.html')


def clothe(request, id_clothe):
    a = list(get_all_clothes())
    listaC = list(get_comments_by_clothe(get_all_comments(),Ropa.objects.get(id=id_clothe)))
    context = {
        'id': id_clothe,
        'listaRopa': list(get_all_clothes()),
        'prenda': Ropa.objects.get(id=id_clothe),
        'comentarios' : listaC,
        'avg' : get_average(listaC),
        'recuentoVals' : get_ratings_count(listaC),
        'marcas': get_all_brands(a),
        'id': id_clothe
    }
    return render(request, 'inditde/prenda.html', context)


def contact(request): 
    msg=""    
    if request.method == "POST":
        form = fSugerencia(request.POST)
        print(request.POST)
        print(form)
        print(form.errors)
        if form.is_valid():
            #post = form.save()
            su = Sugerencia()
            su.nombre = form.cleaned_data['nombre']
            su.titulo = form.cleaned_data['titulo']
            su.texto = form.cleaned_data['texto']
            #post.published_date = timezone.now()
            su.save()
            msg="Sugerencia enviada con éxito."
        else:
            msg="Error al enviar la sugerencia."
            
        temp_email = request.POST.get('email')
        to_email = [settings.EMAIL_HOST_USER, temp_email]
        
        if (temp_email != ""):
            strEmail = "Ahora estás suscrito a nuestra newsletter. Pronto recibirás noticias de nuestros productos."
            send_mail("Te has suscrito a nuestra newsletter", strEmail, settings.EMAIL_HOST_USER, to_email, fail_silently=False)
            msg=""
    a = list(get_sugerencias())
    form = fSugerencia()
    
    context = {
        'sugerencias': a,
        'form': form,
        'marcas': get_all_brands(get_all_clothes()),
        'mensage': msg,
        }
    return render(request, 'inditde/contact.html', context)




def brand(request, brand_name):
    brand = Marca.objects.get(nombre=brand_name)
    ropa = get_by_brand(list(get_all_clothes()), brand)
    context = {'my_ropa': ropa, 'marca': brand, 'marcas': get_all_brands(list(get_all_clothes()))}
    return render(request, 'inditde/marca.html', context)


def order_by_disccount(ropas):
    return sorted(ropas, key=lambda x: (x.pvp - x.pfinal), reverse=True)


def get_all_clothes():
    ropas = Ropa.objects.all()
    return ropas

def get_all_comments():
    comments = Comentario.objects.all()
    return comments

def get_sugerencias():
    sugerencias = Sugerencia.objects.all()
    return sugerencias


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

def get_ratings_count(comments):
    cinco = 0
    cuatro = 0
    tres = 0
    dos = 0
    uno = 0
    for i in comments:
        if(i.valoracion == 5):
            cinco += 1
        elif (i.valoracion == 4):
            cuatro += 1
        elif (i.valoracion == 3):
            tres += 1
        elif (i.valoracion == 2):
            dos += 1
        else:
            uno += 1
    vals = [cinco,cuatro,tres,dos,uno]
    return vals

def get_comments_by_clothe(comentarios, ropa):
    comments = []
    for i in comentarios:
        if (i.ropa.id == ropa.id):
            comments.append(i)
    return comments

def get_average(comentarios):
    suma = 0
    contador = 0
    for i in comentarios:
        suma += (i.valoracion)
        contador += 1
    if contador != 0:
        avg = float(suma / contador)
    else:
        avg = 0
    return avg

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
# def new_suggestion(request):
#        Sugerencia = Sugerencia()
#    return render(request, 'poner_url', {'Sugerencia': Sugerencia})
