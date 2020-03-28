import requests
import json

def wawa_get_emergency():
    with open("countries.txt") as json_file:
      data = json.load(json_file)
    return data["Afghanistan"]["ambulance"]

if __name__ == "__main__":
    print(tell_joke())
