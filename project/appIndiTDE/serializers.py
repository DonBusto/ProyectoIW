from appIndiTDE.models import Ropa, Favorito
from rest_framework import serializers


# Serializers define the API representation.
class RopaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ropa
        fields = ['id', 'nombre', 'tipo', 'pvp', 'pfinal', 'categoria', 'genero', 'desc', 'img', 'marca', 'cantidad']

class FavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorito
        fields = ['id', 'usuario', 'ropa']
        depth = 1
