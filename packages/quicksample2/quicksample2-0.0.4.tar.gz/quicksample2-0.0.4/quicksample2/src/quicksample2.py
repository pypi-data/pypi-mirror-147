import requests
import json

url = "https://api.socialkarma.xyz/api/v1/report"

class Client:
  def __init__(self, api_key):
    self.api_key = api_key

  def submit_report(self, reported_user_id, reporting_user_id, title, description):
    url = "https://api.socialkarma.xyz/api/v1/report"

    payload = json.dumps({
      "ReportedUserId": "127",
      "ReportingUserId": "20",
      "Title": "Test",
      "Description": "our moderation team caught chris performing an imposter scam through X means with Y victim"
    })
    headers = {
      'Auth': '22f30b08-b169-11ec-b909-0242ac120002',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
