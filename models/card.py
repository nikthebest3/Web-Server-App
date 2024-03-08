from init import db, ma
from marshmallow import fields 

class Card(db.Model):
  __tablename__ = "Comment Cards"
  
  title = db.Column(db.String(100))
  description = db.Column(db.Text)
  # user = db.Column(db.String) # Who created the comment 
  date = db.Column(db.Date) # Date when comment was made/created
  
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Who created the comment 
  
  user = db.relationship('User', back_populatres='cards')
  
class CardSchema(ma.Schema):
  
  user = fields.Nested('UserSchema', only = ['name', 'email'])
  
  class Meta:
    fields = ('title', 'description', 'date', 'user')
    
card_schema = CardSchema()
cards_schema = CardSchema(many=True)