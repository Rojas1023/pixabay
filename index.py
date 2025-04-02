import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Obtener la API Key de las variables de entorno en Vercel
API_KEY = os.getenv("API_KEY")
PIXABAY_URL = "https://pixabay.com/api/"

@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('query', '')
    order = request.args.get('order', 'popular')
    page = int(request.args.get('page', 1))
    images = []
    total_pages = 1  

    if query:
        try:
            response = requests.get(PIXABAY_URL, params={
                "key": API_KEY,
                "q": query,
                "image_type": "photo",
                "page": page,
                "per_page": 30,
                "lang": "es",
                "order": order
            })
            data = response.json()
            images = data.get("hits", [])
            total = data.get("totalHits", 0)
            total_pages = (total // 30) + (1 if total % 30 > 0 else 0)
        except Exception as e:
            print(f"Error en la API de Pixabay: {e}")

    page = min(page, total_pages)

    # Paginación
    page_range = 2  
    pagination = []

    pagination.append(1)
    for i in range(page - page_range, page + page_range + 1):
        if i > 1 and i < total_pages:
            pagination.append(i)
    if total_pages > 1:
        pagination.append(total_pages)

    pagination = sorted(set(pagination))
    if len(pagination) > 1 and pagination[1] > 2:
        pagination.insert(1, '...')
    if len(pagination) > 2 and pagination[-2] < total_pages - 1:
        pagination.insert(-1, '...')

    show_pagination = len(images) > 0 or query == ''

    return render_template('index.html', images=images, query=query, order=order, page=page, total_pages=total_pages, pagination=pagination, show_pagination=show_pagination)

# Vercel necesita este handler
def handler(event, context):
    return app.wsgi_app(event, context)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
