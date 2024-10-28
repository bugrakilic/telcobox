import requests
from flask import Blueprint, render_template, request

ping_latency_app = Blueprint('ping_latency_app', __name__, template_folder='templates')

# Function to ping a host via HTTP
def ping_host(host):
    try:
        # Send a simple HTTP GET request to the host
        response = requests.get(f'http://{host}', timeout=2)
        return f"HTTP Response Code: {response.status_code}, Response Time: {response.elapsed.total_seconds() * 1000:.2f} ms"
    except requests.RequestException as e:
        return f"Ping failed: {str(e)}"

@ping_latency_app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        host = request.form.get('host')
        result = ping_host(host)
    return render_template('ping_latency.html', result=result)
