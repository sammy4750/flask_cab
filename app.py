from flask import Flask, render_template, request, redirect, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "super secret key"



app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#flask_login Stuff:

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):

    return users.query.get(int(user_id))

#  Database Models

class users(db.Model, UserMixin):
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
    if request.cookies:
        c = request.cookies
        print(c)
    else:
        print("Bye Bye")
    return render_template("index.html")

@app.route('/booking')
@login_required
def booking():
    return render_template("booking.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/about')
def about():
    return render_template("about.html")

# Register, Login and Logout

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        data = users.query.filter_by(email=email).first()

        if not data or not check_password_hash(data.password, password):
            flash('Please check your login credentials')
            return redirect('/login')
        login_user(data)
        return render_template("index.html", data=data)

    return render_template("login.html")

@app.route('/logout',methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect("/login")

# Run Code

if __name__=="__main__":
    app.run(debug=True)