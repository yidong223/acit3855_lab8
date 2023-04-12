import connexion
import json
import logging
import logging.config
import requests
import yaml

statuses = {
    "receiver": "",
    "storage": "",
    "processing": ""
}

def check():
    # TODO - use try except block(s) to send a GET request to each of your services /health endpoints (receiver, storage, and processing)
    
    
    services = {
        "receiver": "172.18.0.7",
        "processing": "172.18.0.6",
        "storage": "172.18.0.5"
    }

    for name in services.keys():
        try:
            status_code = requests.get(services[name]).status_code
            # For each service, check if the response has status code 200, e.g. res.status_code == 200
            # If the status code for a given service is 200, index into the statuses dict and assign the string "Up" to the correct service key
            if status_code == 200:
                statuses[name] = "Up"
            else:
                statuses[name] = "Down"
        except:
            statuses[name] = "Down"

    # If the status is not 200, or an exception is thrown because the request cannot be completed, index into the statuses dict and assign the string "Down" to the correct key

    return statuses # ignore the instructions to convert this to JSON and leave as-is

app = connexion.FlaskApp(__name__, specification_dir='')

# if you are deploying this to your VM, make sure to add base_path="/health" to the add_api method (and update your NGINX config to proxy requests to the health service)
app.add_api("openapi.yml",base_path="/health", strict_validation=True, validate_responses=True)

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basic')

if __name__ == "__main__":
    app.run(port=8110)