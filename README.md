# Requisitos entrega ProyectoIW

Descripción
El proyecto "IndiTDE" deberá implementar un sitio web en el que se muestren diferentes ofertas de ropa de todas las marcas propiedad 
de la empresa, clasificados por marcas (P&B, Bershka, Zara, etc.) y por categorías (Sudaderas, Chaquetas, Camisetas, etc.), pudiendo 
una misma prenda estar en varias categorías. También se podrán ver los detalles de cada marca y de cada categoría, incluida la lista 
de ofertas de ropa asociadas en cada caso.

[E2] Funcionalidades básicas (2,5 puntos)

Personalización de una plantilla (estructura de varios niveles) y sus estilos. 

Visualizar la portada de "IndiTDE", mostrando dos ofertas de ropa de cada marca (p.ej. las más baratas o el criterio que queráis).

Visualizar los detalles de una marca, incluida la lista asociada de ofertas de prendas.

Visualizar los detalles de una categoría, incluida la lista asociada de ofertas de ropa.

Visualizar los detalles de una oferta de ropa concreta, incluido el nombre de la marca y la lista de categorías asociadas

# How to run
Para poder ejecutar el manage.py se puede hacer:
* virtualenv piw 
o:
* pip install requirements.txt

# IndiTDE:
(Página basada en plantilla winter: https://colorlib.com/wp/template/winter/)

Página base:
	Estructura por capas.
	El apartado marcas se despliega y muestra todas las marcas con las que trabajamos, al hacer click en alguna lleva a la información de esta.
	En la parte superior se pueden buscar artículos por su nombre.
	Carga de animaciones y efectos
	Footer con imagenes de varias marcas y su redirección a su instagram
	Todas las categorias, marcas y dirección de contacto.
	Al estar en la página contacto aparecerá en el footer la posibilidad de meter tu email para suscribirse al envío de la newsletter
	
	
Página Index:
	Al hacer click en mujer, hombre o unisex, redirige a la página Tienda filtrando los resultados por el genero elegido.
	En el apartado top ofertas saldrán las 4 ofertas que tengan mayor descuento en €.
	Animaciones y eventos reutilizados y añadidos los del apartado de top ofertas para que solo aparezcan las 4 del genero elegido.
	Al hacer click en el titulo de cualquier prenda te llevara a la pagina de su descripción.

Página Tienda:
	Hemos reutilizado ciertas funciones y otras las hemos redefinido.
	Por defecto se muestran 6 prendas y dandole a mostrar más se verán todas, dando a mostrar menos se volverán a ver solo 6.
	Hemos usado filters.py
	Se puede filtrar por categoría "formal, deporte, ...", marcas y/o género. Al dar a buscar se efectuará el filtrado.
	Al hacer click en el titulo del artículo lleva a su descripción.
	
Página Prenda:
	Muestra el artículo y toda su información.
	La marca redirige a la información de la marca
	El apartado opiniones solo muestra las opiniones metidas desde /admin/ puesto que para esta entrega no se pide tanto.
	Aparecen las especificaciones y la descripción correspondiente al artículo.

Página Marca:
	Imagen de la marca, nombre, titulo y descripción.
	Y todas las ropas de la marca.

Página Contacto:
	Se muestran todas las sugerencias dejadas por las personas.
	Buzón de sugerencias para poder dejar sugerencias mediante form.
	En el footer aparece un apartado para meter tu correo para suscribirse a la newsletter, se te enviará un correo de confirmación de que el correo ha sido recibido.
