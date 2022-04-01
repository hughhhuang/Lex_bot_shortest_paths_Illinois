import requests
import json
import uuid

url = "https://seorwrpmwh.execute-api.us-east-1.amazonaws.com/prod/mp3-autograder-2022-spring"

payload = {
	"graphApi": "https://x6gmjxmgt3.execute-api.us-east-1.amazonaws.com/tst",
	"botName": "CcaCityPathBot",
	"botAlias": "CcaCityPathBot",
	"identityPoolId": "us-east-1:3fabf8f5-eb87-4b65-9478-e6725a7a710c",
	"accountId": "917722021757",
	"submitterEmail": "hughh3@illinois.edu",
	"secret": "3W9zYfQqqzRTdmjW",
	"region": "us-east-1"
    }

r = requests.post(url, data=json.dumps(payload))

print(r.status_code, r.reason)
print(r.text)