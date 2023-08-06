import requests

url = "https://api.socialkarma.xyz/api/v1/report"

class Client:
  def __init__(self, api_key):
    self.api_key = api_key

  def submit_report(self, reported_user_id, reporting_user_id, title, description):
    headers = {
      'Auth': self.api_key,
      'Content-Type': 'application/json'
    }

    payload = {
      "ReportedUserId" : reported_user_id,
      "ReportingUserId" : reporting_user_id, 
      "Title": title, 
      "Description": description 
    }

    return requests.request("POST", url, headers=headers, data=payload)
