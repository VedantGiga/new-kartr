#!/usr/bin/env python
import os
import shutil
import sys

print("Setting up application for Render deployment...")
print("Current working directory:", os.getcwd())
print("Directory contents:", os.listdir())

# Check if Influencer_kartr_personal exists
if os.path.exists('Influencer_kartr_personal'):
    print("Influencer_kartr_personal directory found")
    
    # List of files to copy to the root directory
    files_to_copy = [
        'app.py',
        'routes.py',
        'models.py',
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
    
    # Copy each file if it exists
    for file in files_to_copy:
        source_path = os.path.join('Influencer_kartr_personal', file)
        if os.path.exists(source_path):
            print(f"Copying {file} to root directory")
            shutil.copy(source_path, file)
        else:
            print(f"Warning: {file} not found in Influencer_kartr_personal")
    
    # Copy directories
    dirs_to_copy = [
        'templates',
        'static',
        'data'
    ]
    
    for directory in dirs_to_copy:
        source_dir = os.path.join('Influencer_kartr_personal', directory)
        if os.path.exists(source_dir):
            print(f"Copying directory {directory} to root")
            if os.path.exists(directory):
                shutil.rmtree(directory)
            shutil.copytree(source_dir, directory)
        else:
            print(f"Warning: Directory {directory} not found in Influencer_kartr_personal")
    
    print("Setup complete!")
else:
    print("Warning: Influencer_kartr_personal directory not found")
    print("Checking if necessary files already exist in root directory...")
    
    required_files = ['app.py', 'routes.py', 'models.py']
    missing_files = [file for file in required_files if not os.path.exists(file)]
    
    if missing_files:
        print(f"Error: Missing required files: {', '.join(missing_files)}")
        print("Cannot continue setup")
        sys.exit(1)
    else:
        print("All required files found in root directory")
        print("Setup complete!")
