from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:777888777@localhost/database_mysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    price = db.Column(db.Float)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    quantity = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    # Получаем все товары из базы данных
    products = Products.query.all()
    return render_template('add_product.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])

    new_product = Products(name=name, description=description, price=price)
    db.session.add(new_product)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    # Находим товар в базе данных по его ID
    product = Products.query.get(product_id)
    if product:
        # Удаляем товар из базы данных
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)