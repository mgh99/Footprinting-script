import requests

def fecth():
  urls = open("recon.txt", "r")
  for url in urls:
    url = url.strip()
    print("Footprint report for " + url + " Web server: ")
    req = requests.get(url)
    result = dict(req.headers)
    for item, value in result.items():
      print(item + " : " + value + "\n")

fecth()
