# ------------------------- IMPORTS -------------------------
import json
from flask import Flask, jsonify
import random

# ------------------------- CREATE FLASK APPLICATION -------------------------
app = Flask(__name__)

# ------------------------- CREATE DATA -------------------------
competitors = [{'id': 1, 'name': 'David'}, \
               {'id': 2, 'name': 'Jackie'}, \
               {'id': 3, 'name': 'Carmen'}, \
               {'id': 4, 'name': 'Roxy'}, \
               {'id': 5, 'name': 'Gunnar'}
               ]

# ------------------------- HELPER METHOD -------------------------
nextId = len(competitors)

# ------------------------- INDEX (READ / GET) -------------------------
@app.route('/', methods=['GET'])
def index():
    return jsonify(competitors)

# ------------------------- CREATE / POST -------------------------
@app.route('/create/<string:name>/', methods=['GET', 'POST'])
def add_competitor(name):
    '''This method takes in a name and adds it to the list of competitors'''
    global nextId
    nextId += 1
    competitor = {
        'id': nextId,
        'name': name
    }
    competitors.append(competitor)
    return jsonify(competitors), 201

# ------------------------- READ / GET -------------------------
@app.route('/get/<int:id>/')
def get_competitor(id=0):
    '''
    This method takes in an id and reads the name of that competitor.
    If no id was given, a random competitor's name is returned.
    '''
    # Cases where no id is specified, we return a random competitor:
    if id == 0:
        return random.choice(competitors), 200
    # Cases where id is valid, we return the competitor:
    else:
        for competitor in competitors:
            if competitor['id'] == id:
                return jsonify(competitors[id - 1]), 200
    # Cases where id isn't valid, we throw a 404 error:
    return "404 error. The requested id was not found on this server.", 404

# ------------------------- UPDATE / PUT -------------------------
@app.route('/update/<int:id>/<string:name>/', methods=['GET', 'POST'])
def update_competitor(id, name):
    '''This method takes in an id and updates that competitor's name.'''
    for competitor in competitors:
        if competitor['id'] == id:
            updated_competitor = {
                'id': id,
                'name': name
            }
            competitors[id - 1] = updated_competitor
            return jsonify(competitors), 200
    return "404 error. The requested id was not found on this server.", 404

# ------------------------- DELETE -------------------------
@app.route('/delete/<int:id>/', methods=['GET', 'DELETE'])
def delete_competitor(id):
    global nextId
    for competitor in competitors:
        if competitor['id'] == id:
            # Remove the competitor
            competitors.pop(id - 1)

            # Update all of the ids of the remaining competitors
            new_id = 1
            for remaining_competitor in competitors:
                remaining_competitor['id'] = new_id
                new_id += 1
            # Update nextId
            nextId = len(competitors)
            return jsonify(competitors), 200
    return "404 error. The requested id was not found on this server.", 404

# ------------------------- RUN FLASK APP -------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

# ------------------------- URLS -------------------------
# Index URL:            http://localhost:5000/
# Create / Post:        http://localhost:5000/create/<name>
# Read / Get:           http://localhost:5000/get/<id>
# Update / Put:         http://localhost:5000//update/<id>/<name>
# Delete:               http://localhost:5000/delete/<id>