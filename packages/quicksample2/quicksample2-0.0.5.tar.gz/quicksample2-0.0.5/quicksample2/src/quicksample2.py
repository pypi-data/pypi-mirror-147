import requests
import json

url = "https://api.socialkarma.xyz/api/v1/report"

class Client:
  def __init__(self, api_key):
    self.api_key = api_key

  def submit_report(self, reported_user_id, reporting_user_id, title, description):
    url = "https://api.socialkarma.xyz/api/v1/report"

    payload = json.dumps({
      "ReportedUserId": reported_user_id,
      "ReportingUserId": reporting_user_id,
      "Title": title,
      "Description": description
    })
    headers = {
      'Auth': self.api_key,
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
