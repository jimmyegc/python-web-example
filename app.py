from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Cargar URI desde el entorno
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["crud_db"]
collection = db["items"]

@app.route('/')
def index():
    items = collection.find()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    if name:
        collection.insert_one({"name": name})
    return redirect('/')

@app.route('/delete/<item_id>')
def delete(item_id):
    from bson.objectid import ObjectId
    collection.delete_one({"_id": ObjectId(item_id)})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
