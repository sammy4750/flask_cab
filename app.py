from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import LoginManager
# from flask_login import UserMixin

app = Flask(__name__)
app.secret_key = "super secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# login_manager = LoginManager()

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contact = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    cpassword = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return "{}{}".format(self.id,self.email)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/booking')
def booking():
    return render_template("booking.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        data = users.query.filter_by(email=email).first()

        # if data is not None:              #code by sammy for login
        #     user_pass = data[5]
        #     if password == user_pass:
        #         return redirect("/")   

        if not data or not check_password_hash(data.password, password):
            flash('Please check your login credentials.')
            return redirect('/login')
        return redirect("/")

    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        cpassword = request.form['cpassword']

        data = users.query.filter_by(email=email).first()
        if data:
            flash('User already exist')
            return redirect("/register")

        registration = users(fname=fname,lname=lname,email=email,contact=contact,password=generate_password_hash(password,method='sha256'),cpassword=generate_password_hash(cpassword,method='sha256'))
        db.session.add(registration)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

if __name__=="__main__":
    app.run(debug=True)