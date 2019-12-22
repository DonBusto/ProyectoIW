from django.db import models
from django import forms
from django.contrib.auth.models import User
# Create your models here.

TEME_CHOICES = (('masculino', 'Masculino'), ('femenino', 'FEMENINO'), ('unisex', 'UNISEX'), )

class Carro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ropa = models.ForeignKey('Ropa', on_delete=models.CASCADE)

class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ropa = models.ForeignKey('Ropa', on_delete=models.CASCADE)
    
class Marca(models.Model):
    id = models.CharField(max_length = 5, primary_key =True)
    nombre = models.CharField(max_length = 20)
    desc = models.TextField()
    descEn = models.TextField()
    logo = models.ImageField()


    def __str__(self):
        return self.nombre


class Ropa(models.Model):
    id = models.CharField(max_length = 10, primary_key =True)
    nombre = models.CharField(max_length = 30)
    tipo = models.CharField(max_length = 120)
    pvp = models.DecimalField(max_digits = 7, decimal_places = 2)
    pfinal = models.DecimalField(max_digits = 7, decimal_places = 2, default = pvp)
    categoria = models.CharField(max_length = 120)
    genero = models.CharField(max_length = 10, choices = TEME_CHOICES, default = 'unisex')
    desc = models.TextField()
    img = models.ImageField()
    marca = models.ForeignKey('Marca', on_delete = models.CASCADE)
    cantidad = models.IntegerField(default = 1)


    """docstring for Ropa."""
    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    nombre = models.CharField(max_length = 20)
    contrasenya = models.CharField(max_length = 20)
    carro = models.ManyToManyField('appIndiTDE.Ropa')
    lista_deseo = models.ManyToManyField('appIndiTDE.Ropa', related_name = 'lista_deseo')
    tarjeta_credito = models.IntegerField()

    def __str__(self):
        return self.nombre

class Sugerencia(models.Model):
    nombre = models.CharField(max_length = 20, default="anonymous")
    titulo = models.CharField(max_length = 30)
    texto = models.CharField(max_length = 240)

    def __str__(self):
        return self.nombre

class Comentario(models.Model):
    id = models.CharField(max_length = 10, primary_key =True)
    usuario = models.ForeignKey('Usuario', on_delete = models.CASCADE)
    ropa = models.ForeignKey('Ropa', on_delete = models.CASCADE)
    texto = models.CharField(max_length = 240)
    valoracion = models.IntegerField()

    def __str__(self):
        return self.texto

class Review(models.Model):
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    ropa = models.ForeignKey('Ropa', on_delete = models.CASCADE)
    texto = models.CharField(max_length = 240)
    valoracion = models.IntegerField()

    def __str__(self):
        return self.texto
