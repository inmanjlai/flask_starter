from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
database_name = 'posts.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_name
database = SQLAlchemy(app)

from models.Posts import Posts

@app.route("/")
def home():
    posts = Posts.query.all()
    posts.reverse()
    return render_template("home.html", posts=posts)

@app.route("/posts", methods=["POST"])
def create_post():
    body = request.form
    
    new_post = Posts(
            title=body['title'],
            content=body['content'],
            username=body['username']
        )
    database.session.add(new_post)
    database.session.commit()

    return redirect("/")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post_to_delete = Posts.query.get(post_id)
    database.session.delete(post_to_delete)
    database.session.commit()

    return redirect("/")

# THIS ROUTE WILL JUST CREATE 15 POSTS TO POPULATE THE POSTS COLUMN ->
@app.route("/seed-posts")
def seed():
    for x in range(16):
        new_post = Posts(
            title=f"Post Title {x}",
            content="Pellentesque in ipsum id orci porta dapibus. Nulla porttitor accumsan tincidunt. Nulla porttitor accumsan tincidunt. Curabitur aliquet quam id dui posuere blandit. Nulla porttitor accumsan tincidunt.",
            username=f"User-{x}"
        )
        database.session.add(new_post)
        database.session.commit()

    return redirect("/")
