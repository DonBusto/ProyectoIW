from django.shortcuts import render, redirect
from .models import Usuario, Ropa, Marca, Sugerencia, Comentario, Carro, Favorito, Review
from django.core.mail import send_mail
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.conf import settings
from .filters import RopaFilter
from .forms import fSugerencia
from appIndiTDE.serializers import RopaSerializer, FavoritoSerializer
from rest_framework import viewsets
import logging


# Create your views here.

class RopaViewSet(viewsets.ModelViewSet):
    queryset = Ropa.objects.all()
    serializer_class = RopaSerializer

class FavoritosViewSet(viewsets.ModelViewSet):
    queryset = Favorito.objects.all()
    serializer_class = FavoritoSerializer

def index(request):
    a = list(get_all_clothes())
    c = list(get_carro_completo())
    masculino = get_by_genre(a, 'masculino')
    femenino = get_by_genre(a, 'femenino')
    unisex = get_by_genre(a, 'unisex')
    context = {
        'my_ropa': order_by_disccount(a),
        'marcas': get_all_brands(a),
        'my_ropa_masculino': order_by_disccount(masculino),
        'my_ropa_femenino': order_by_disccount(femenino),
        'my_ropa_unisex': order_by_disccount(unisex),
    }
    if request.user.is_authenticated:
        user = request.user
        context['user'] = user
        context['carro'] = get_clothes_by_user(c, user)

    return render(request, 'inditde/index.html', context)

def cart(request):

    if request.user.is_authenticated:
        user = request.user

        if request.method == 'POST':
            carroRopaID = request.POST.get('ropaEliminar')
            carro = Carro.objects.filter(id = carroRopaID)
            carro.delete()

        c = list(get_carro_completo())
        a = list(get_all_clothes())
        context = {
            'carro' : get_cantidades_ropa(c, user),
            'marcas': get_all_brands(a),
            'total' : get_total(get_clothes_by_user(c, user))
        }
        return render(request, 'inditde/cart.html', context)


    else:
        return redirect('index')

def favourites(request):
    if request.user.is_authenticated:
        user = request.user
        f = list(get_favoritos_completo())
        a = list(get_all_clothes())
        context = {
            'favoritos' : get_cantidades_ropa_favoritos(f, user),
            'marcas': get_all_brands(a),
            'usuario': user

        }
        return render(request, 'inditde/favourites.html', context)
    else:
        return redirect('index')

def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        c = list(get_carro_completo())
        a = list(get_all_clothes())
        context = {
            'carro' : get_cantidades_ropa(c, user),
            'marcas': get_all_brands(a),
            'total' : get_total(get_clothes_by_user(c, user))
        }
        return render(request, 'inditde/checkout.html', context)
    else:
        return redirect('index')

def register(request):
    print(request)
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
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Error en la creación de usuario: Este usuario ya existe')
            return render(request, 'inditde/register.html')
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Error en la creación de usuario: Este usuario ya existe.')
            return render(request, 'inditde/register.html', context)
        else:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                            last_name=last_name)
            user.save()
            messages.info(request, 'Usuario creado')
            return redirect('index')
    else:
        return render(request, 'inditde/register.html', context)


def logout(request):
    auth.logout(request)
    return render(request, 'inditde/index.html')


def login(request):
    a = list(get_all_clothes())
    masculino = get_by_genre(a, 'masculino')
    femenino = get_by_genre(a, 'femenino')
    unisex = get_by_genre(a, 'unisex')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        request.session['username'] = username
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            context = {
                'username': username,
                'carro': get_clothes_by_user(list(Carro.objects.all()), user),
                'my_ropa': order_by_disccount(a),
                'marcas': get_all_brands(a),
                'my_ropa_masculino': order_by_disccount(masculino),
                'my_ropa_femenino': order_by_disccount(femenino),
                'my_ropa_unisex': order_by_disccount(unisex),
                'user': user,
            }
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Usuario no valido')
            return render(request, 'inditde/login.html')

    else:
        return render(request, 'inditde/login.html')


def clothe(request, id_clothe):
    if request.user.is_authenticated:
        user = request.user
    if request.method == 'POST':
        id = request.POST.get('ropaCarro')
        ids = id.split("-")
        if ids[1] == "c":
            item = Ropa.objects.get(id=ids[0])
            newItem = Carro.objects.create(usuario=request.user, ropa=item)
            newItem.save()
        if ids[1] == "s":
            item = Ropa.objects.get(id=ids[0])
            valo = request.POST.get('message')
            rating = request.POST.get('rating')
            newComment = Review.objects.create(usuario=request.user, ropa=item, texto=valo, valoracion=rating)
            newComment.save()

    a = list(get_all_clothes())
    c = list(get_carro_completo())
    listaR = list(get_reviews_by_clothe(get_all_reviews(), Ropa.objects.get(id=id_clothe)))
    context = {
        'id': int(id_clothe),
        'listaRopa': list(get_all_clothes()),
        'prenda': Ropa.objects.get(id=id_clothe),
        'reviews': listaR,
        'avg': get_average(listaR),
        'recuentoVals': get_ratings_count(listaR),
        'marcas': get_all_brands(a),
        'id': id_clothe
    }

    return render(request, 'inditde/prenda.html', context)



