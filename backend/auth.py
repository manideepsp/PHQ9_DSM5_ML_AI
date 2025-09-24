from flask import Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User, Base
import bcrypt
import uuid
import os
from datetime import datetime

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/postgres')
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    emailid = data.get('emailid')
    username = data.get('username')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    age = data.get('age')
    gender = data.get('gender')
    industry = data.get('industry')
    profession = data.get('profession')

    if not emailid or not emailid.endswith('@gmail.com'):
        return jsonify({'error': 'Email must be a valid @gmail.com address'}), 400
    if not password or len(password) < 4:
        return jsonify({'error': 'Password must be at least 4 characters'}), 400
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400
    if not age or not gender or not industry or not profession:
        return jsonify({'error': 'All fields are required'}), 400

    session = Session()
    if session.query(User).filter_by(emailid=emailid).first():
        return jsonify({'error': 'Email already registered'}), 400
    if session.query(User).filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 400

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(
        emailid=emailid,
        username=username,
        firstname=firstname,
        lastname=lastname,
        age=int(age),
        gender=gender,
        industry=industry,
        profession=profession,
        password_hash=password_hash
    )
    session.add(user)
    session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    emailid = data.get('emailid')
    password = data.get('password')
    session = Session()
    user = session.query(User).filter_by(emailid=emailid).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({'error': 'Invalid credentials'}), 401
    return jsonify({'user_id': str(user.user_id), 'username': user.username}), 200
