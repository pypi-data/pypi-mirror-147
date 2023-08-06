# Status code handler

Library for handler GET requests 
comparing their status code.

## Installation

``` bash
$ pip3 install request_handler
```

## Get started

How to compare the status code to know 
if continue or stop.

``` python3
from request_handler import RequestHandler

if __name__ == '__main__':
    handler = RequestHandler('https://catfact.ninja/fact')
    handler_jsoned = handler.check_json_response()
    if handler_jsoned:
        print(handler_jsoned)
    else:
        print("[-] Exiting...")
        exit(1)
 
```
