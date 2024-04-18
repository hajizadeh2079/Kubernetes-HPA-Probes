from flask import Flask, jsonify
import time
import random

app = Flask(__name__)

healthy = True

@app.route('/increase_cpu')
def increase_cpu():
    start_time = time.time()
    while time.time() - start_time < 120:  # Run for 2 minutes
        # Simulate CPU-intensive operations
        result = 0
        for _ in range(1000000):
            result += random.random()
    return 'CPU usage increased for 2 minutes.\n'

@app.route('/increase_memory')
def increase_memory():
    memory_usage = []
    for _ in range(200):
        # Simulate memory allocation
        data = '*' * 1024 * 1024  # Allocate 1 MB of memory
        memory_usage.append(data)
    time.sleep(120)
    return 'Memory usage increased for 2 minutes.\n'

@app.route('/set_health_false')
def set_health_false():
    global healthy
    healthy = False
    return 'Health status set to False.\n'

@app.route('/health')
def health_check():
    global healthy
    if healthy:
        return jsonify({'status': 'ok'}), 200
    else:
        return jsonify({'status': 'error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
