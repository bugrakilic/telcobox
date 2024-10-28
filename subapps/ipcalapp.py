from flask import Blueprint, render_template, request
import ipaddress

ip_subnet_app = Blueprint('ip_subnet_app', __name__, template_folder='templates')

# Calculating IPv4 subnet details
def calculate_ipv4_subnet(ip, cidr):
    ip_bin = ''.join([f'{int(octet):08b}' for octet in ip.split('.')])
    
    subnet_mask_bin = '1' * cidr + '0' * (32 - cidr)
    subnet_mask = [str(int(subnet_mask_bin[i:i+8], 2)) for i in range(0, 32, 8)]
    
    network_bin = ip_bin[:cidr] + '0' * (32 - cidr)
    network = [str(int(network_bin[i:i+8], 2)) for i in range(0, 32, 8)]
    
    broadcast_bin = ip_bin[:cidr] + '1' * (32 - cidr)
    broadcast = [str(int(broadcast_bin[i:i+8], 2)) for i in range(0, 32, 8)]
    
    first_host_bin = network_bin[:31] + '1'
    first_host = [str(int(first_host_bin[i:i+8], 2)) for i in range(0, 32, 8)]
    
    last_host_bin = broadcast_bin[:31] + '0'
    last_host = [str(int(last_host_bin[i:i+8], 2)) for i in range(0, 32, 8)]
    
    num_hosts = (2 ** (32 - cidr)) - 2
    
    return {
        "ip": ip,
        "cidr": cidr,
        "subnet_mask": ".".join(subnet_mask),
        "network_address": ".".join(network),
        "broadcast_address": ".".join(broadcast),
        "first_host": ".".join(first_host),
        "last_host": ".".join(last_host),
        "num_hosts": num_hosts
    }

# Calculating IPv6 subnet details
def calculate_ipv6_subnet(ip, cidr):
    network = ipaddress.IPv6Network(f'{ip}/{cidr}', strict=False)
    
    return {
        "ip": ip,
        "cidr": cidr,
        "network_address": str(network.network_address),
        "broadcast_address": "N/A (no broadcast in IPv6)",
        "first_host": str(network[1]) if network.num_addresses > 1 else "N/A",
        "last_host": str(network[-2]) if network.num_addresses > 2 else "N/A",
        "num_hosts": network.num_addresses - 2  # -2 for first and last in the range
    }

@ip_subnet_app.route('/', methods=['GET', 'POST'])
def index():
    result_ipv4 = None
    result_ipv6 = None

    if request.method == 'POST':
        if 'ipv4_submit' in request.form:
            ip = request.form['ipv4_ip']
            cidr = int(request.form['ipv4_cidr'])
            result_ipv4 = calculate_ipv4_subnet(ip, cidr)
        elif 'ipv6_submit' in request.form:
            ip = request.form['ipv6_ip']
            cidr = int(request.form['ipv6_cidr'])
            result_ipv6 = calculate_ipv6_subnet(ip, cidr)

    return render_template('ip_calculator.html', result_ipv4=result_ipv4, result_ipv6=result_ipv6)
