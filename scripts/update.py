import json
from pathlib import Path
from datetime import datetime, timezone

output = {
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "events": {}
}

Path("data/events.json").write_text(
    json.dumps(output, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("events.json updated")
