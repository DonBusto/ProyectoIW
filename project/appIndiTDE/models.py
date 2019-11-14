from django.db import models
from django import forms
# Create your models here.

TEME_CHOICES = (('masculino', 'Masculino'), ('femenino', 'FEMENINO'), ('unisex', 'UNISEX'), )


class Marca(models.Model):
    id = models.CharField(max_length = 5, primary_key =True)
    nombre = models.CharField(max_length = 20)
    desc = models.TextField()
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
