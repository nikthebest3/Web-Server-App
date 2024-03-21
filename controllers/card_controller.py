from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.card import Card, cards_schema, card_schema
from models.user import User

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

@cards_bp.route('/')
def get_all_cards():
  stmt = db.select(Card).order_by(Card.date.desc())
  cards = db.session.scalars(stmt)
  return cards_schema.dump(cards)

# Comment Card ID 
@cards_bp.route('/<int:commentcard_id>')
def get_one_card(commentcard_id):
  stmt = db.select(Card).filter_by(id=commentcard_id)
  card = db.session.scalar(stmt)
  if card:
    return card_schema.dump(card)
  else:
    return {"error": f"Comment Card with id {commentcard_id} not found"}, 404
  
  
@cards_bp.route('/', methods=["POST"])
@jwt_required()
def create_commentcard():
  body_data = card_schema.load(request.get_json())
  card = Card(
    title = body_data.get('title'),
    description = body_data.get('description'),
    date = date.today(),
    user_id = get_jwt_identity()
  )
  db.session.add(card)
  db.session.commit()
  
  return card_schema.dump(card), 201

@cards_bp.route("/<int:commentcard_id>", methods=['DELETE'])
@jwt_required()
def delete_card(commentcard_id):
  
  stmt = db.select(Card).where(Card.id == commentcard_id)
  card = db.session.scalar(stmt)
  
  if card:
    if str(card.user_id) != get_jwt_identity():
      return {"error": "Only the owner can delete the comment"}, 403
    db.session.delete(card)
    db.session.commit()
    return {"message": f"Comment '{card.title}' has been deleted"}
  else:
    return {"error": f"Comment with id {commentcard_id} not found"}, 404
  
@cards_bp.route('/<int:commentcard_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_commentcard(commentcard_id):
  
  body_data = request.get_json()
  
  stmt = db.select(Card).filter_by(id=commentcard_id)
  card = db.session.scalar(stmt)
  
  if card:
    if str(card.user_id) != get_jwt_identity():
      return {"error": "Only the owner can edit the comment"}, 403
    card.title = body_data.get('title') or card.title 
    card.description = body_data.get('description') or card.description
    db.session.commit()
    return card_schema.dump(card)
  else:
    return {"error": f"Comment with id {commentcard_id} not found"}, 404
  

def users_admin_status():
  user_id = get_jwt_identity()
  stmt = db.select(User).filter_by(id=user_id)
  user = db.session.scalar(stmt)
  return user.is_admin