from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = "49617833-17b6310e26005e88c7f20f06f"
PIXABAY_URL = "https://pixabay.com/api/"

@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('query', '')
    order = request.args.get('order', 'popular')  # Valor por defecto "popular"
    page = int(request.args.get('page', 1))
    images = []
    total_pages = 1  # La API Cambia el valor o devuelve 1 si no hay resultados
    current_page = 1 #--------------------------------------
    

    if query:
        response = requests.get(PIXABAY_URL, params={
            "key": API_KEY,
            "q": query,
            "image_type": "photo",
            "page": page,
            "per_page": 30,
            "lang": "es",
            "order": order  # Agregamos el parámetro de ordenamiento
            })
        data = response.json()
        images = data.get("hits", [])
        total = data.get("totalHits", 0)
        total_pages = (total // 30) + (1 if total % 30 > 0 else 0)

    # Asegura que la pagina actual no supere el total de paginas
    page = min(page, total_pages)

    # Lógica de paginación
    page_range = 2  # Cantidad de paginas atras y adelabo de la pagina actual
    pagination = []

    # Página inicial
    pagination.append(1)

    # Páginas antes y después de la página actual
    for i in range(page - page_range, page + page_range + 1):
        if i > 1 and i < total_pages:
            pagination.append(i)

    # Páginas finales
    if total_pages > 1:
        pagination.append(total_pages)

    # Eliminar duplicados y ordenar
    pagination = sorted(set(pagination))

    # Agregar los puntos suspensivos si es necesario
    if len(pagination) > 1 and pagination[1] > 2:
        pagination.insert(1, '...')
    if len(pagination) > 2 and pagination[-2] < total_pages - 1:
        pagination.insert(-1, '...')

    # Si no hay imágenes, no mostrar la paginación
    show_pagination = len(images) > 0 or query == '' 

    return render_template('index.html', images=images, query=query, order=order, page=page, total_pages=total_pages, pagination=pagination, show_pagination=show_pagination)

def handler(event, context):
return app(event, context)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
