import os
import sys

print("Current working directory:", os.getcwd())
print("Python path:", sys.path)
print("Directory contents:", os.listdir())

# Check if Influencer_kartr_personal exists
if os.path.exists('Influencer_kartr_personal'):
    print("Influencer_kartr_personal exists")
    print("Contents:", os.listdir('Influencer_kartr_personal'))
else:
    print("Influencer_kartr_personal does not exist")

# Check if app.py exists in the current directory
if os.path.exists('app.py'):
    print("app.py exists in current directory")
else:
    print("app.py does not exist in current directory")
