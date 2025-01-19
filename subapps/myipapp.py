import requests
from flask import Blueprint, render_template, request

whats_my_ip_app = Blueprint('whats_my_ip_app', __name__, template_folder='templates')

# Function to get the user's IP address
def get_user_ip():
    return request.remote_addr

# Function to fetch IP details using FreeIPAPI
def get_ip_details(ip):
    url = f"https://freeipapi.com/api/json/{ip}"  # IP is passed into the URL
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {}

@whats_my_ip_app.route('/')
def index():
    # Fetch the user's IP address
    user_ip = get_user_ip()
    
    # Get the IP details using FreeIPAPI
    ip_details = get_ip_details(user_ip)
    
    # Pass the data to the template for rendering
    return render_template('whats_my_ip.html', user_ip=user_ip, ip_details=ip_details)
