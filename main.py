import sys
import os

# Add the Influencer_kartr_personal directory to the Python path
sys.path.insert(0, os.path.abspath('Influencer_kartr_personal'))

# Import the Flask app
from app import app
import routes  # noqa: F401

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
