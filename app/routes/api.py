from crypt import methods
from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User
from app.db import get_db

import sys

bp = Blueprint('api', __name__, url_prefix='/api')

# POST route to receive new user data
@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()
  
  try:
    # attempt to create new user
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

  except:
    print(sys.exc_info()[0])
    # insert failed, so rollback and send error to front end
    db.rollback()
    return jsonify(message = 'Signup failed'), 500

  # added session object to signup route
  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True

  return jsonify(id = newUser.id)

# POST route to logout user
@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove session variables
  session.clear()
  return '', 204

# POST route to login user
@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()

  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])

    return jsonify(message = 'Incorrect credentials'), 400

  # verify password at login
  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Incorrect credentials'), 400

  # create user session after logged in
  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True

  return jsonify(id = user.id)