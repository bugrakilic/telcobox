from flask import render_template, request, Blueprint

data_calculator_app = Blueprint('data_calculator_app', __name__)

def calculate_download_time(data_size, data_unit, speed, speed_unit):
    # Converting data size to bits
    if data_unit == "GB":
        data_size_bits = data_size * 8 * 1e9  # GB to bits
    else:
        data_size_bits = data_size * 8 * 1e6  # MB to bits

    # Converting speed to bits per second
    if speed_unit == "Gbps":
        speed_bps = speed * 1e9  # Gbps to bps
    else:
        speed_bps = speed * 1e6  # Mbps to bps

    time_seconds = data_size_bits / speed_bps
    minutes = int(time_seconds // 60)
    seconds = int(time_seconds % 60)

    return minutes, seconds

@data_calculator_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data_size = float(request.form.get('data_size'))
        data_unit = request.form.get('data_unit')
        speed = float(request.form.get('speed'))
        speed_unit = request.form.get('speed_unit')
        minutes, seconds = calculate_download_time(data_size, data_unit, speed, speed_unit)
        return render_template('data_calculator.html', data_size=data_size, data_unit=data_unit,
                               speed=speed, speed_unit=speed_unit, minutes=minutes, seconds=seconds)
    return render_template('data_calculator.html', data_size='', data_unit='GB', speed='', speed_unit='Mbps')
