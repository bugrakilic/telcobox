from flask import Blueprint, render_template, request

raid_app = Blueprint('raid_app', __name__, template_folder='templates')

# Function to RAID calculation 
def calculate_raid(num_disks, disk_size, raid_level):
    total_capacity = 0
    redundancy = 0
    performance = ""

    if raid_level == "0":
        total_capacity = num_disks * disk_size
        performance = (
            "Highest performance through data striping across all disks. "
            "Offers maximum read/write speeds but NO data protection - "
            "if any drive fails, all data is lost. "
            f"Requires minimum {2 if num_disks < 2 else num_disks} drives."
        )
    elif raid_level == "1":
        total_capacity = disk_size
        redundancy = 1
        performance = (
            "Complete data redundancy through mirroring. "
            "Good read performance with slightly slower writes. "
            "Can survive failure of half of the drives as long as a mirror pair remains. "
            f"Usable capacity is {disk_size}GB (50% of total raw capacity). "
            "Minimum 2 drives required."
        )
    elif raid_level == "5":
        total_capacity = (num_disks - 1) * disk_size
        redundancy = 1
        performance = (
            "Balanced solution with distributed parity. "
            "Good read performance, write performance significantly impacted by parity calculations. "
            f"Can survive {redundancy} drive failure. "
            f"Requires minimum {3 if num_disks < 3 else num_disks} drives. "
            f"Usable capacity is {total_capacity}GB ({(total_capacity/(num_disks * disk_size)*100):.1f}% of total raw capacity)."
        )
    elif raid_level == "6":
        total_capacity = (num_disks - 2) * disk_size
        redundancy = 2
        performance = (
            "Enhanced reliability with double distributed parity. "
            "Good read performance, significantly lower write speed due to double parity calculations. "
            f"Can survive {redundancy} simultaneous drive failures. "
            f"Requires minimum {4 if num_disks < 4 else num_disks} drives. "
            f"Usable capacity is {total_capacity}GB ({(total_capacity/(num_disks * disk_size)*100):.1f}% of total raw capacity)."
        )
    elif raid_level == "10":
        total_capacity = (num_disks // 2) * disk_size
        redundancy = 1
        performance = (
            "Combines mirroring (RAID 1) and striping (RAID 0). "
            "Excellent read/write performance with good redundancy. "
            "Can survive up to half of the total drives failing if at least one drive in each mirror pair remains functional. "
            f"Requires minimum 4 drives. "
            f"Usable capacity is {total_capacity}GB (50% of total raw capacity)."
        )

    return {
        'num_disks': num_disks,
        'disk_size': disk_size,
        'raid_level': raid_level,
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