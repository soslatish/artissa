from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///artissa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Поля профиля пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)

#Поля задания
class Job(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(400), nullable = False)
    budget = db.Column(db.Float, nullable = False)
    #user_id = db.Column()
    user = db.relationship('User', backref= db.backref('jobs', lazy = True))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST' :
        name = request.form ['name']
        email = request.form ['email']
        password = request.form ['password']
        user = User(name = name, password = password, email = email)
        db.session.add(user)
        db.session.commit
        return redirect(url_for('signup_success', name = name))
    return render_template('signp.html')

@app.route('/signup_success/<name>')
def signup_success(name):
    return render_template('signup_success.html', name = name)

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form ['email']
        password = request.form ['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return redirect(url_for('login_success.html', email = email))
        else:
            return redirect(url_for('login.html', error = True))
    return render_template('login_html')

@app.route('/login_success/<email>')
def login_success(email):
    return render_template ('login_success.html', email = email)

@app.route('/add_job', methods=['POST', 'GET'])
def add_job():
    if request.method == 'POST':
        title = request.form ['title']
        description=request.form ['description']
        budget=request.form['budget']
        user=User.query.filter_by(email=request.form['email']).first()
        job = Job(title=title, description = description, budget=budget, user=user)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('job_success', email = user.email))
    return render_template('add_job.html')

@app.route('/job_success/<email>')
def job_success(email):
    return render_template('job_success.html', email = email)


if __name__ == "__main__":
    app.run(debug=True)