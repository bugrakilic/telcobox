import requests
import socket
from flask import Blueprint, render_template, request

ping_latency_app = Blueprint('ping_latency_app', __name__, template_folder='templates')

# Function to ping a host via HTTP
def ping_host(host):
    try:
        response = requests.get(f'http://{host}', timeout=2)
        latency = f"HTTP Response Code: {response.status_code}, Response Time: {response.elapsed.total_seconds() * 1000:.2f} ms"
        return latency
    except requests.RequestException as e:
        return f"Ping failed: {str(e)}"

# Function to resolve a domain to an IP address
def get_ip_from_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

# Function to get IP information using ipinfo.io
def get_ip_info(ip):
    url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(url)
        data = response.json()
        return f"IP: {data.get('ip')}\nISP: {data.get('org')}\nLocation: {data.get('city')}, {data.get('region')}, {data.get('country')}"
    except requests.RequestException as e:
        return f"IP Lookup failed: {str(e)}"

@ping_latency_app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    checked_domain = None

    if request.method == 'POST':
        checked_domain = request.form.get('host')

        # Step 1: Ping the domain
        ping_result = ping_host(checked_domain)

        # Step 2: Get IP address from domain
        ip_address = get_ip_from_domain(checked_domain)
        if ip_address:
            ip_info = get_ip_info(ip_address)
            result = f"{ping_result}\n\nResolved IP: {ip_address}\n\n{ip_info}"
        else:
            result = f"{ping_result}\n\nFailed to resolve IP address."

    return render_template('ping_latency.html', result=result, checked_domain=checked_domain)

