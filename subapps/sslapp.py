from flask import render_template, request, Blueprint
import socket
import ssl
from datetime import datetime

ssl_checker_app = Blueprint('ssl_checker_app', __name__)

def get_ssl_info(hostname):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expiration_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                issuer = dict(x[0] for x in cert['issuer'])
                issuer_name = issuer.get('organizationName', 'Unknown')
                return {
                    'expiration_date': expiration_date,
                    'issuer': issuer_name,
                    'valid': datetime.utcnow() < expiration_date
                }
    except Exception as e:
        return {'error': str(e)}

@ssl_checker_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        hostname = request.form.get('hostname')
        ssl_info = get_ssl_info(hostname)
        return render_template('ssl_checker.html', hostname=hostname, ssl_info=ssl_info)
    return render_template('ssl_checker.html', hostname='', ssl_info=None)
