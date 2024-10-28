from flask import Blueprint, render_template, request
import dns.resolver

dns_lookup_app = Blueprint('dns_lookup_app', __name__, template_folder='templates')

# DNS lookup function
def dns_lookup(record_type, domain):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [str(answer) for answer in answers]
    except Exception as e:
        return [f"Error: {e}"]

@dns_lookup_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        domain = request.form.get('domain')
        record_type = request.form.get('record_type')
        result = dns_lookup(record_type, domain)
        return render_template('dns_lookup.html', domain=domain, record_type=record_type, result=result)
    return render_template('dns_lookup.html', domain='', record_type='', result=None)
