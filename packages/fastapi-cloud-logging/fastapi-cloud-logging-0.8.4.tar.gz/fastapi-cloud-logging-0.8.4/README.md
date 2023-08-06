# fastapi-cloud-logging

## Installation

```sh
pip install fastapi-cloud-logging
```

## Usage

Add middleware and handler to send a request info to cloud logging.

```python
from fastapi import FastAPI
from google.cloud.logging import Client
from google.cloud.logging_v2.handlers import setup_logging

from fastapi_cloud_logging import FastAPILoggingHandler, RequestLoggingMiddleware

app = FastAPI()

# Add middleware
app.add_middleware(RequestLoggingMiddleware)

# Use manual handler
handler = FastAPILoggingHandler(Client())
setup_logging(handler)
```
