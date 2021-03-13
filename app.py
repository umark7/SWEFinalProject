from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://H3ll0w0rld@localhost/finalProject'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://H3ll0w0rld@localhost/finalProject'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    class = db.Column(db.String(200), unique=True)
    teacher = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, class, teacher, rating, comments): #constructor in Python
        self.class = class
        self.teacher = teacher
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        class = request.form['class']
        teacher = request.form['teacher']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(class, teacher, rating, comments)
        if class == '' or teacher == '':
            return render_template('index.html', message='Please enter fields')
        if db.session.query(Feedback).filter(Feedback.class == class).count() == 0:
            data = Feedback(class, teacher, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(class, teacher, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')


if __name__ == '__main__':
    app.run()