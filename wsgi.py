import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

# Add the Influencer_kartr_personal directory to the Python path if it exists
if os.path.exists('Influencer_kartr_personal'):
    sys.path.insert(0, os.path.abspath('Influencer_kartr_personal'))

# Try to import the app
try:
    from Influencer_kartr_personal.app import app
except ImportError:
    try:
        from app import app
    except ImportError:
        # If app.py doesn't exist in the current directory, copy it from Influencer_kartr_personal
        if not os.path.exists('app.py') and os.path.exists('Influencer_kartr_personal/app.py'):
            import shutil
            print("Copying app.py from Influencer_kartr_personal")
            shutil.copy('Influencer_kartr_personal/app.py', 'app.py')
            shutil.copy('Influencer_kartr_personal/routes.py', 'routes.py')
            from app import app
        else:
            raise ImportError("Could not find app module")

# Import routes to register them with the app
try:
    import Influencer_kartr_personal.routes
except ImportError:
    try:
        import routes
    except ImportError:
        print("Warning: Could not import routes")

# This is the WSGI application object that Gunicorn will use
application = app
