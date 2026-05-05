#!/usr/bin/env bash
# Generate Pydantic v2 models from the platform's OpenAPI spec.
# Run before each release; commit the result.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Try the in-tree Platform docs first (fast, deterministic), fall back to the
# remote staging spec.
LOCAL_SPEC="$REPO_ROOT/../Platform/docs/apis/openapi.json"
REMOTE_SPEC="https://staging-api.neuratel.ai/openapi.json"

if [[ -f "$LOCAL_SPEC" ]]; then
  INPUT="$LOCAL_SPEC"
  echo "📥 Using local Platform spec: $INPUT"
else
  INPUT="$REMOTE_SPEC"
  echo "📥 Using remote staging spec: $INPUT"
fi

OUTPUT="$REPO_ROOT/src/neuratelai/types/_generated.py"

uv run datamodel-codegen \
  --input "$INPUT" \
  --input-file-type openapi \
  --output "$OUTPUT" \
  --output-model-type pydantic_v2.BaseModel \
  --use-schema-description \
  --field-constraints \
  --use-double-quotes \
  --use-standard-collections \
  --use-union-operator \
  --target-python-version 3.10 \
  --collapse-root-models \
  --use-default-kwarg \
  --disable-timestamp \
  --custom-file-header "# Auto-generated from openapi.json by scripts/generate_types.sh. DO NOT EDIT."

echo "✅ Generated $OUTPUT"
echo "   $(wc -l < "$OUTPUT" | tr -d ' ') lines"
