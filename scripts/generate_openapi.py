from pathlib import Path
import json
import yaml

from main import app

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "docs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

schema = app.openapi()

json_path = OUTPUT_DIR / "openapi.json"
yaml_path = OUTPUT_DIR / "openapi.yaml"

json_path.write_text(json.dumps(schema, indent=2, ensure_ascii=False), encoding="utf-8")
yaml_path.write_text(yaml.safe_dump(schema, sort_keys=False, allow_unicode=True), encoding="utf-8")

print(f"OpenAPI JSON generated: {json_path}")
print(f"OpenAPI YAML generated: {yaml_path}")
