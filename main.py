import sys
import os

# Print debug information
print("Current working directory:", os.getcwd())
print("Directory contents:", os.listdir())

# Try different paths to find the app module
possible_paths = [
    os.path.abspath('Influencer_kartr_personal'),
    os.path.abspath('.'),
    os.path.abspath('..'),
]

# Add all possible paths to Python path
for path in possible_paths:
    if path not in sys.path:
        sys.path.insert(0, path)
    print(f"Added {path} to Python path")

# Try to import the app
try:
    # First try direct import
    from app import app
    import routes  # noqa: F401
    print("Successfully imported app directly")
except ImportError:
    try:
        # Then try from Influencer_kartr_personal
        if os.path.exists('Influencer_kartr_personal'):
            sys.path.insert(0, os.path.abspath('Influencer_kartr_personal'))
            from app import app
            import routes  # noqa: F401
            print("Successfully imported app from Influencer_kartr_personal")
        else:
            # Copy app.py and routes.py to current directory if they don't exist
            if not os.path.exists('app.py') and os.path.exists('Influencer_kartr_personal/app.py'):
                import shutil
                shutil.copy('Influencer_kartr_personal/app.py', 'app.py')
                shutil.copy('Influencer_kartr_personal/routes.py', 'routes.py')
                from app import app
                import routes  # noqa: F401
                print("Copied app.py and routes.py to current directory")
            else:
                raise ImportError("Could not find app module")
    except ImportError as e:
        print(f"Error importing app: {e}")
        raise

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
