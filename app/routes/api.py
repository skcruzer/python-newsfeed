from crypt import methods
import json
from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User, Post, Comment, Vote
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
            username=data['username'],
            email=data['email'],
            password=data['password']
        )

        # save in database
        # method to prep the INSERT statement
        db.add(newUser)
        # method to officially update database
        db.commit()

    except:
        print(sys.exc_info()[0])
        # insert failed, so rollback and send error to front end
        db.rollback()
        return jsonify(message='Signup failed'), 500

    # added session object to signup route
    session.clear()
    session['user_id'] = newUser.id
    session['loggedIn'] = True

    return jsonify(id=newUser.id)


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

        return jsonify(message='Incorrect credentials'), 400

    # verify password at login
    if user.verify_password(data['password']) == False:
        return jsonify(message='Incorrect credentials'), 400

    # create user session after logged in
    session.clear()
    session['user_id'] = user.id
    session['loggedIn'] = True

    return jsonify(id=user.id)


# connect comment route to db
@bp.route('/comments', methods=['POST'])
def comment():
    data = request.get_json()
    db = get_db()

    try:
        # create a new comment
        newComment = Comment(
            comment_text=data['comment_text'],
            post_id=data['post_id'],
            user_id=session.get('user_id')
        )

        db.add(newComment)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message='Comment failed'), 500

    return jsonify(id=newComment.id)


# upvotes action
@bp.route('/posts/upvote', methods=['PUT'])
def upvote():
    data = request.get_json()
    db = get_db()

    try:
        # create a new vote with incoming id and session id
        newVote = Vote(
            post_id=data['post_id'],
            user_id=session.get('user_id')
        )

        db.add(newVote)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message='Upvote failed'), 500

    return '', 204


# creating posts route
@bp.route('/posts', methods=['POST'])
def create():
      data = request.get_json()
      db = get_db()

      try:
        # create a new post
        newPost = Post(
          title = data['title'],
          post_url = data['post_url'],
          user_id = session.get('user_id')
        )

        db.add(newPost)
        db.commit()
      except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post failed'), 500

      return jsonify(id = newPost.id)


# route for updating posts
@bp.route('/posts/<id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    db = get_db()

    try:
      # retrieve post and update title property
      post = db.query(Post).filter(Post.id == id).one()
      post.title = data['title']
      db.commit()
    except:
      print(sys.exc_info()[0])

      db.rollback()
      return jsonify(message = 'Post not found'), 404

    return '', 204


# route for deleting posts
@bp.route('/posts/<id>', methods=['DELETE'])
def delete(id):
    db = get_db()

    try:
      # delete post from db
      db.delete(db.query(Post).filter(Post.id == id).one())
      db.commit()
    except:
      print(sys.exc_info()[0])

      db.rollback()
      return jsonify(message = 'Post not found'), 404

    return '', 204