from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    study_time = db.Column(db.Integer, nullable=False)
    quizzes_taken = db.Column(db.Integer, nullable=False)
    pre_test_score = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float, nullable=False)
    classification = db.Column(db.String(50), nullable=False)
    model_results = db.Column(db.String(300), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/compare")
def compare():
    return render_template("compare.html")

@app.route("/history")
def history():
    all_predictions = Prediction.query.order_by(Prediction.timestamp.desc()).all()
    return render_template("history.html", predictions=all_predictions)

@app.route('/save_prediction', methods=['POST'])
def save_prediction():
    data = request.form
    new_prediction = Prediction(
        study_time=int(data['study_time']),
        quizzes_taken=int(data['quizzes_taken']),
        pre_test_score=int(data['pre_test_score']),
        score=float(data['score']),
        classification=data['classification'],
        model_results=data['model_results']
    )
    db.session.add(new_prediction)
    db.session.commit()
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
