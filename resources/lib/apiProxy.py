from __future__ import absolute_import, division, unicode_literals
from config import HEADERS
import requests

def apiRequest(
    uri,
    method,
    data = None,
):
    print(f"<plugin.video.anixart> API Request:\n {uri}\n headers: {HEADERS}\n method: {method}\n data: {data}")
    if not method:
        return {"error": "No method specified"}

    if method == "POST":
        r = requests.post(
            uri,
            data,
            headers=HEADERS,
        )
    if method == "GET":
        r = requests.get(uri, headers=HEADERS)

    print(f"<plugin.video.anixart> API Response:\n {r.text}")
    if r.status_code != 200:
        return {"error": r.text}
    return r.json()
