import json
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen

SOURCES = [
    "https://www.tehrantimes.com/rss"
]

events = {}

for url in SOURCES:
    try:
        request = Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urlopen(request, timeout=20) as response:
            content = response.read().decode("utf-8", errors="ignore")

        print(f"Source checked: {url}")
        print(f"Received {len(content)} bytes")

    except Exception as error:
        print(f"Source failed: {url} - {error}")

output = {
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "events": events
}

Path("data/events.json").write_text(
    json.dumps(output, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("events.json updated")
