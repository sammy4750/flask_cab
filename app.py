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
    contact = db.Column(db.Integer, nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return "{}{}".format(self.id,self.email)


@app.route('/')
def index():
    return render_template("/user/index.html")

@app.route('/booking')
@login_required
def booking():
    return render_template("/user/booking.html")

@app.route('/contact')
def contact():
     return render_template("/user/contact.html")

@app.route('/about')
def about():
    return render_template("/user/about.html")

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

        if password==cpassword:
            registration = users(fname=fname,lname=lname,email=email,contact=contact,password=generate_password_hash(password,method='sha256'))
            db.session.add(registration)
            db.session.commit()
            login_user(registration, remember=True)
            return redirect("/")
        else:
            flash('Confirm Password is not same as the Password')
            return redirect("/register")

    return render_template("/user/register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # remem = request.form['remember']

        data = users.query.filter_by(email=email).first()

        if not data or not check_password_hash(data.password, password):
            flash('Please check your login credentials')
            return redirect('/login')
        # if remem:
        #     login_user(data, remember=True)
        # else:
        #     login_user(data, remember=False)
        login_user(data, remember=True)
        return redirect("/")

    return render_template("/user/login.html")

@app.route('/logout',methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect("/login")

#Edit Profile and Password

@app.route('/editprofile')
@login_required
def editprofile():
    return render_template("/user/editprofile.html")

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        contact = request.form['contact']

        data = users.query.filter_by(id=id).first()
        data.fname = fname
        data.lname = lname
        data.contact = contact
        db.session.add(data)
        db.session.commit()

        return redirect("/")
    return redirect('/editprofile')

@app.route('/editpass')
@login_required
def editpass():
    return render_template("/user/editpass.html")

@app.route('/updatepass/<int:id>', methods=['GET', 'POST'])
@login_required
def updatepass(id):
    if request.method == 'POST':
        opassword = request.form['opassword']
        npassword = request.form['npassword']
        cnpassword = request.form['cnpassword']

        data = users.query.filter_by(id=id).first()

        if check_password_hash(data.password,opassword):
            if npassword==cnpassword:
                data.password = generate_password_hash(npassword)
                data.cpassword = generate_password_hash(cnpassword)
                db.session.add(data)
                db.session.commit()
                return redirect("/")
            else:
                flash('Confirm Password is not same as the Password')
                return redirect("/editpass")
        else:
            flash('Old password does not match')
            return redirect('/editpass')
    return redirect('/editpass')
        

# Run Code

if __name__=="__main__":
    app.run(debug=True)