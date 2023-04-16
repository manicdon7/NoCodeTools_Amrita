import requests

url = "https://api.verbwire.com/v1/nft/store/file"

files = {"filePath": ("C:/Users/nagip/Desktop/Group_of_projects/NoCodeTools_Amrita/requirements.txt", open(
    "C:/Users/nagip/Desktop/Group_of_projects/NoCodeTools_Amrita/requirements.txt", "rb"), "text/html")}
headers = {
    "accept": "application/json",
    "X-API-Key": "sk_live_fdd243a1-07c3-4c90-a976-c133c47f1b3a"
}

response = requests.post(url, files=files, headers=headers)

print(response.text)
