from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["crud_db"]
collection = db["items"]

@app.route('/')
def index():
    items = list(collection.find())
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        collection.insert_one({'nombre': nombre, 'descripcion': descripcion})
        return redirect(url_for('index'))
    return render_template('form.html')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_item(id):
    item = collection.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        collection.update_one({'_id': ObjectId(id)}, {'$set': {'nombre': nombre, 'descripcion': descripcion}})
        return redirect(url_for('index'))
    return render_template('form.html', item=item)

@app.route('/delete/<id>')
def delete_item(id):
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
