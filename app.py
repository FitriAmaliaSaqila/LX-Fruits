import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    fruit = list(db.fruit.find({}))
    return render_template("dashboard.html", fruit=fruit)

@app.route('/fruit', methods=['GET', 'POST'])
def fruit():
    fruit = list(db.fruit.find({}))
    return render_template("index.html", fruit=fruit)

@app.route('/addfruit', methods=['GET', 'POST'])
def addFruit():
    if request.method == 'POST':
        nama = request.form['fruitsName']
        harga = request.form['price']
        deskripsi = request.form['descriptionProduct']
        nama_gambar = request.files['image']

        if nama_gambar :
            nama_file_asli = nama_gambar.filename
            nama_file_gambar = nama_file_asli.split('/')[-1]
            file_path = f'static/assets/imgFruit/{nama_file_gambar}'
            nama_gambar.save(file_path)
        else :
            nama_gambar = None
        
        doc = {
            'nama': nama,
            'harga': harga,
            'gambar': nama_file_gambar,
            'deskripsi': deskripsi
        }

        db.fruit.insert_one(doc)
        return redirect(url_for('fruit'))
    return render_template("AddFruit.html")

@app.route('/edit/<_id>', methods=['GET', 'POST'])
def edit(_id):
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['edit_fruitsName']
        harga = request.form['edit_price']
        deskripsi = request.form['edit_descriptionProduct']
        nama_gambar = request.files['edit_image']

        doc = {
            'nama': nama,
            'harga': harga,
            'deskripsi': deskripsi
        }

        if nama_gambar :
            nama_file_asli = nama_gambar.filename
            nama_file_gambar = nama_file_asli.split('/')[-1]
            file_path = f'static/assets/imgFruit/{nama_file_gambar}'
            nama_gambar.save(file_path)
            doc['gambar'] = nama_file_gambar

        db.fruit.update_one({'_id': ObjectId(id)}, {'$set': doc})
        return redirect(url_for('fruit'))
    
    id = ObjectId(_id)
    data = list(db.fruit.find({'_id': id}))
    print(data)
    return render_template("EditFruit.html", data=data)

@app.route('/delete/<_id>', methods=['GET', 'POST'])
def delete(_id):
    db.fruit.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('fruit'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)