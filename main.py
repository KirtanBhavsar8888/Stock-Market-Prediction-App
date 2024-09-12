from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import random
from flask_mail import Mail, Message
from stock_data import get_stock_data  # Import stock data function from stock_data.py

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sqluser:kirtan15@localhost/emails'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super secret key'

# Currency API URL
url = "http://data.fixer.io/api/latest?access_key=5032fc77867c90a637bac81b7278711f"

# Mail Configuration 
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'dontreplystock@outlook.com'
app.config['MAIL_PASSWORD'] = '@12a@34b'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)  
# Mail Configuration Complete
db = SQLAlchemy(app)

class users_stockapp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    user = users_stockapp.query.filter_by(email=email, password=password).first()

    if user:
        return redirect(url_for('home'))
    else:
        return "Login failed. Incorrect email or password."

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        return "Passwords do not match. Please try again."

    global otp
    otp = random.randint(100000, 999999)

    # Store user data in session
    session['name'] = name
    session['email'] = email
    session['password'] = password

    msg = Message('OTP for Stock Prediction App', sender='dontreplystock@outlook.com', recipients=[email])
    msg.body = f"Hello {name}, your OTP for registration is {otp}. Please use it to verify your account."
    mail.send(msg)
    
    return render_template('verify_otp.html', email=email)

@app.route('/user_otp_verify', methods=['POST'])
def email_verify():
    user_otp = request.form['otp']
    if int(user_otp) == otp:
        # Retrieve user data from session
        name = session.get('name')
        email = session.get('email')
        password = session.get('password')

        # Check if the data exists before saving to the database
        if name and email and password:
            user = users_stockapp(name=name, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            flash("You have successfully registered. Please login to continue.")
            return redirect(url_for('index'))
        else:
            flash("Error retrieving user data. Please try again.")
            return redirect(url_for('register'))

    flash("OTP verification failed. Please try again.")
    return redirect(url_for('register'))

def currency_converter():
    return render_template('currency_converter.html')

@app.route('/stock/<ticker>')
def stock_detail(ticker):
    
    raw_data, graphs = get_stock_data(ticker)
    
    return render_template('stock.html', ticker=ticker, raw_data=raw_data.to_html(), 
                           basic_graph=graphs['basic'], week_graph=graphs['week'], 
                           month_graph=graphs['month'], year_graph=graphs['year'])


if __name__ == '__main__':
    app.run(debug=True)
