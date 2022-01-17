from flask import Flask, jsonify, request, Response, render_template
import csv
import json
import time
import requests
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET','POST'])
def view():
    if request.method == 'POST':
        data = {
            'H': int(request.form.get('H')),
            'U': int(request.form.get('U')),
            'D': int(request.form.get('D')),
            'F': int(request.form.get('F'))
        }
        result = requests.post('http://localhost:5000/snail', json=data)
    else:
        result = None

    api = read_attempts()
    return render_template('index.html', method=request.method, data=api.json, result=result)

@app.route('/snail', methods=['GET'])
def read_attempts():
    with open('results.csv', 'r') as f:
        data = [
            {
                k: v
                for k, v in row.items()
            }
            for row in csv.DictReader(f, skipinitialspace=True)
        ]

    return jsonify(data)

@app.route('/snail', methods=['POST'])
def run_simulation():
    if request.headers.get('Content-Type') != 'application/json':
        return Response('{"error": "Unsupport content type"}', status=500, mimetype='application/json')

    fields = ('H', 'U', 'D', 'F')
    if not all(key in request.json for key in fields):
        return Response('{"error": "Missing fields"}', status=500, mimetype='application/json')

    if not all(isinstance(request.json[key], int) for key in request.json if key in fields) or not all(request.json[key] > 0 for key in request.json if key in fields) or request.json.get('F') > 100:
        return Response('{"error": "Invalid input"}', status=500, mimetype='application/json')

    try:
        escape_height = int(request.json.get('H'))
        original_climb_distance = int(request.json.get('U'))
        slide_distance = int(request.json.get('D'))
        fatigue_factor_percentage = int(request.json.get('F'))

        current_height = 0
        current_climb_distance = original_climb_distance
        day = 0
        isEscaped = None

        while isEscaped is None:
            day += 1

            # day phase
            current_height += current_climb_distance

            if current_height >= escape_height:
                isEscaped = True
            else:
                # night phase
                current_height -= slide_distance
                current_climb_distance -= (original_climb_distance * fatigue_factor_percentage / 100)

                if current_height <= 0:
                    isEscaped = False

                if current_climb_distance < 0:
                    current_climb_distance = 0

        result = f'{"success" if isEscaped else "failure"} on day {day}'

        with open('results.csv', 'a', newline='') as f:
            handler = csv.writer(f)
            handler.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), escape_height, original_climb_distance, slide_distance, fatigue_factor_percentage, result])
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=500, mimetype='application/json')

    return Response(
        json.dumps({
            'H': escape_height,
            'U': original_climb_distance,
            'D': slide_distance,
            'F': fatigue_factor_percentage,
            'result': result
        }), 
        status=201, 
        mimetype='application/json'
    )

app.run()
