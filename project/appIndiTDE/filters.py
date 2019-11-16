from .models import Ropa, Marca
import django_filters
from django import forms



class RopaFilter(django_filters.FilterSet):
    tipo = django_filters.CharFilter(lookup_expr='icontains')
    nombre= django_filters.CharFilter(lookup_expr='icontains')
    categoria = django_filters.CharFilter(lookup_expr='icontains')
    marca = django_filters.ModelMultipleChoiceFilter(queryset= Marca.objects.all() , widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Ropa
        fields = ['nombre','tipo', 'pfinal', 'categoria','genero', 'marca',]

    