# Network Optimization Module
For Desire6G

## Description
tbd

## Installation
tbd

## Use
tbd

## Demo Instructions
Don't forget to activate `.venv`!

1. Generate a random service request:  
`Python3 servicegen.py`

2. Start the NOE Module  
`Python3 app.py`

3. In a new terminal window, send the service request to NOE:  
`cd inbox`  
`curl -X POST -F "request=@sid85034.json" http://127.0.0.1:5863/service_request`

## Todo
- [x] Phase out management.py and replace it with UI
- [x] Demo partition (fix from Cyril)
- [x] Return the partitioned requests back to the curler
- [x] Updated translation.py file with YAML or JSON 
- [x] servicegen2.py that generates random graph services
- [ ] Basic UI functionality
- [x] Re-structure pre-defined protocol
- [x] Clear old rdf parts

## Troubleshooting
tbd