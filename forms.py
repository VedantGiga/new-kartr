import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Print debug information
print("Importing forms.py")
print("Current working directory:", os.getcwd())

# Try to import Flask-WTF
try:
    from flask_wtf import FlaskForm
    from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
    from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL
    print("Successfully imported Flask-WTF and WTForms")
except ImportError as e:
    logger.error(f"Error importing Flask-WTF: {e}")
    raise

# Check if Influencer_kartr_personal/forms.py exists
if os.path.exists('Influencer_kartr_personal/forms.py'):
    print("Found Influencer_kartr_personal/forms.py, importing forms from there")
    
    # Add Influencer_kartr_personal to Python path if not already there
    influencer_path = os.path.abspath('Influencer_kartr_personal')
    if influencer_path not in sys.path:
        sys.path.insert(0, influencer_path)
    
    # Import all forms from Influencer_kartr_personal/forms.py
    try:
        from Influencer_kartr_personal.forms import RegistrationForm, LoginForm, YouTubeStatsForm, YouTubeDemoForm, ForgotPasswordForm, OTPVerificationForm
        print("Successfully imported forms from Influencer_kartr_personal/forms.py")
        
        # Re-export the forms
        __all__ = ['RegistrationForm', 'LoginForm', 'YouTubeStatsForm', 'YouTubeDemoForm', 'ForgotPasswordForm', 'OTPVerificationForm']
    except ImportError as e:
        logger.error(f"Error importing forms from Influencer_kartr_personal/forms.py: {e}")
        
        # Define basic forms
        class RegistrationForm(FlaskForm):
            username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
            email = StringField('Email', validators=[DataRequired(), Email()])
            password = PasswordField('Password', validators=[DataRequired()])
            confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
            user_type = SelectField('Account Type', choices=[('influencer', 'Influencer'), ('sponsor', 'Sponsor')], validators=[DataRequired()])
            submit = SubmitField('Sign Up')

        class LoginForm(FlaskForm):
            email = StringField('Email', validators=[DataRequired(), Email()])
            password = PasswordField('Password', validators=[DataRequired()])
            remember = BooleanField('Remember Me')
            submit = SubmitField('Login')

        class YouTubeStatsForm(FlaskForm):
            youtube_url = StringField('YouTube Channel URL', validators=[DataRequired(), URL()])
            submit = SubmitField('Get Stats')

        class YouTubeDemoForm(FlaskForm):
            youtube_url = StringField('YouTube Video URL', validators=[DataRequired(), URL()])
            submit = SubmitField('Analyze Video')

        class ForgotPasswordForm(FlaskForm):
            email = StringField('Email', validators=[DataRequired(), Email()])
            submit = SubmitField('Send OTP')

        class OTPVerificationForm(FlaskForm):
            otp = StringField('OTP', validators=[DataRequired(), Length(min=6, max=6)])
            new_password = PasswordField('New Password', validators=[DataRequired()])
            confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
            submit = SubmitField('Reset Password')
else:
    logger.error("Could not find Influencer_kartr_personal/forms.py")
    
    # Define basic forms
    class RegistrationForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
        email = StringField('Email', validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
        user_type = SelectField('Account Type', choices=[('influencer', 'Influencer'), ('sponsor', 'Sponsor')], validators=[DataRequired()])
        submit = SubmitField('Sign Up')

    class LoginForm(FlaskForm):
        email = StringField('Email', validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        remember = BooleanField('Remember Me')
        submit = SubmitField('Login')

    class YouTubeStatsForm(FlaskForm):
        youtube_url = StringField('YouTube Channel URL', validators=[DataRequired(), URL()])
        submit = SubmitField('Get Stats')

    class YouTubeDemoForm(FlaskForm):
        youtube_url = StringField('YouTube Video URL', validators=[DataRequired(), URL()])
        submit = SubmitField('Analyze Video')

    class ForgotPasswordForm(FlaskForm):
        email = StringField('Email', validators=[DataRequired(), Email()])
        submit = SubmitField('Send OTP')

    class OTPVerificationForm(FlaskForm):
        otp = StringField('OTP', validators=[DataRequired(), Length(min=6, max=6)])
        new_password = PasswordField('New Password', validators=[DataRequired()])
        confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
        submit = SubmitField('Reset Password')
