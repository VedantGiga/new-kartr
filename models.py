import os
import sys
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Print debug information
print("Importing models.py")
print("Current working directory:", os.getcwd())

# Try to import from app
try:
    from app import db
    print("Successfully imported db from app")
except ImportError as e:
    logger.error(f"Error importing db from app: {e}")
    raise

# Try to import Flask-Login
try:
    from flask_login import UserMixin
    from werkzeug.security import generate_password_hash, check_password_hash
    print("Successfully imported UserMixin and password hash functions")
except ImportError as e:
    logger.error(f"Error importing UserMixin: {e}")
    raise

# Check if Influencer_kartr_personal/models.py exists
if os.path.exists('Influencer_kartr_personal/models.py'):
    print("Found Influencer_kartr_personal/models.py, importing models from there")
    
    # Add Influencer_kartr_personal to Python path if not already there
    influencer_path = os.path.abspath('Influencer_kartr_personal')
    if influencer_path not in sys.path:
        sys.path.insert(0, influencer_path)
    
    # Import all models from Influencer_kartr_personal/models.py
    try:
        # Import specific models to avoid circular imports
        from Influencer_kartr_personal.models import User, YouTubeChannel, Search
        print("Successfully imported models from Influencer_kartr_personal/models.py")
        
        # Re-export the models
        __all__ = ['User', 'YouTubeChannel', 'Search']
    except ImportError as e:
        logger.error(f"Error importing models from Influencer_kartr_personal/models.py: {e}")
        
        # Define basic models
        class User(UserMixin, db.Model):
            __tablename__ = 'users'
            
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(64), unique=True, nullable=False)
            email = db.Column(db.String(120), unique=True, nullable=False)
            password_hash = db.Column(db.String(256), nullable=False)
            user_type = db.Column(db.String(20), nullable=False)  # 'sponsor' or 'influencer'
            date_registered = db.Column(db.DateTime, default=datetime.utcnow)
            email_visible = db.Column(db.Boolean, default=False)
            
            def set_password(self, password):
                self.password_hash = generate_password_hash(password)
                
            def check_password(self, password):
                return check_password_hash(self.password_hash, password)
            
            def __repr__(self):
                return f'<User {self.username}>'

        class YouTubeChannel(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            channel_id = db.Column(db.String(120), nullable=False)
            title = db.Column(db.String(120), nullable=False)
            subscriber_count = db.Column(db.Integer, nullable=True)
            video_count = db.Column(db.Integer, nullable=True)
            view_count = db.Column(db.Integer, nullable=True)
            date_added = db.Column(db.DateTime, default=datetime.utcnow)
            date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
            user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
            
            def __repr__(self):
                return f'<YouTubeChannel {self.title}>'

        class Search(db.Model):
            __tablename__ = 'searches'
            
            id = db.Column(db.Integer, primary_key=True)
            user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
            search_term = db.Column(db.String(255), nullable=False)
            video_id = db.Column(db.String(20), nullable=True)
            search_type = db.Column(db.String(20), nullable=True)
            date_searched = db.Column(db.DateTime, default=datetime.utcnow)
            
            user = db.relationship('User', backref=db.backref('searches', lazy=True))
            
            def __repr__(self):
                return f'<Search {self.search_term}>'
else:
    logger.error("Could not find Influencer_kartr_personal/models.py")
    
    # Define basic models
    class User(UserMixin, db.Model):
        __tablename__ = 'users'
        
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password_hash = db.Column(db.String(256), nullable=False)
        user_type = db.Column(db.String(20), nullable=False)  # 'sponsor' or 'influencer'
        date_registered = db.Column(db.DateTime, default=datetime.utcnow)
        email_visible = db.Column(db.Boolean, default=False)
        
        def set_password(self, password):
            self.password_hash = generate_password_hash(password)
            
        def check_password(self, password):
            return check_password_hash(self.password_hash, password)
        
        def __repr__(self):
            return f'<User {self.username}>'

    class YouTubeChannel(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        channel_id = db.Column(db.String(120), nullable=False)
        title = db.Column(db.String(120), nullable=False)
        subscriber_count = db.Column(db.Integer, nullable=True)
        video_count = db.Column(db.Integer, nullable=True)
        view_count = db.Column(db.Integer, nullable=True)
        date_added = db.Column(db.DateTime, default=datetime.utcnow)
        date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        
        def __repr__(self):
            return f'<YouTubeChannel {self.title}>'

    class Search(db.Model):
        __tablename__ = 'searches'
        
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        search_term = db.Column(db.String(255), nullable=False)
        video_id = db.Column(db.String(20), nullable=True)
        search_type = db.Column(db.String(20), nullable=True)
        date_searched = db.Column(db.DateTime, default=datetime.utcnow)
        
        user = db.relationship('User', backref=db.backref('searches', lazy=True))
        
        def __repr__(self):
            return f'<Search {self.search_term}>'
