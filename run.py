from flask import Flask, render_template
from subapps.dnsapp import dns_lookup_app
from subapps.ipcalapp import ip_subnet_app
from subapps.myipapp import whats_my_ip_app
from subapps.pingapp import ping_latency_app
from subapps.speedapp import speedtest_app
from subapps.raidapp import raid_app
from subapps.datacalcapp import data_calculator_app
from subapps.bytecalcapp import byte_calculator_app
from subapps.sslapp import ssl_checker_app

app = Flask(__name__)

# Register the dns_lookup_app Blueprint with URL prefixes. 
app.register_blueprint(dns_lookup_app, url_prefix='/dns-lookup')
app.register_blueprint(ip_subnet_app, url_prefix='/ipsubnet-calculator')
app.register_blueprint(whats_my_ip_app, url_prefix='/whats-my-ip')
app.register_blueprint(ping_latency_app, url_prefix='/ping-latency-checker')
app.register_blueprint(speedtest_app, url_prefix='/speedtest')
app.register_blueprint(raid_app, url_prefix='/raid-calculator')
app.register_blueprint(data_calculator_app, url_prefix='/data-calculator')
app.register_blueprint(byte_calculator_app, url_prefix='/byte-calculator')
app.register_blueprint(ssl_checker_app, url_prefix='/ssl-checker')

# Define routes for the main app
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)