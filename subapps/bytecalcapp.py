from flask import render_template, request, Blueprint

byte_calculator_app = Blueprint('byte_calculator_app', __name__)

# Conversion factors for simplicity
UNIT_FACTORS = {
    'bit': 1,
    'byte': 8,
    'KB': 8 * 1024,
    'MB': 8 * 1024 * 1024,
    'GB': 8 * 1024 * 1024 * 1024,
}

def convert_units(amount, from_unit, to_unit):
    # Convert to bits
    bits = amount * UNIT_FACTORS[from_unit]
    # Convert to the target unit
    return bits / UNIT_FACTORS[to_unit]

@byte_calculator_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        from_unit = request.form.get('from_unit')
        to_unit = request.form.get('to_unit')
        
        # Perform the conversion
        result = convert_units(amount, from_unit, to_unit)
        return render_template('byte_calculator.html', amount=amount, from_unit=from_unit, to_unit=to_unit, result=round(result, 2))
    return render_template('byte_calculator.html', amount='', from_unit='', to_unit='', result=None)
