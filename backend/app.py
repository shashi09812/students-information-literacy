from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import joblib
import pandas as pd
import numpy as np
import os
from functools import wraps
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')
app.secret_key = os.environ.get('SECRET_KEY', 'super_secret_learning_predictor_key_123')
# PostgreSQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/info_literacy_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

class User(db.Model):
    """Model for Mentor accounts."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    predictions = db.relationship('Prediction', backref='mentor', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Load trained models at startup
models = {}
for name in ['decision_tree', 'knn', 'naive_bayes', 'neural_net', 'random_forest']:
    try:
        dict_key = name.replace('_', ' ').title()
        if dict_key == 'Neural Net':
            pass # Name as is
        # Absolute path to models folder within backend
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(backend_dir, 'models', f'{name}.joblib')
        models[dict_key] = joblib.load(model_path)
    except Exception as e:
        print(f"Model {name} not found: {e}")

@app.template_filter('fromjson')
def fromjson_filter(s):
    """Parse JSON string for use inside Jinja2 templates."""
    try:
        return json.loads(s)
    except Exception:
        return {}

class Prediction(db.Model):
    """Model for storing student performance predictions locally."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    info_thinking = db.Column(db.Float, nullable=False)
    info_retrieval = db.Column(db.Float, nullable=False)
    info_ethics = db.Column(db.Float, nullable=False)
    score = db.Column(db.Float, nullable=False)
    classification = db.Column(db.String(50), nullable=False)
    model_results = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('signup'))
            
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, Mentor {username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('landing'))

@app.route("/dashboard")
@login_required
def index():
    return render_template("index.html")

@app.route("/compare")
@login_required
def compare():
    return render_template("compare.html")

@app.route("/history")
@login_required
def history():
    user_id = session['user_id']
    try:
        all_predictions = Prediction.query.filter_by(user_id=user_id).order_by(Prediction.timestamp.desc()).all()
        return render_template("history.html", predictions=all_predictions)
    except Exception as e:
        print(f"PostgreSQL Error in /history: {e}")
        # PostgreSQL doesn't need path hacks, just ensure the connection is alive
        return f"<h3>Database Connection Error</h3><p>{e}</p><p>Please ensure PostgreSQL is running and the database 'info_literacy_db' exists.</p>", 500

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    data = request.json
    info_thinking = float(data.get('info_thinking', 0))
    info_retrieval = float(data.get('info_retrieval', 0))
    info_ethics = float(data.get('info_ethics', 0))
    
    X = pd.DataFrame([{
        'info_thinking': info_thinking,
        'info_retrieval': info_retrieval,
        'info_ethics': info_ethics
    }])
    
    results = {}
    score_map = {'High Effect': 85.0, 'Moderate Effect': 65.0, 'Low Effect': 45.0}
    
    if not models:
        return jsonify({"error": "Models not loaded. Did you run ML script?"}), 500

    for name, model in models.items():
        try:
            prediction = model.predict(X)[0]
            # Probabilities for a more granular score, if available
            try:
                probs = model.predict_proba(X)[0]
                classes = list(model.classes_)
                # Let's derive a numeric score representing % confidence
                # We give high weight to High Effect, med to Moderate, low to Low
                score = (probs[classes.index('High Effect')] * 100 * 0.9) + \
                        (probs[classes.index('Moderate Effect')] * 100 * 0.6) + \
                        (probs[classes.index('Low Effect')] * 100 * 0.3)
            except Exception:
                score = score_map.get(prediction, 50.0)
                
            results[name] = {
                'score': score,
                'classification': prediction
            }
        except Exception as e:
            pass

    # The abstract emphasizes Random Forest as the best model, so let's default the overall prediction to it
    best_model = 'Random Forest'
    overall_score = results[best_model]['score'] if best_model in results else 50
    overall_class = results[best_model]['classification'] if best_model in results else 'Low Effect'
    
    return jsonify({
        'results': results,
        'ensembleScore': overall_score,
        'ensembleClass': overall_class
    })

@app.route('/save_prediction', methods=['POST'])
@login_required
def save_prediction():
    data = request.form
    new_prediction = Prediction(
        user_id=session['user_id'],
        info_thinking=float(data['info_thinking']),
        info_retrieval=float(data['info_retrieval']),
        info_ethics=float(data['info_ethics']),
        score=float(data['score']),
        classification=data['classification'],
        model_results=data['model_results']
    )
    db.session.add(new_prediction)
    db.session.commit()
    return "", 204

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
