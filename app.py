import email
from unicodedata import name
from flask import Flask, render_template, request, redirect, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, logout_user, current_user
from flask_user import roles_required, UserMixin, login_required, UserManager
from flask_googlemaps import GoogleMaps, Map
import json

app = Flask(__name__)
app.secret_key = "50cf8b9fd427ee793cb4bfb17af7f69e7e373d3d9095b1061da93552aca8eea3"
app.config['USER_ENABLE_EMAIL'] = False

app.config['GOOGLEMAPS_KEY'] = "AIzaSyDdQ3Jx0mPk6J9vNVdKN-tSDCM5eYk9abs"
# app.config['USER_ENABLE_AUTH0'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDdQ3Jx0mPk6J9vNVdKN-tSDCM5eYk9abs" #Setting Google Maps API key
db = SQLAlchemy(app)
migrate = Migrate(app,db)
# GoogleMaps(app)

#Initializing the extension
GoogleMaps(app)

#flask_login Stuff:

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __table_name__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20))
    rider = db.relationship("Rider")
    driver = db.relationship("Driver")
    roles = db.relationship('Role', secondary='user_roles')

    __mapper_args__ = {
        'polymorphic_on':type,
         'polymorphic_identity':'User'
    }

    def __repr__(self) -> str:
        return "{}{}".format(self.id,self.fname)
        
user_manager = UserManager(app, db, User)

class Rider(User, db.Model):
    rider_id = db.Column(ForeignKey('user.id'), primary_key=True)
    rider_email = db.Column(db.String(100), nullable=False, unique=True)
    rider_contact = db.Column(db.Integer, nullable=False, unique=True)

    __mapper_args__ = {
        'polymorphic_identity':'Rider'
    }

class Driver(User, db.Model):
    driver_id = db.Column(ForeignKey('user.id'), primary_key=True)
    file_name = db.Column(db.String(200), nullable=False)
    original_file = db.Column(db.LargeBinary)
    driver_email = db.Column(db.String(100), nullable=False, unique=True)
    driver_contact = db.Column(db.Integer, nullable=False, unique=True)

    __mapper_args__ = {
        'polymorphic_identity':'Driver'
    }

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))

# Define the UserRoles association table
class UserRoles(User, db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), ForeignKey('roles.id', ondelete='CASCADE'))

# User Side
@app.route('/')
def user_index():
    return render_template("/user/index.html")

@app.route('/user/contact')
def contact():
     return render_template("/user/contact.html")

@app.route('/user/about')
def about():
    return render_template("/user/about.html")

