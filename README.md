# Network Optimization Engine Module
For Desire6G WP3 | Dr. Anestis Dalgkitsis, Cyril Hsu

## Description
Network Optimization Engine module 3-domain partition demonstration. 

## Installation
Just `git clone` this repository.

## Demo Instructions
Don't forget to activate `.venv`!

1. Generate a random service request:  
`Python3 servicegen.py`

2. Start the NOE Module  
`Python3 app.py`

3. In a new terminal window, send the service request to NOE:  
`cd inbox`  
`curl -X POST -F "request=@sid85034.json" http://127.0.0.1:5863/service_request`

## Deploy Container
Simply run the following commands on root.

`docker build -t oe_d6g_dalgkitsis .`
`docker run --name Optimization_Engine_Dalgkitsis -d -p 5863:5863 oe_d6g_dalgkitsis`

## Todo
- [ ] UI functionality
    - [ ] Realtime UI updates
    - [x] Basic functionality (manual refresh)
- [x] 2 more mock partitioning algorithms
- [ ] mock algorithm auto-selector
- [ ] calculate QoS service info
- [ ] Easy deployment with Docker
    - [x] dockerfile
- [ ] Store service request log
- [ ] Config file loading during startup
- [ ] Create common model interfaces (for autoselection)
- [x] Pass-through service graph info
- [x] Phase out management.py and replace it with UI
- [x] Demo partition (fix from Cyril)
- [x] Return the partitioned requests back to the curler
- [x] Updated translation.py file with YAML or JSON 
- [x] servicegen2.py that generates random graph services
- [x] Re-structure pre-defined protocol
- [x] Clear old rdf parts

## Known Errors
- Limited to 3 domains only.