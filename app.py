from flask import Flask, render_template, request, redirect, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "super secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_BINDS'] = {
    'db2': 'sqlite:///drivers.db'
}
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

class drivers(db.Model, UserMixin):
    __bind_key__ = 'db2'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contact = db.Column(db.Integer, nullable=False, unique=True)
    file_name = db.Column(db.String(200), nullable=False)
    original_file = db.Column(db.LargeBinary)
    password = db.Column(db.String(100),nullable=False)


# User Side

@app.route('/')
def user_index():
    return render_template("/user/index.html")

@app.route('/user/booking')
@login_required
def booking():
    return render_template("/user/booking.html")

@app.route('/user/contact')
def contact():
     return render_template("/user/contact.html")

@app.route('/user/about')
def about():
    return render_template("/user/about.html")

# Register, Login and Logout

@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        cpassword = request.form['cpassword']

        data = users.query.filter_by(email=email).first()
        data1 = users.query.filter_by(contact=contact).first()
        if data:
            flash('Email is already registered')
            return redirect("/user/register")
        if data1:
            flash('Number is already registered')
            return redirect("/user/register")

        if password==cpassword:
            registration = users(fname=fname,lname=lname,email=email,contact=contact,password=generate_password_hash(password,method='sha256'))
            db.session.add(registration)
            db.session.commit()
            login_user(registration, remember=True)
            return redirect("/")
        else:
            flash('Confirm Password is not same as the Password')
            return redirect("/user/register")

    return render_template("/user/register.html")

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # remem = request.form['remember']

        data = users.query.filter_by(email=email).first()

        if not data or not check_password_hash(data.password, password):
            flash('Please check your login credentials')
            return redirect('/user/login')
        # if remem:
        #     login_user(data, remember=True)
        # else:
        #     login_user(data, remember=False)
        login_user(data, remember=True)
        return redirect("/")

    return render_template("/user/login.html")

@app.route('/user/logout',methods=['GET', 'POST'])
@login_required
def user_logout():
    logout_user()
    return redirect("/user/login")

#Edit Profile and Password

@app.route('/user/editprofile')
@login_required
def user_editprofile():
    return render_template("/user/editprofile.html")

@app.route('/user/update/<int:id>', methods=['GET', 'POST'])
@login_required
def user_update(id):
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
    return redirect('/user/editprofile')

@app.route('/user/editpass')
@login_required
def user_editpass():
    return render_template("/user/editpass.html")

@app.route('/user/updatepass/<int:id>', methods=['GET', 'POST'])
@login_required
def user_updatepass(id):
    if request.method == 'POST':
        opassword = request.form['opassword']
        npassword = request.form['npassword']
        cnpassword = request.form['cnpassword']

        data = users.query.filter_by(id=id).first()

        if check_password_hash(data.password,opassword):
            if npassword==cnpassword:
                data.password = generate_password_hash(npassword)
                db.session.add(data)
                db.session.commit()
                return redirect("/")
            else:
                flash('Confirm Password is not same as the Password')
                return redirect("/user/editpass")
        else:
            flash('Old password does not match')
            return redirect('/user/editpass')
    return redirect('/user/editpass')
        

# Driver Side

@app.route('/driver/home')
def home():
    return render_template('/driver/home.html')

@app.route('/driver/register', methods=['GET', 'POST'])
def driver_register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        contact = request.form['contact']
        file = request.files['inputFile']
        password = request.form['password']
        cpassword = request.form['cpassword']

        data = drivers.query.filter_by(email=email).first()
        data1 = users.query.filter_by(contact=contact).first()
        if data:
            flash('Email is already registered')
            return redirect("/driver/register")
        if data1:
            flash('Number is already registered')
            return redirect("/driver/register")

        if password==cpassword:
            registration = drivers(first_name=fname,last_name=lname,email=email,contact=contact,file_name=file.filename,original_file=file.read(),password=generate_password_hash(password,method='sha256'))
            db.session.add(registration)
            db.session.commit()
            login_user(registration, remember=True)
            return redirect("/driver/home")
        else:
            flash('Confirm Password is not same as the Password')
            return redirect("/driver/register")
    return render_template('/driver/register.html')









# Run Code

if __name__=="__main__":
    app.run(debug=True)