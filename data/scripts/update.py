import json
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

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
            content = response.read()

        root = ET.fromstring(content)

        for item in root.findall(".//item"):
            title = item.findtext("title")
            link = item.findtext("link")
            date = item.findtext("pubDate")

            if title:
                events[title] = {
                    "title": title,
                    "link": link or "",
                    "date": date or ""
                }

        print(f"Source checked: {url}")
        print(f"Events found: {len(events)}")

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
