import random
from flask import Flask, jsonify, render_template, request
from time import sleep
from threading import Thread

app = Flask(__name__)

task_completed = False
result = None

# Simulating a long-running task
def long_running_task():
    global task_completed, result
    sleep(10)  # Simulate 10 seconds of work
    result = random.randint(1, 100)  # Generate a random number
    task_completed = True

@app.route('/')
def index():
    return render_template('index.html', task_completed=task_completed, result=result)

@app.route('/start_task', methods=['POST'])
def start_task():
    global task_completed, result
    task_completed = False
    result = None
    Thread(target=long_running_task).start()  # Start the long-running task in a separate thread
    print('done')
    return jsonify({'message': 'Task started.'})

@app.route('/check_task_status')
def check_task_status():
    # Check if the task has completed
    return jsonify({'status': 'completed' if task_completed else 'running'})

@app.route('/get_result')
def get_result():
    # Return the result if the task has completed
    if task_completed:
        return jsonify({'result': result})
    else:
        return jsonify({'result': None})

if __name__ == '__main__':
    # Start the long-running task in a separate thread
    Thread(target=long_running_task).start()

    # Run the Flask app
    app.run(debug=True)