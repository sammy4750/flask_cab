from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
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

@app.route('/login')
def login():
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

        registration = users(fname=fname,lname=lname,email=email,contact=contact,password=password,cpassword=cpassword)
        db.session.add(registration)
        db.session.commit()

    return render_template("register.html")

if __name__=="__main__":
    app.run(debug=True)