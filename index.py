from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Toma la API_KEY desde las variables de entorno
API_KEY = os.environ.get("API_KEY")  
PIXABAY_URL = "https://pixabay.com/api/"

@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('query', '')
    order = request.args.get('order', 'popular')  
    page = int(request.args.get('page', 1))
    images = []
    total_pages = 1  

    if query:
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

    page = min(page, total_pages)

    page_range = 2  
    pagination = [1]

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

# Ejecuta el servidor solo en desarrollo
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
