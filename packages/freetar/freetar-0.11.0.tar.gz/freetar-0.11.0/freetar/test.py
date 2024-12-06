import requests
from requests_ip_rotator import ApiGateway
import time

BASE_URL = "https://httpbin.org"

print("Initiating ApiGateway")
gateway = ApiGateway(BASE_URL, verbose=True, regions=["eu-west-1"])
gateway.start()

# Assign gateway to session
session = requests.Session()
print("Mounting")
session.mount(BASE_URL, gateway)


def send_request(path: str):
    print("Sending request")
    resp = session.get(BASE_URL + path)
    #resp.raise_for_status()
    print(resp.text)


send_request("/ip")
send_request("/ip")
send_request("/ip")


print("Shutting down")
gateway.shutdown()
