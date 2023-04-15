import requests

url = "https://api.verbwire.com/v1/nft/userOps/ipfsUploads"

headers = {
    "accept": "application/json",
    "X-API-Key": "sk_live_fdd243a1-07c3-4c90-a976-c133c47f1b3a"
}

response = requests.get(url, headers=headers)

print(response.text)
