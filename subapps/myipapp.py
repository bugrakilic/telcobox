from flask import Blueprint, render_template, request

whats_my_ip_app = Blueprint('whats_my_ip_app', __name__, template_folder='templates')

# Function to get the user's IP address
def get_user_ip():
    return request.remote_addr

@whats_my_ip_app.route('/')
def index():
    user_ip = get_user_ip()
    return render_template('whats_my_ip.html', user_ip=user_ip)
