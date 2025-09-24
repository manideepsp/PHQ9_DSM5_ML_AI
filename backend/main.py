from flask import Flask, request
from phq9_processor import process_phq9_submission
from auth import auth_bp
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(
    app,
    origins=["http://localhost:3000", "http://localhost:5173"],
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    expose_headers=["Content-Type", "Authorization"]
)
app.register_blueprint(auth_bp)

@app.route('/api/phq9', methods=['POST'])
def phq9():
    data = request.get_json()
    print('Received PHQ-9 data:', data)
    user_id = data.get('user_id')
    responses = data.get('responses')
    total_score = data.get('totalScore')
    doctors_notes = data.get('doctors_notes', "")
    patients_notes = data.get('patients_notes', "")
    result = process_phq9_submission(user_id, responses, total_score, doctors_notes, patients_notes)
    return result, 200

if __name__ == '__main__':
    app.run(debug=True)