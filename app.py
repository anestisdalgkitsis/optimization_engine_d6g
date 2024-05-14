from flask import Flask, request, jsonify
from rdflib import Graph

app = Flask(__name__)

# Management API

@app.route('/management', methods=['POST'])
def management():
    print("ok")
    return jsonify("ok")

# IBN (RDF) Endpoint

@app.route('/service_request', methods=['POST'])
def process_rdf():
    if 'request' not in request.files:
        return jsonify({'error': 'No RDF service request provided'})

    file = request.files['request']

    # Parse RDF file
    g = Graph()
    g.parse(file, format='xml')

    # Perform processing (e.g., calculate total weight)
    total_weight = 0
    for s, p, o in g:
        if str(p) == 'http://example.org/weight':
            total_weight += float(o)

    # Generate results
    results = {'total_weight': total_weight}

    return jsonify(results)

# SO Endpoint
# << TBD >>

# Monitoring Endpoint
# << TBD >>

# MAIN
if __name__ == '__main__':
    app.run(debug=True)