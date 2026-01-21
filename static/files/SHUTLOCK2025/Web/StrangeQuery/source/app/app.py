from flask import Flask, request, jsonify, make_response, render_template, redirect, url_for, session, flash, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from os import environ
import time, sys, re

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
db = SQLAlchemy(app)

def linkify_tags(content):
    pattern = r'@tag\(([^,]+),([^,]*),(\d+)\)'
    return re.sub(pattern, r'<a style="color: #e50914" href="/profile/\3">@\1 . (\2)</a>', content)

app.jinja_env.filters['linkify_tags'] = linkify_tags

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    pronouns = db.Column(db.String(500))
    verified = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    image_link = db.Column(db.String(256), nullable=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    comments = db.relationship('Comment', backref='post', lazy=True)

    def __repr__(self):
        return f'<Post {self.title}>'

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f'<Comment {self.content[:20]}>'

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Vous êtes connecté.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Nom d\'utilisateur ou mot de passe invalide.', 'danger')

    return render_template("auth/login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Nom d\'utilisateur ou email déjà utilisé.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Inscription réussite. Bienvenu!', 'success')
        return redirect(url_for('login'))

    return render_template("auth/register.html")

@app.route('/logout')
def logout():
    session.clear()
    flash('Vous avez été deconnecté', 'info')
    return redirect(url_for('home'))

@app.route("/forum", methods=["GET", "POST"])
def forum():
    movies = Movie.query.all()
    return render_template("forum.html", movies=movies)

@app.route("/movies/addMovie", methods=["GET", "POST"])
def addMovie():
  if request.method == "POST":
        if g.user:
            if g.user.verified:
              title = request.form["title"]
              content = request.form["content"]
              image_link = request.form["image_link"]
              movie = Movie(title=title, content=content, user_id=g.user.id, image_link=image_link)
              db.session.add(movie)
              db.session.commit()
              flash("Movie created successfully.", "success")
              return redirect(url_for("forum"))
            else:
              flash("Votre compte doit être vérifié pour ajouter un film.", "warning")
              return redirect(url_for("forum"))
        else:
            flash("You need to be logged in to create a post.", "warning")
            return redirect(url_for("login"))
  return render_template("movies/addMovie.html")


@app.route("/movie/<int:movie_id>", methods=["GET", "POST"])
def movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == "POST":
        if g.user and g.user.verified:
            content = request.form["content"]

            tags = re.findall(r"@[A-Za-z0-9_-]+", content)
            for tag in tags:
                username = tag[1:]
                user = User.query.filter_by(username=username).first()

                if user:
                    pronouns = user.pronouns if user.pronouns else ""
                    if pronouns:
                        sql = text("SELECT verified, id FROM users WHERE username=:username AND pronouns ='"+pronouns+"'")
                        result = db.session.execute(sql, {'username': username}).first()

                        print(result, file=sys.stderr)
                        if result[1] > 1: # We cannot tag Administrator
                          pronoun_text = f'{pronouns}' if pronouns else ''
                          content = content.replace(tag, f'@tag({username},{pronoun_text},{result[1]})')
                        elif result[1] == 1:
                            flash("Vous ne pouvez pas tag un Administrateur...", "danger")

            sql = text("INSERT INTO comments (content, movie_id, user_id) VALUES (:content, :movie_id, :user_id)")
            db.session.execute(sql, {'content': content, 'movie_id': movie.id, 'user_id': g.user.id})

            db.session.commit()

            flash("Commentaire ajouté.", "success")
            return redirect(url_for("movie", movie_id=movie.id))
        elif (g.user and not g.user.verified):
            flash("Votre compte doit être vérifié pour commenter.", "warning")

        else:
            flash("Vous devez être connecté pour commenter.", "warning")
            return redirect(url_for("login"))

    comments = Comment.query.filter_by(movie_id=movie.id).all()
    return render_template("movie.html", movie=movie, comments=comments)

@app.route('/profile', methods=['GET', 'POST'])
def profile_edit():
    if not g.user:
        flash("Vous devez être connecté pour accéder à votre profil.", "warning")
        return redirect('/login')

    if request.method == 'POST':
        email = request.form['email']
        pronouns = request.form['pronouns']
        password = request.form['password']

        if email and g.user.email != email:
          if User.query.filter_by(email=email).first():
            flash('Email déjà utilisé.', 'danger')
            return redirect('/profile')
          g.user.email = email
        if pronouns:
            g.user.pronouns = pronouns
        if password:
            g.user.password = generate_password_hash(password)

        db.session.commit()
        flash("Le profil a été mis à jour.", "success")
        return redirect('/profile')

    return render_template('profile_edit.html')

@app.route('/profile/<int:profile_id>', methods=['GET', 'POST'])
def profile(profile_id):
    if not g.user:
        flash("Vous devez être connecté pour voir un profil.", "warning")
        return redirect('/login')

    user = User.query.get_or_404(profile_id)
    if request.method == 'POST':
        if g.user.is_admin or request.cookies.get('is_a_cool_admin') == "yes":
            sql = text("UPDATE users SET verified=true WHERE id=:user_id")
            db.session.execute(sql, {'user_id': profile_id})

            db.session.commit()
            flash("Profil vérifié avec succès!", "success")
        else:
            flash("Vous ne pouvez pas faire ça!", "danger")
        return redirect(f'/profile/{profile_id}')
    resp = make_response(render_template('profile.html', user=user))
    resp.set_cookie('is_a_cool_admin','no')
    return resp

if __name__ == '__main__':
    time.sleep(1)
    with app.app_context():
        db.create_all()
    app.run(debug=False, host='0.0.0.0')
