from .models import Ropa, Marca
import django_filters
from django import forms



class RopaFilter(django_filters.FilterSet):
    tipo = django_filters.CharFilter(lookup_expr='icontains')
    marca = django_filters.ModelMultipleChoiceFilter(queryset= Marca.objects.all() , widget=forms.CheckboxSelectMultiple)
    a = {'marcas' : Marca.objects.all()}
    class Meta:
        model = Ropa
       
        fields = ['tipo', 'pfinal', 'categoria','genero', 'marca',]

    