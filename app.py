from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from dotenv import load_dotenv
load_dotenv()

from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import atexit


app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)


print("Initializing Flask application")
print(f"Template folder: {app.template_folder}")
print("Registered routes:")
for rule in app.url_map.iter_rules():
    print(f" - {rule}")




google_bp = make_google_blueprint(
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    scope=["profile", "email"]
)
app.register_blueprint(google_bp, url_prefix="/google_login")


facebook_bp = make_facebook_blueprint(
    client_id=os.getenv('FACEBOOK_APP_ID'),
    client_secret=os.getenv('FACEBOOK_APP_SECRET'),
    scope=["email"]
)
app.register_blueprint(facebook_bp, url_prefix="/facebook_login")


login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email
        self.username = id


    def get_id(self):
        return str(self.id)


USER_STORAGE_FILE = 'users.json'

def load_users():
    try:
        with open(USER_STORAGE_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users():
    with open(USER_STORAGE_FILE, 'w') as f:
        json.dump(users, f)


users = load_users()


atexit.register(save_users)

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id, users[user_id].get('email', user_id))
    return None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        pass
    return render_template('index.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if username in users:
            flash('Username already exists', 'error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters', 'error')
        elif password != confirm_password:
            flash('Passwords do not match', 'error')
        else:
            hashed_password = generate_password_hash(password)
            users[username] = {
                'password': hashed_password,
                'email': username

            }
            save_users()

            flash('Registration successful! Please login.', 'success')
            return redirect('/login')
            
    return render_template('register.html',
                        google_client_id=os.getenv('GOOGLE_CLIENT_ID'),
                        facebook_app_id=os.getenv('FACEBOOK_APP_ID'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and check_password_hash(users[username]['password'], password):
            user = User(username, username)
            session['username'] = username

            login_user(user)
            return redirect('/')
        else:
            flash('Invalid username or password', 'error')
            
    return render_template('login.html',
                        google_client_id=os.getenv('GOOGLE_CLIENT_ID'),
                        facebook_app_id=os.getenv('FACEBOOK_APP_ID'))

@app.route('/google-login', methods=['POST'])
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return "Google login failed", 400
    
    google_data = resp.json()
    user = User(google_data['id'], google_data['email'])
    login_user(user)
    return redirect('/')

@app.route('/facebook-login', methods=['POST'])
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for("facebook.login"))
    
    resp = facebook.get("/me?fields=id,email")
    if not resp.ok:
        return "Facebook login failed", 400
    
    facebook_data = resp.json()
    user = User(facebook_data['id'], facebook_data['email'])
    login_user(user)
    return redirect('/')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/video_lectures')
def video_lectures():
    return render_template('video_lectures.html')

@app.route('/quizzes')
def quizzes():
    return render_template('quizzes.html')




@app.route('/test_quizzes')
def test_quizzes():
    print("Test quizzes route accessed")

    try:
        return render_template('quizzes.html')
    except Exception as e:
        print(f"Error rendering quizzes template: {e}")

        return f"Template rendering error: {str(e)}"

@app.route('/ask_questions')
def ask_questions():
    return render_template('ask_questions.html')

@app.route('/scholarship')
def scholarship():
    return render_template('scholarship.html')


@app.route('/subjects')
def subjects():
    return render_template('subjects.html')

@app.route('/grades')
def grades():
    return render_template('grades.html')



@app.route('/profile_manager')
def profile_manager():
    return render_template('profile_manager.html')


@app.route('/quiz1')
def quiz1():
    return render_template('quiz1.html')

@app.route('/quiz2')
def quiz2():
    return render_template('quiz2.html')

@app.route('/quiz3')
def quiz3():
    return render_template('quiz3.html')










if __name__ == '__main__':

    app.run(debug=True)
