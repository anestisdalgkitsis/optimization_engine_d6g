# Network Optimization Module
For Desire6G

## Description
tbd

## Installation
tbd

## Use
tbd

## Demo Instructions
Generate a random service request:
Python3 servicegen.py

Start the NOE Module
Python3 app.py

Send the services request to NOE:
curl -X POST -F "request=@sid85034.json" http://127.0.0.1:5863/service_request

## Plan
- [ ] Phase out management.py and replace it with UI
- [ ] Return the partitioned requests to the curl-er
- [x] Updated translation.py file with YAML or JSON 
- [x] servicegen2.py that generates random digraph services
- [ ] Basic UI functionality (Optional)
- [x] Clear old rdf parts

## Troubleshooting
tbd