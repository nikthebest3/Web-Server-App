from flask import Blueprint
from init import db, bcrypt
from models.user import User

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_comment():
  db.create_all()
  print("Comment Page Created")
  
@db_commands.cli.command('drop')
def drop_comment():
  db.drop_all()
  print("Comment Page Dropped")
  
@db_commands.cli.command('seed')
def seed_page():
  users = [
    User(
      email="admin@email.com",
      password=bcrypt.generate_password_hash('123456').decode('utf-8'),
      is_admin=True
    ),
    User(
      name="User 1",
      email="user1@email.com",
      password=bcrypt.generate_password_hash('123456').decode('utf-8')
    )
  ]
  
  db.session.add_all(users)
  db.session.commit()
  
  print("Comment Page Seeded")