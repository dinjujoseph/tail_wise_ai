import requests

url = "https://api.thedogapi.com/v1/images/upload"

payload = {'sub_id': '123'}
files=[
  ('file',('file',open('/home/dinju/Downloads/French-bulldog.jpg','rb')))
]
headers = {
  'Content-Type': 'multipart/form-data',
  'x-api-key': 'live_X5qa9dWCHV7V4gk9O3PamI5XYy1owMUzhY69lddFscpQ8zNQnWEuLMlyTb6CQ6ae'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)