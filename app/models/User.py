from app.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates

import bcrypt

salt = bcrypt.gensalt()

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(String(50), nullable=False)
  email = Column(String(50), nullable=False, unique=True)
  password = Column(String(100), nullable=False)

  # email validation
  @validates('email')
  def validate_email(self, key, email):
    # this will make sure email address contains @ character
    assert '@' in email

    return email

  # password validation
  @validates('password')
  def validate_password(self,key, password):
    # throw error if password length is fewer than 4 characters
    assert len(password) > 4

    # encrypt password
    return bcrypt.hashpw(password.encode('utf-8'), salt)

  # password verification
  def verify_password(self, password):
    # compare incoming password to the one saved on User object
    return bcrypt.checkpw(
      password.encode('utf-8'),
      self.password.encode('utf-8')
    )