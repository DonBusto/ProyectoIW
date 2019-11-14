from django.shortcuts import render
from .models import Usuario, Ropa, Marca
# Create your views here.

def index(request):
	a = list(get_all_clothes())
	return render(request, 'inditde/index.html', {'my_ropa':  get_biggest_discount(a)})
	

def get_biggest_discount(ropas):
	n = len(ropas)
	for i in range(n):
		for j in range(0, n - i -1):
			if (ropas[j].pvp - ropas[j].pfinal  > ropas[j+1].pvp - ropas[j+1].pfinal):
				ropas[j], ropas[j+1] = ropas[j+1], ropas[j]
	
	if(n >= 5):
		my_ropa =[5]
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

#def get_all_categories(request):
    #ropas = Ropa.objects.all()
    #my_categorias = []
    #for i in ropas:
        #if ropas[i].categoria in my_categorias:
