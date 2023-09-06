from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        names = db.session.query(Author.name).all()
        if not name:
            raise ValueError('name attribute is required for author')
        elif name in names:
            raise ValueError('cannot use an existing name')
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if len(number) != 10:
            raise ValueError('phone number has to be 10 digits')
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        clickbaits = ['Won\'t Believe', 'Secret', 'Top', 'Guess']
        if not title:
            raise ValueError('post must include a title')
        if not any(clickbait in title for clickbait in clickbaits):
            raise ValueError('post title must be clickbait-y')
        return title
    
    @validates('content', 'summary')
    def validate_length(self, key, string):
        if key == 'content':
            if len(string) < 250:
                raise ValueError('content must be 250 or more characters')
        if key == 'summary':
            if len(string) >= 250:
                raise ValueError('summary cannot have more than 250 characters')
        return string
    
    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('category must be either "Fiction" or "Non-Fiction"')
        return category
    



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
