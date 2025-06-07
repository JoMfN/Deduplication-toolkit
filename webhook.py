import requests

def notify_hook(event, payload, url):
    try:
        r = requests.post(url, json={"event": event, "data": payload})
        return r.status_code, r.text
    except Exception as e:
        return None, str(e)

# Example use
if __name__ == "__main__":
    event = "duplicates_filtered"
    payload = {"report": "filtered_duplicates_report.txt"}
    status, response = notify_hook(event, payload, "https://your-museum-api.org/hook")
    print(f"Status: {status}, Response: {response}")
