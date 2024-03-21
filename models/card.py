from marshmallow import fields
from marshmallow.validate import Length

from init import db, ma
class Card(db.Model):
  __tablename__ = "comment-card"
  
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100))
  description = db.Column(db.Text)
  user = db.Column(db.String) # Who created the comment 
  date = db.Column(db.Date) # Date when comment was made/created
  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Who created the comment 
  
  user = db.relationship('User', back_populates='cards')
  
class CardSchema(ma.Schema):
  
  title = fields.String(required=True, validate=Length(min=2, error="Please enter a title that is atleast 2 characters long"))
  
  user = fields.Nested('UserSchema', only = ['name', 'email'])
  
  class Meta:
    fields = ('id', 'title', 'description', 'date', 'user')
    ordered=True
    
card_schema = CardSchema()
cards_schema = CardSchema(many=True)