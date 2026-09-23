import json
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

SOURCES = [
    "https://www.mehrnews.com/rss"
]

KEYWORDS = [
    "کنسرت",
    "تئاتر",
    "نمایشگاه",
    "جشنواره",
    "موسیقی",
    "فیلم",
    "سینما",
    "گردشگری",
    "طبیعت",
    "تور",
    "رویداد"
]

events = {}

for url in SOURCES:
    try:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})

        with urlopen(request, timeout=30) as response:
            content = response.read()

        root = ET.fromstring(content)

        for item in root.findall(".//item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            date = (item.findtext("pubDate") or "").strip()

            if any(keyword in title for keyword in KEYWORDS):
                events[title] = {
                    "title": title,
                    "link": link,
                    "date": date
                }

        print("Relevant events found:", len(events))

    except Exception as error:
        print("Source failed:", error)

output = {
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "events": events
}

Path("data/events.json").write_text(
    json.dumps(output, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("events.json updated")
