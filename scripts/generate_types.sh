#!/usr/bin/env bash
# Generate Pydantic v2 models from the platform's OpenAPI spec.
# Run before each release; commit the result.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# The live API is the source of truth (FastAPI auto-generates /openapi.json).
# Fall back to the local copy only when offline or CI needs determinism.
REMOTE_SPEC="https://api.neuratel.ai/openapi.json"
LOCAL_SPEC="$REPO_ROOT/../platform/backend/openapi.json"

if [[ "${FORCE_LOCAL:-0}" == "1" ]]; then
  INPUT="$LOCAL_SPEC"
  echo "⚠️  FORCE_LOCAL=1, using local copy: $INPUT"
elif curl -sf --max-time 10 "$REMOTE_SPEC" -o /tmp/_neuratel_spec.json 2>/dev/null; then
  INPUT="/tmp/_neuratel_spec.json"
  echo "📥 Using live spec from $REMOTE_SPEC"
else
  if [[ -f "$LOCAL_SPEC" ]]; then
    INPUT="$LOCAL_SPEC"
    echo "⚠️  Remote spec unavailable, using local copy: $INPUT"
  else
    echo "❌ No spec available (remote unreachable, local copy missing)" >&2
    exit 1
  fi
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
