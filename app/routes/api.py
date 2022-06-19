from crypt import methods
from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

# POST route to receive new user data
@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()
  
  # create new user
  newUser = User(
    username = data['username'],
    email = data['email'],
    password = data['password']
  )

  # save in database
  # method to prep the INSERT statement
  db.add(newUser)

  #method to officially update database
  db.commit()

  return jsonify(id = newUser.id)