from flask import Blueprint, render_template, request

raid_app = Blueprint('raid_app', __name__, template_folder='templates')

# Function to RAID calculation 
def calculate_raid(num_disks, disk_size, raid_level):
    total_capacity = 0
    redundancy = 0
    performance = ""

    if raid_level == "0":
        total_capacity = num_disks * disk_size
        performance = "High performance, no redundancy."
    elif raid_level == "1":
        total_capacity = disk_size
        redundancy = 1
        performance = "Good redundancy, low capacity."
    elif raid_level == "5":
        total_capacity = (num_disks - 1) * disk_size
        redundancy = 1
        performance = "Balanced performance and redundancy."
    elif raid_level == "6":
        total_capacity = (num_disks - 2) * disk_size
        redundancy = 2
        performance = "Higher redundancy."
    elif raid_level == "10":
        total_capacity = (num_disks // 2) * disk_size
        redundancy = 1
        performance = "Good performance and redundancy."

    return {
        'total_capacity': total_capacity,
        'redundancy': redundancy,
        'performance': performance,
    }

@raid_app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        num_disks = int(request.form['num_disks'])
        disk_size = int(request.form['disk_size'])
        raid_level = request.form['raid_level']
        result = calculate_raid(num_disks, disk_size, raid_level)
    return render_template('raid_calculator.html', result=result)