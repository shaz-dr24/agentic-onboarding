import requests

def call_n8n(url, data):
    try:
        print(f"📡 Calling n8n webhook: {url}")
        print(f"📦 Payload: {data}")

        response = requests.post(url, json=data, timeout=5)

        # Check response status
        if response.status_code == 200:
            print("✅ n8n workflow triggered successfully")
        else:
            print(f"⚠️ n8n returned status: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to n8n. Is it running on port 5678?")
    
    except requests.exceptions.Timeout:
        print("⏳ Request to n8n timed out")

    except Exception as e:
        print(f"🔥 Unexpected error: {str(e)}")