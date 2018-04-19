from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:MyNewPass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.TEXT)

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<User %r>' % self.title

@app.route("/newpost", methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':

        blog_title = request.form['title']
        blog_body = request.form['body']

        if blog_title == "":
            error = "Please fill in Title."
            return redirect("/newpost")
        
        elif blog_body == "":
            error = "Please fill in Body."
            return redirect("/newpost")

        else:
            new_post = Blog(title=blog_title, body=blog_body)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog')

    else:
         return render_template('new.html')


@app.route('/blog', methods=['POST', 'GET'])
def index():

    posts = Blog.query.all()

    return render_template('blog.html', posts=posts)

if __name__ == '__main__':
    app.run()