def contact(request):
    msg = ""
    b = list(get_all_clothes())
    c = list(get_carro_completo())
    if request.method == "POST":
        form = fSugerencia(request.POST)
        print(request.POST)
        print(form)
        print(form.errors)
        if form.is_valid():
            # post = form.save()
            su = Sugerencia()
            su.nombre = form.cleaned_data['nombre']
            su.titulo = form.cleaned_data['titulo']
            su.texto = form.cleaned_data['texto']
            # post.published_date = timezone.now()
            su.save()
            msg = "Sugerencia enviada con éxito."
        else:
            msg = "Error al enviar la sugerencia."

        temp_email = request.POST.get('email')
        to_email = [settings.EMAIL_HOST_USER, temp_email]

        if (temp_email != ""):
            strEmail = "Ahora estás suscrito a nuestra newsletter. Pronto recibirás noticias de nuestros productos."
            send_mail("Te has suscrito a nuestra newsletter", strEmail, settings.EMAIL_HOST_USER, to_email,
                      fail_silently=False)
            msg = ""
    a = list(get_sugerencias())
    form = fSugerencia()

    context = {
        'sugerencias': a,
        'form': form,
        'marcas': get_all_brands(b),
        'mensage': msg,

    }
    if request.user.is_authenticated:
        user = request.user
        context['user'] = user
        context['carro'] = get_clothes_by_user(c, user)
    return render(request, 'inditde/contact.html', context)


def brand(request, brand_name):
    c = list(get_carro_completo())
    brand = Marca.objects.get(nombre=brand_name)
    ropa = get_by_brand(list(get_all_clothes()), brand)
    context = {'my_ropa': ropa, 'marca': brand, 'marcas': get_all_brands(list(get_all_clothes()))}
    if request.user.is_authenticated:
        user = request.user
        context['user'] = user
        context['carro'] = get_clothes_by_user(c, user)
    return render(request, 'inditde/marca.html', context)

def brand_eng(request, brand_name):
    c = list(get_carro_completo())
    brand = Marca.objects.get(nombre=brand_name)
    ropa = get_by_brand(list(get_all_clothes()), brand)
    context = {'my_ropa': ropa, 'marca': brand, 'marcas': get_all_brands(list(get_all_clothes()))}
    if request.user.is_authenticated:
        user = request.user
        context['user'] = user
        context['carro'] = get_clothes_by_user(c, user)
    return render(request, 'inditde/marcaen.html', context)


def order_by_disccount(ropas):
    return sorted(ropas, key=lambda x: (x.pvp - x.pfinal), reverse=True)


def get_all_clothes():
    ropas = Ropa.objects.all()
    return ropas


def get_carro_completo():
    carro = Carro.objects.all()
    return carro

def get_favoritos_completo():
    fav = Favorito.objects.all()
    return fav

def get_all_reviews():
    reviews = Review.objects.all()
    return reviews


def get_sugerencias():
    sugerencias = Sugerencia.objects.all()
    return sugerencias


def category(request):
    c = list(get_carro_completo())
    filtro = RopaFilter(request.GET, queryset=get_all_clothes())
    context = {'marcas': get_all_brands(get_all_clothes()), 'filter': filtro}
    if request.user.is_authenticated:
        user = request.user
        context['user'] = user
        context['carro'] = get_clothes_by_user(c, user)
    if request.method == 'POST':
        id = request.POST.get('ropaCarro')
        ids = id.split("-")
        if ids[1] == "c":
            item = Ropa.objects.get(id=ids[0])
            newItem = Carro.objects.create(usuario=request.user, ropa=item)
            newItem.save()
        if ids[1] == "f":
            item = Ropa.objects.get(id=ids[0])
            newItem = Favorito.objects.create(usuario=request.user, ropa=item)
            newItem.save()
            print("Fav guardado")
        return redirect('category')

    return render(request, 'inditde/category.html', context)


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


def get_clothes_by_user(carro, user):
    my_carro = []
    for i in carro:
        if (i.usuario == user):
            my_carro.append(i)
    return my_carro

def get_cantidades_ropa(carro, user):
    my_carro = []
    for i in carro:
        if (i.usuario == user):
            if(len(my_carro) >= 1):
                c = any(x.ropa.nombre == i.ropa.nombre for x in my_carro)
                if c:
                    for x in my_carro:
                        if x.ropa.nombre == i.ropa.nombre:
                            x.ropa.cantidad = x.ropa.cantidad + 1
                else:
                    i.ropa.cantidad = 1
                    my_carro.append(i)

            else:
                i.ropa.cantidad = 1
                my_carro.append(i)
    return my_carro

def get_favourites_by_user(favoritos, user):
    my_favourites = []
    for i in favoritos:
        if (i.usuario == user):
            my_favourites.append(i)
    return my_favourites

def get_cantidades_ropa_favoritos(favoritos, user):
    my_favourites = []
    for i in favoritos:
        if (i.usuario == user):
            if(len(my_favourites) >= 1):
                c = any(x.ropa.nombre == i.ropa.nombre for x in my_favourites)
                if c:
                    for x in my_favourites:
                        if x.ropa.nombre == i.ropa.nombre:
                            x.ropa.cantidad = x.ropa.cantidad + 1
                else:
                    i.ropa.cantidad = 1
                    my_favourites.append(i)

            else:
                i.ropa.cantidad = 1
                my_favourites.append(i)
    return my_favourites

def get_total(carro):
    suma = 0
    for i in carro:
        suma += i.ropa.pfinal
    return suma


def get_ratings_count(comments):
    cinco = 0
    cuatro = 0
    tres = 0
    dos = 0
    uno = 0
    for i in comments:
        if (i.valoracion == 5):
            cinco += 1
        elif (i.valoracion == 4):
            cuatro += 1
        elif (i.valoracion == 3):
            tres += 1
        elif (i.valoracion == 2):
            dos += 1
        else:
            uno += 1
    vals = [cinco, cuatro, tres, dos, uno]
    return vals


def get_reviews_by_clothe(reviews, ropa):
    revieews = []
    for i in reviews:
        if (i.ropa.id == ropa.id):
            revieews.append(i)
    return revieews


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
