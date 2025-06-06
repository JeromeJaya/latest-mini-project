import requests
r = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': 'YOUR_TEXT_URL',
    },
    headers={'api-key': '4ae5aadc-f887-4334-8dd8-91f19bd56080'}
)
print(r.json())


# Example posting a local text file:

import requests
r = requests.post(
    "https://api.deepai.org/api/text2img",
    files={
        'text': open('file.txt', 'rb'),
    },
    headers={'api-key': '4ae5aadc-f887-4334-8dd8-91f19bd56080'}
)
print(r.json())


# Example directly sending a text string:

import requests
r = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': 'YOUR_TEXT_HERE',
    },
    headers={'api-key': '4ae5aadc-f887-4334-8dd8-91f19bd56080'}
)
print(r.json())