import os
import sys
import logging
import shutil
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

# Print debug information
print("Current working directory:", os.getcwd())
print("Directory contents:", os.listdir())

# Check if we're in the root directory or Influencer_kartr_personal
if os.path.exists('Influencer_kartr_personal'):
    # We're in the root directory, add Influencer_kartr_personal to path
    sys.path.insert(0, os.path.abspath('Influencer_kartr_personal'))
    
    # Copy necessary files if they don't exist
    files_to_copy = [
        'models.py',
        'routes.py',
        'forms.py',
        'youtube_api.py',
        'youtube_utils.py',
        'email_utils.py',
        'auth0_config.py',
        'rag_ques.py',
        'virtual_influencer.py',
        'social_media_agents.py',
        'demo.py',
        'graph.py'
    ]
    
    for file in files_to_copy:
        source_path = os.path.join('Influencer_kartr_personal', file)
        if os.path.exists(source_path) and not os.path.exists(file):
            print(f"Copying {file} to root directory")
            shutil.copy(source_path, file)
    
    # Copy directories
    dirs_to_copy = [
        'templates',
        'static',
        'data'
    ]
    
    for directory in dirs_to_copy:
        source_dir = os.path.join('Influencer_kartr_personal', directory)
        if os.path.exists(source_dir) and not os.path.exists(directory):
            print(f"Copying directory {directory} to root")
            shutil.copytree(source_dir, directory)

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "kartr_secret_key_for_development")

# Configure database - for development using SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///kartr.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Set YouTube API key from environment variable
app.config["YOUTUBE_API_KEY"] = os.environ.get("YOUTUBE_API_KEY", "")

# Import email configuration if available
try:
    from config import EMAIL_CONFIG
    # Set email configuration in app config
    app.config["EMAIL_USER"] = os.environ.get("EMAIL_USER", EMAIL_CONFIG.get("EMAIL_USER", ""))
    app.config["EMAIL_PASSWORD"] = os.environ.get("EMAIL_PASSWORD", EMAIL_CONFIG.get("EMAIL_PASSWORD", ""))
except ImportError:
    # No config file found, use environment variables only
    app.config["EMAIL_USER"] = os.environ.get("EMAIL_USER", "")
    app.config["EMAIL_PASSWORD"] = os.environ.get("EMAIL_PASSWORD", "")

# Initialize the database with the app
db.init_app(app)

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Import models and create tables
with app.app_context():
    try:
        from models import User
        db.create_all()
        logger.debug("Database tables created")
    except ImportError:
        logger.error("Could not import models. Make sure models.py is in the current directory or Python path.")

# Load user from user ID (required by Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    try:
        from models import User
        return User.query.get(int(user_id))
    except ImportError:
        logger.error("Could not import User model")
        return None

# --------------------------------------
# API Route: Toggle Email Visibility
# --------------------------------------
@app.route('/api/toggle-email-visibility', methods=['POST'])
@login_required
def toggle_email_visibility():
    """API endpoint to toggle email visibility setting"""
    try:
        data = request.get_json()
        if not data or "email_visible" not in data:
            return jsonify({"error": "Invalid data"}), 400

        is_visible = data["email_visible"]
        
        # Update the database model
        current_user.email_visible = is_visible
        db.session.commit()
        
        # Update the CSV file
        try:
            from youtube_utils import update_email_visibility
            success = update_email_visibility(current_user.email, is_visible)
            
            if success:
                logger.debug(f"Email visibility set to: {is_visible}")
                return jsonify({"success": True, "email_visible": is_visible}), 200
            else:
                # Rollback the database change if CSV update failed
                current_user.email_visible = not is_visible
                db.session.commit()
                return jsonify({"success": False, "message": "Failed to update email visibility in CSV file"}), 500
        except ImportError:
            logger.error("Could not import youtube_utils")
            return jsonify({"error": "Server configuration error"}), 500
    except Exception as e:
        logger.error(f"Error in toggle-email-visibility: {e}")
        return jsonify({"error": f"Something went wrong: {str(e)}"}), 500

# --------------------------------------
# Optional: Handle 404 errors with JSON
# --------------------------------------
@app.errorhandler(404)
def not_found(e):
    return jsonify(error="Not found"), 404
