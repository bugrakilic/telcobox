from flask import Flask, render_template, request, Blueprint

# Initialize Flask app and Blueprint
app = Flask(__name__)
data_calculator_app = Blueprint('data_calculator_app', __name__)

# Function to calculate download time
def calculate_download_time(data_size, data_unit, speed, speed_unit):
    # Convert data size to bits
    if data_unit == "GB":
        data_size_bits = data_size * 8 * 1e9  # GB to bits
    else:
        data_size_bits = data_size * 8 * 1e6  # MB to bits

    # Convert speed to bits per second
    if speed_unit == "Gbps":
        speed_bps = speed * 1e9  # Gbps to bps
    else:
        speed_bps = speed * 1e6  # Mbps to bps

    # Calculate time in seconds and convert to minutes and seconds
    time_seconds = data_size_bits / speed_bps
    minutes = int(time_seconds // 60)
    seconds = int(time_seconds % 60)

    return minutes, seconds

# Route for the data calculator
@data_calculator_app.route('/', methods=['GET', 'POST'])
def index():
    # Default values for rendering the template
    data_size = None
    data_unit = 'GB'
    speed = None
    speed_unit = 'Mbps'
    minutes = None
    seconds = None

    if request.method == 'POST':
        # Get form input
        data_size = float(request.form.get('data_size'))
        data_unit = request.form.get('data_unit')
        speed = float(request.form.get('speed'))
        speed_unit = request.form.get('speed_unit')

        # Perform calculation
        minutes, seconds = calculate_download_time(data_size, data_unit, speed, speed_unit)

    return render_template(
        'data_calculator.html',
        data_size=data_size,
        data_unit=data_unit,
        speed=speed,
        speed_unit=speed_unit,
        minutes=minutes,
        seconds=seconds
    )

# Register Blueprint and run the app
app.register_blueprint(data_calculator_app, url_prefix='/')
if __name__ == '__main__':
    app.run(debug=True)
