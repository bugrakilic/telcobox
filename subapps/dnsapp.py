from flask import Blueprint, render_template, request
import dns.resolver

dns_lookup_app = Blueprint('dns_lookup_app', __name__, template_folder='templates')

# DNS lookup function for all record types
def dns_lookup_all(domain):
    record_types = ["A", "AAAA", "MX", "TXT", "CNAME", "NS"]
    result = {}
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            result[record_type] = [str(answer) for answer in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
            result[record_type] = ["No records found or an error occurred."]
    return result

@dns_lookup_app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    domain = ''
    if request.method == 'POST':
        domain = request.form.get('domain')
        if domain:
            result = dns_lookup_all(domain)
    return render_template('dns_lookup.html', domain=domain, result=result)
