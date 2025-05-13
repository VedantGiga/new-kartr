# Kartr - Influencer Analytics Platform

## Deployment on Render

This repository is configured for deployment on Render's free tier.

### Prerequisites

- A Render account (https://render.com)
- A GitHub account (for repository hosting)

### Deployment Steps

1. Fork or clone this repository to your GitHub account
2. Remove the Fooocus-main directory if it exists (it's too resource-intensive for free tier)
3. Push the changes to your GitHub repository
4. Log in to your Render account
5. Click "New" and select "Web Service"
6. Connect your GitHub repository
7. Use the following settings:
   - Name: kartr-influencer-app (or your preferred name)
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -c gunicorn_config.py main:app`
8. Add the following environment variables:
   - SESSION_SECRET (generate a random string)
   - AUTH0_DOMAIN
   - AUTH0_CLIENT_ID
   - AUTH0_CLIENT_SECRET
   - AUTH0_API_AUDIENCE
   - YOUTUBE_API_KEY
9. Click "Create Web Service"

### Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with the required environment variables
6. Run the application: `python main.py`

## Features

- YouTube channel analytics
- Influencer and sponsor matching
- Data visualization
- User authentication

## License

[MIT License](LICENSE)
