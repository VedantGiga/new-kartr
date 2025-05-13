import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Print debug information
print("Importing routes.py")
print("Current working directory:", os.getcwd())

# Try to import from app
try:
    from app import app, db
    print("Successfully imported app and db from app")
except ImportError as e:
    logger.error(f"Error importing app: {e}")
    raise

# Try to import models
try:
    from models import User, YouTubeChannel, Search
    print("Successfully imported models")
except ImportError as e:
    logger.error(f"Error importing models: {e}")
    raise

# Try to import forms
try:
    from forms import RegistrationForm, LoginForm, YouTubeStatsForm, YouTubeDemoForm, ForgotPasswordForm, OTPVerificationForm
    print("Successfully imported forms")
except ImportError as e:
    logger.error(f"Error importing forms: {e}")
    # This is not critical, so we'll continue

# Try to import other modules
try:
    from flask import render_template, url_for, flash, redirect, request, jsonify, session
    from flask_login import login_user, current_user, logout_user, login_required
    from youtube_api import get_video_stats, get_channel_stats, extract_video_info
    from youtube_utils import save_user_to_csv, validate_user_login, save_analysis_to_csv
    from googleapiclient.discovery import build
    from email_utils import generate_otp, store_otp, verify_otp, send_otp_email
    print("Successfully imported other modules")
except ImportError as e:
    logger.error(f"Error importing other modules: {e}")
    # This is not critical, so we'll continue

# Check if Influencer_kartr_personal/routes.py exists
if os.path.exists('Influencer_kartr_personal/routes.py'):
    print("Found Influencer_kartr_personal/routes.py, importing routes from there")
    
    # Add Influencer_kartr_personal to Python path if not already there
    influencer_path = os.path.abspath('Influencer_kartr_personal')
    if influencer_path not in sys.path:
        sys.path.insert(0, influencer_path)
    
    # Import all routes from Influencer_kartr_personal/routes.py
    try:
        from Influencer_kartr_personal.routes import *
        print("Successfully imported routes from Influencer_kartr_personal/routes.py")
    except ImportError as e:
        logger.error(f"Error importing routes from Influencer_kartr_personal/routes.py: {e}")
        
        # Try to define basic routes
        @app.route('/')
        def home():
            return render_template('landing.html', title='Kartr - Connect Influencers and Sponsors')
        
        @app.route('/login')
        def login():
            return render_template('login.html', title='Login')
        
        @app.route('/register')
        def register():
            return render_template('register.html', title='Register')
else:
    logger.error("Could not find Influencer_kartr_personal/routes.py")
    
    # Define basic routes
    @app.route('/')
    def home():
        return render_template('landing.html', title='Kartr - Connect Influencers and Sponsors')
    
    @app.route('/login')
    def login():
        return render_template('login.html', title='Login')
    
    @app.route('/register')
    def register():
        return render_template('register.html', title='Register')