# Register, Login and Logout
@app.route('/user/register1', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        cpassword = request.form['cpassword']

        data = Rider.query.filter_by(rider_email=email).first()
        data1 = Rider.query.filter_by(rider_contact=contact).first()
        if data:
            flash('Email is already registered')
            return redirect("/user/register")
        if data1:
            flash('Number is already registered')
            return redirect("/user/register")

        if password==cpassword:
            registration = Rider(fname=fname,lname=lname,rider_email=email,rider_contact=contact,password=generate_password_hash(password,method='sha256'))
            registration.roles=[Role.query.filter_by(id="1").first()]
            db.session.add(registration)
            db.session.commit()
            login_user(registration) #remember=True
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

        data = Rider.query.filter_by(rider_email=email).first()

        if not data or not check_password_hash(data.password, password):
            flash('Please check your login credentials')
            return redirect('/user/login')
        login_user(data) # remember=True
        return redirect("/")

    return render_template("/user/login.html")

@app.route('/user/logout',methods=['GET', 'POST'])
@login_required
def user_logout():
    logout_user()
    return redirect("/user/login")

#Edit Profile and Password
@app.route('/user/editprofile')
@roles_required("Rider")
@login_required
def user_editprofile():
    return render_template("/user/editprofile.html")

@app.route('/user/update/<int:id>', methods=['GET', 'POST'])
@roles_required("Rider")
@login_required
def user_update(id):
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        contact = request.form['contact']

        data = User.query.filter_by(id=id).first()
        data.fname = fname
        data.lname = lname
        data.rider_contact = contact
        db.session.add(data)
        db.session.commit()

        return redirect("/")
    return redirect('/user/editprofile')

@app.route('/user/editpass')
@roles_required("Rider")
@login_required
def user_editpass():
    return render_template("/user/editpass.html")

@app.route('/user/updatepass/<int:id>', methods=['GET', 'POST'])
@roles_required("Rider")
@login_required
def user_updatepass(id):
    if request.method == 'POST':
        opassword = request.form['opassword']
        npassword = request.form['npassword']
        cnpassword = request.form['cnpassword']

        data = User.query.filter_by(id=id).first()

        if check_password_hash(data.password,opassword):
            if npassword==cnpassword:
                data.password = generate_password_hash(npassword)
                db.session.add(data)
                db.session.commit()
                flash("Your password has been changed.")
                email = current_user.rider_email
                data = Rider.query.filter_by(rider_email=email).first()
                login_user(data)
                return redirect("/user/editpass")
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

        data = Driver.query.filter_by(driver_email=email).first()
        data1 = Driver.query.filter_by(driver_contact=contact).first()
        if data:
            flash('Email is already registered')
            return redirect("/driver/register")
        if data1:
            flash('Number is already registered')
            return redirect("/driver/register")

        if password==cpassword:
            registration = Driver(fname=fname,lname=lname,driver_email=email,driver_contact=contact,file_name=file.filename,original_file=file.read(),password=generate_password_hash(password,method='sha256'))
            registration.roles=[Role.query.filter_by(id="2").first()]
            db.session.add(registration)
            db.session.commit()
            login_user(registration) # remember=True
            return redirect("/driver/home")
        else:
            flash('Confirm Password is not same as the Password')
            return redirect("/driver/register")
    return render_template('/driver/register.html')

@app.route('/driver/login', methods=['GET', 'POST'])
def driver_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        data = Driver.query.filter_by(driver_email=email).first()

        if not data or not check_password_hash(data.password, password):
            flash('Please check your login credentials')
            return redirect('/driver/login')
        login_user(data) #remember=True
        return redirect("/driver/home")

    return render_template("/driver/login.html")

@app.route('/driver/logout',methods=['GET', 'POST'])
@roles_required("Driver")
@login_required
def driver_logout():
    logout_user()
    return redirect("/driver/login")

# Edit Profile and Password

@app.route('/driver/editprofile')
@roles_required("Driver")
@login_required
def driver_editprofile():
    return render_template("/driver/editprofile.html")

@app.route('/driver/update/<int:id>', methods=['GET', 'POST'])
@roles_required("Driver")
@login_required
def driver_update(id):
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        contact = request.form['contact']

        data = Driver.query.filter_by(id=id).first()
        data.fname = fname
        data.lname = lname
        data.driver_contact = contact
        db.session.add(data)
        db.session.commit()

        return redirect("/driver/home")
    return redirect('/drriver/editprofile')

@app.route('/driver/editpass')
@roles_required("Driver")
@login_required
def driver_editpass():
    return render_template("/driver/editpass.html")

@app.route('/driver/updatepass/<int:id>', methods=['GET', 'POST'])
@roles_required("Driver")
@login_required
def driver_updatepass(id):
    if request.method == 'POST':
        opassword = request.form['opassword']
        npassword = request.form['npassword']
        cnpassword = request.form['cnpassword']

        data = Driver.query.filter_by(id=id).first()

        if check_password_hash(data.password,opassword):
            if npassword==cnpassword:
                data.password = generate_password_hash(npassword)
                db.session.add(data)
                db.session.commit()
                flash("Your password has been changed.")
                email = current_user.driver_email
                data = Driver.query.filter_by(driver_email=email).first()
                login_user(data)
                return redirect("/driver/editpass")
            else:
                flash('Confirm Password is not same as the Password')
                return redirect("/driver/editpass")
        else:
            flash('Old password does not match')
            return redirect('/driver/editpass')
    return redirect('/driver/editpass')

@app.route('/user/booking', methods=['GET', 'POST'])
@roles_required("Rider")
@login_required
def bookride():
    # if request.method == 'POST':

    #     # Write code here to store the data
        
    #     return render_template('user/ridedetails.html')
    return render_template('user/booking.html')

# @app.route('/bookride', methods=['GET', 'POST'])
# def bookride():
#     if request.method == 'POST':
#         # Collecting location data submitted by user
#         origin_coordinates = request.form['origin_coordinates']
#         destination_coordinates = request.form['destination_coordinates']
#         origin_name = request.form['origin_name']

#         origin_place_id = request.form['origin_place_id']
#         destination_place_id = request.form['destination_place_id']
#         destination_name = request.form['destination_name']

#         # Converting string back into dictionary
#         origin_coordinates_dict = json.loads(origin_coordinates)
#         destination_coordinates_dict = json.loads(destination_coordinates)

#         # Printing Data
#         print("Origin co-ordinates are: " + origin_coordinates)
#         print("Origin Place id is: " + origin_place_id)
#         print("Origin Place name is: " + origin_name)
        
#         print("Destination co-ordinates are: " + destination_coordinates)
#         print("Destination Place id is: " + destination_place_id)
#         print("Destination Place name is: " + destination_name)
#         return render_template('user/ridedetails.html', name=[origin_name,destination_name])
#     return render_template('/user/bookride.html')


@app.route('/ride')
def ride():
    return render_template('/user/ridedetails.html')


# Run Code
if __name__=="__main__":
    app.run(debug=True)