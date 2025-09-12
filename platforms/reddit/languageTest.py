

import requests


data = requests.post("http://10.226.53.238:6000/langDetect", json={"content":"mera naam azad hai"})
print(data)