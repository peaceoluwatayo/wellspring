from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Configure the PostgreSQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class StudentBehavior(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.String(255), nullable=False)
    class_name = db.Column(db.String(255), nullable=False)
    section = db.Column(db.String(255), nullable=False)
    behavior = db.Column(db.String(255), nullable=False)
    students = db.Column(db.Text, nullable=True)
    subject = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    feedback = db.Column(db.Text, nullable=True)


@app.route('/submit_behavior', methods=['POST'])
def submit_behavior():
    data = request.json
    if not isinstance(data, list):
        return jsonify({'error': 'Data must be a list of entries.'}), 400

    try:
        new_entries = []
        for entry in data:
            new_entry = StudentBehavior(
                teacher=entry['teacher'],
                class_name=entry['class_name'],  # Align with frontend naming
                section=entry['section'],
                behavior=entry['behavior'],
                students=entry.get('students', None),
                subject=entry['subject'],
                date=datetime.strptime(entry['date'], '%Y-%m-%d').date(),
                feedback=entry.get('feedback', None)
            )
            new_entries.append(new_entry)

        db.session.bulk_save_objects(new_entries)
        db.session.commit()

        return jsonify({'message': 'Data successfully submitted!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    

@app.route('/get_behavior_data', methods=['GET'])
def get_behavior_data():
    try:
        behaviors = StudentBehavior.query.all()
        data = [
            {
                'id': behavior.id,
                'teacher': behavior.teacher,
                'class_name': behavior.class_name,
                'section': behavior.section,
                'behavior': behavior.behavior,
                'students': behavior.students,
                'subject': behavior.subject,
                'date': behavior.date.strftime('%Y-%m-%d'),
                'timestamp': behavior.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'feedback': behavior.feedback,
            }
            for behavior in behaviors
        ]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

   
if __name__ == '__main__':
    app.run(debug=True)
