from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'aishu@123'

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["bigmobile_store"]
users_collection = db["users"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/affiliate')
def affiliate():
    return render_template('affiliate.html')

@app.route('/special')
def special():
    return render_template('special.html')

@app.route('/sitemap')
def sitemap():
    return render_template('sitemap.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        address = request.form.get('address')
        courses = request.form.get('courses')
        terms = request.form.get('terms')

        if not terms:
            flash("Please accept terms and conditions.")
            return redirect(url_for('register'))

        users_collection.insert_one({
            "name": name,
            "email": email,
            "password": password,
            "dob": dob,
            "gender": gender,
            "address": address,
            "courses": courses,
            "registered_on": datetime.utcnow()
        })

        flash("Registration successful! You can now log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = users_collection.find_one({"email": email, "password": password})
        if user:
            flash("Login successful! Welcome back.")
            return redirect(url_for('index'))
        else:
            flash("Invalid email or password.")
            return redirect(url_for('login'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
