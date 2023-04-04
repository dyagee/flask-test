from flask import Flask,flash,render_template,request, url_for, session,abort,redirect
#from markupsafe import escape
import os
from flask_sqlalchemy import SQLAlchemy 
#from sqlalchemy.dialects.postgresql import ARRAY
 

basedir = os.path.abspath(os.path.dirname(__file__))

# create the app
app = Flask(__name__)
app.secret_key =''

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
msg = None
error = None

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    diary = db.Column(db.String)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/users")
def users():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("list.html", users=users)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        user = User(
            username=request.form["name"],
            email=request.form["email"],
            diary = request.form["diary"],
        )
        db.session.add(user)
        db.session.commit()
        msg =f"User ID :{user.id}; Username: {user.username} created successfully" 
        return render_template('action.html', msg=msg )
    return render_template("create.html")

@app.route("/add_bio", methods=['GET','POST'])
def add_bio():
    if request.method == "POST":
        email=request.form["email"]
        user = db.one_or_404(
        db.select(User).filter_by(email=email),
        description=f"'{email}' Not found!"
        )
        if user: 
            user.diary += f"-{request.form['diary']}"
            db.session.merge(user)
            db.session.commit()
            msg =f"Bio added to Account: '{user.username}' created successfully" 
            return render_template('action.html', msg=msg )
       
    return render_template("update.html")

@app.route("/check_bio", methods=['GET','POST'])
def check_bio():
    if request.method == "POST":
        email=request.form["email"]
        user = db.one_or_404(
        db.select(User).filter_by(email=email),
        description=f"'{email}' Not found!"
        )
        if user: 
            
            diaries = str(user.diary)
            diaries = diaries.split("-")
            return render_template('action.html', diaries = diaries )
       
    return render_template("bio.html")

if __name__ == "__main__":
    app.run(debug=True)
    
    '''
#uncomment this block of code to instantiate the sqlite db 
with app.app_context():
    db.create_all()'''