from flask import Flask, render_template, request
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)
CORS(app)
admin = Admin(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    nickname = db.Column(db.String(80))
    message = db.Column(db.Text)
    
    def serialize(self):
        return {
            "name": self.name,
            "nickname": self.nickname,
            "message": self.message
            }
    
    def __repr__(self):
        return f"Post('{self.id}', '{self.name}')"
    
admin.add_view(ModelView(Post, db.session))
    
@app.route('/')
def home():
    return render_template('form.html')

@app.route('/wishes')
def wishes():
    return jsonify(list(map(lambda post: post.serialize(), Post.query.all())))
    
@app.route('/add', methods=["GET", "POST"])
def add():
    if request.form:
        post = Post(name=request.form.get("name"), nickname=request.form.get("nickname"), message=request.form.get("message"))
        db.session.add(post)
        db.session.commit()
        return jsonify(request.form)
    return 'Added'

if __name__ == '__main__':
    app.run(debug=True)    