from flask import Blueprint, render_template, jsonify
import speedtest
import statistics
import time
import logging

speedtest_app = Blueprint('speedtest_app', __name__, template_folder='templates')

# Function to measure jitter with a limited number of pings
def measure_jitter(st, server, num_pings=3):
    pings = []
    for _ in range(num_pings):
        st.get_best_server([server])
        ping = st.results.ping
        pings.append(ping)
        time.sleep(0.5) 
    jitter = statistics.stdev(pings) if len(pings) > 1 else None  # Calculate jitter
    return jitter

logging.basicConfig(level=logging.DEBUG)

# Run speed test with performance optimizations
def run_speed_test():
    st = speedtest.Speedtest()
    
    try:
        logging.debug("Fetching best server...")
        st.get_best_server() 
        logging.debug("Best server found.")

        # Run the speed test using multithreading for faster results
        logging.debug("Running download speed test...")
        download = st.download(threads=4) / 1e6  # Convert to Mbps
        logging.debug(f"Download speed: {download} Mbps")

        logging.debug("Running upload speed test...")
        upload = st.upload(threads=4) / 1e6  # Convert to Mbps
        logging.debug(f"Upload speed: {upload} Mbps")

        ping = st.results.ping

        # Measure jitter
        jitter = measure_jitter(st, st.results.server)

        # Collect server info for transparency
        server_info = {
            'name': st.results.server['sponsor'],
            'location': f"{st.results.server['name']}, {st.results.server['country']}",
            'ping': ping,
            'jitter': jitter
        }
        return download, upload, ping, jitter, server_info

    except speedtest.ConfigRetrievalError as e:
        logging.error("Config retrieval error: %s", e)
        return jsonify(error=str(e)), 500  # Return error message and status code
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
        return jsonify(error="An error occurred while running the speed test."), 500

@speedtest_app.route('/')
def index():
    return render_template('speedtest.html')

@speedtest_app.route('/start-test', methods=['GET'])
def start_test():
    download, upload, ping, jitter, server_info = run_speed_test()
    return jsonify(download=download, upload=upload, ping=ping, jitter=jitter, server_info=server_info)