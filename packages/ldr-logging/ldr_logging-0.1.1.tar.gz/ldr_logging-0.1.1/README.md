# Louder Logging

A Google Cloud Logging compliant structured logging library.


## Setup

The following environment variables must be set for logging to function.

```sh
# The name of the actual application running, e.g cloud run service / job name
export LDR_APPLICATION_NAME=application-name
# The version of the application, example here for poetry environments
export LDR_APPLICATION_VERSION=$(poetry version -s)
# The name of the service, can be the same as application name if the service is only
# one component, but in larger projects will be the name of the service offering rather
# than just the application name.
export LDR_APPLICATION_SERVICE_NAME=application-service-name
# The commit hash that this version of the code was committed with.
export LDR_APPLICATION_COMMIT_HASH=$(git rev-parse HEAD)
```

## Examples

```python
import ldr.logging
import logging

ldr.logging.setup(logging.DEBUG)

logging.info("Hello, world!")

entry = ldr.logging.Entry()
logging.warning()
```

Will write the following to stderr

```ndjson
{"logging.googleapis.com/diagnostic": {"instrumentation_source": [{"name": "python", "version": "3.11.3"}]},"severity": "INFO", "logging.googleapis.com/labels": {"python_logger": "google.cloud.logging_v2.handlers.structured_log"}, "logging.googleapis.com/trace": "", "logging.googleapis.com/spanId": "", "logging.googleapis.com/trace_sampled": false, "logging.googleapis.com/sourceLocation": {"line": 149, "file": "/Users/you/Library/Caches/pypoetry/virtualenvs/my-application-N_XRT3hE-py3.11/lib/python3.11/site-packages/google/cloud/logging_v2/handlers/structured_log.py", "function": "emit_instrumentation_info"}, "httpRequest": {} }
{"message": "Hello, world!","severity": "INFO", "logging.googleapis.com/labels": {"python_logger": "root"}, "logging.googleapis.com/trace": "", "logging.googleapis.com/spanId": "", "logging.googleapis.com/trace_sampled": false, "logging.googleapis.com/sourceLocation": {"line": 6, "file": "/Users/you/project/src/main.py", "function": "<module>"}, "httpRequest": {} }
{"client": "LOUD", "message": "Something weird happened but we've handled it", "app": {"name": "application-name", "version": "0.1.0", "service_name": "application-service-name", "commit_hash": "ea09ae9cc6768c50fcee903ed054556e5bfc8347"}, "extra": {"foo": "bar"},"severity": "WARNING", "logging.googleapis.com/labels": {"python_logger": "root"}, "logging.googleapis.com/trace": "", "logging.googleapis.com/spanId": "", "logging.googleapis.com/trace_sampled": false, "logging.googleapis.com/sourceLocation": {"line": 13, "file": "/Users/you/project/src/main.py", "function": "<module>"}, "httpRequest": {} }
```

## Copyright

This project is licensed under the [MIT license](https://opensource.org/license/mit).
