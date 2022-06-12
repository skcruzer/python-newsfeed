from app.models import User
from app.db import Session, Base, engine

# drop and rebuild tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

db = Session()

# insert users
db.add_all([
  User(username='kb24goat', email='kobebryant@mail.com', password='password1'),
  User(username='shaqdiesel', email='bigaristotle@mail.com', password='password1'),
  User(username='themagician32', email='therealmj@mail.com', password='password1'),
  User(username='elspaniard', email='paugasol12@mail.com', password='password1'),
  User(username='kareemthedream', email='kajbestever@mail.com', password='password1'),
])

# to run INSERT statements
db.commit()

db.close()