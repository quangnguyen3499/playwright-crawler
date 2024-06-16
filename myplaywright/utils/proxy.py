from dotenv import load_dotenv
import urllib.parse
import os

load_dotenv()
API_KEY = os.getenv("PROXY_API_KEY")

# Proxy
def get_proxy_url(url):
    payload = {"api_key": API_KEY, "url": url}
    query_string = urllib.parse.urlencode(payload)
    proxy_url = f"https://proxy.scrapeops.io/v1/?{query_string}"
    return proxy_url
