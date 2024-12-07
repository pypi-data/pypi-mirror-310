# SIRI Profile France Parser 

A Python library for parsing  SIRI (Service Interface for Real-time Information) messages according to the French national profile specification (SIRI Profile France).

## Overview
This library implements the French national adaptation of the SIRI standard, which is used for real-time public transport information exchange in France. It provides tools for parsing and working with SIRI messages that conform to the French profile specifications.


## Key Features

Full support for SIRI Profile France v2.0
XML parsing
Type-safe data structures
Support for all SIRI France service types:

- Stop Monitoring
- Estimated Timetable
- General Message
- Situation Exchange
- Production Timetable
- Facility Monitoring
- Connection Monitoring
- Vehicle Monitoring

## Siri interpretation notice et folders structures.
SIRI (Service Interface for Real-time Information) defines 
- Services (services available)
- Structures (data class/ structures for every object found in the specficication)
- Enums 


Sometimes you will find ``:::`` in the specification, ex: 

| LEADER | :::    | 1:1     | xxx-Delivery     | voir xxxDelivery  |
|--------|--------|---------|------------------|-------------------|
|        |        |         |                  |                   |


For us, it means  single or multiples members of xxx-Delivery/LEADER can be found flattened into the structures where xxx-Delivery/LEADER is implemented.

We have therefore decide to flatten XxxDelivery rust struct each time we found ``:::`` or ``LEADER`` defined into a response data structure and we build a custom deserializer for it.
We have done so everytime we found that a data structure needed to be flattened



## Installation

The parser can be installed using pypi, it requires python to be at version >=3.7

```
pip install siri-parser
```


an then it can be used like this:

```python

import siri_parser as siri

siri_parser = siri.SIRI()


data = """SIRI XML"""

parsed_data = siri_parser.parse(data)
print(str(parsed_data))

if parsed_data.body().notify_production_timetable():
    print("production_timetable")
elif parsed_data.body().notify_estimated_timetable():
    print("estimated_timetable")
else:
    print("other services")
```



## License
MIT license