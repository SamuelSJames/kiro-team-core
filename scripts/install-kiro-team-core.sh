#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'

# Kiro Team Core bootstrap installer.
# - clones the canonical GitHub framework to a temporary directory
# - validates the framework before touching ~/.kiro
# - installs agents, steering, skills, templates, tools, and framework docs
# - creates/refreshes the isolated visual-compare environment
# - verifies Graphify
# - validates installed resource/MCP references
# - never leaves ~/.kiro as a Git working tree

REPO_URL="${KIRO_TEAM_CORE_REPO:-https://github.com/SamuelSJames/kiro-team-core.git}"
BRANCH="${KIRO_TEAM_CORE_BRANCH:-main}"
KIRO_HOME="${KIRO_HOME:-$HOME/.kiro}"
LOCAL_BIN="${LOCAL_BIN:-$HOME/.local/bin}"

DRY_RUN=0
SKIP_GRAPHIFY=0
KEEP_BACKUP=1
TRY_KIRO_VALIDATION=1

log()  { printf '[kiro-team-core] %s\n' "$*"; }
warn() { printf '[kiro-team-core] WARNING: %s\n' "$*" >&2; }
die()  { printf '[kiro-team-core] ERROR: %s\n' "$*" >&2; exit 1; }

usage() {
  cat <<'EOF'
Usage: install-kiro-team-core.sh [options]

Options:
  --repo URL              Override source repository.
  --branch NAME           Override Git branch (default: main).
  --kiro-home PATH        Override Kiro home (default: ~/.kiro).
  --skip-graphify         Do not install/verify Graphify.
  --skip-kiro-validate    Skip best-effort Kiro CLI agent validation.
  --no-backup             Delete the successful-install backup after validation.
  --dry-run               Clone and validate source only; do not modify ~/.kiro.
  -h, --help              Show help.

Environment equivalents:
  KIRO_TEAM_CORE_REPO
  KIRO_TEAM_CORE_BRANCH
  KIRO_HOME
  LOCAL_BIN
EOF
}

while (($#)); do
  case "$1" in
    --repo)
      [[ $# -ge 2 ]] || die "--repo requires a value"
      REPO_URL="$2"; shift 2 ;;
    --branch)
      [[ $# -ge 2 ]] || die "--branch requires a value"
      BRANCH="$2"; shift 2 ;;
    --kiro-home)
      [[ $# -ge 2 ]] || die "--kiro-home requires a value"
      KIRO_HOME="$2"; shift 2 ;;
    --skip-graphify)
      SKIP_GRAPHIFY=1; shift ;;
    --skip-kiro-validate)
      TRY_KIRO_VALIDATION=0; shift ;;
    --no-backup)
      KEEP_BACKUP=0; shift ;;
    --dry-run)
      DRY_RUN=1; shift ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      die "Unknown option: $1" ;;
  esac
done

for cmd in git python3; do
  command -v "$cmd" >/dev/null 2>&1 || die "Required command not found: $cmd"
done

if [[ "$DRY_RUN" -eq 0 ]]; then
  for cmd in uv kiro-cli; do
    command -v "$cmd" >/dev/null 2>&1 || die "Required command not found: $cmd"
  done
fi

case "$(uname -s)" in
  Linux) ;;
  *) die "This installer is intended for Linux/WSL." ;;
esac

TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/kiro-team-core.XXXXXX")"
SRC="$TMP_ROOT/src"
STAGE="$TMP_ROOT/stage"
MANIFEST="$KIRO_HOME/.team-core-manifest"
BACKUP_DIR=""
ROLLBACK_ARMED=0
OLD_VISUAL_COMPARE_TYPE=""
OLD_VISUAL_COMPARE_TARGET=""
OLD_VISUAL_COMPARE_COPY=""

cleanup() {
  rm -rf "$TMP_ROOT" 2>/dev/null || true
}

restore_local_bin() {
  local link="$LOCAL_BIN/visual-compare"
  rm -f "$link" 2>/dev/null || true

  case "$OLD_VISUAL_COMPARE_TYPE" in
    symlink)
      ln -s "$OLD_VISUAL_COMPARE_TARGET" "$link"
      ;;
    file)
      [[ -f "$OLD_VISUAL_COMPARE_COPY" ]] && cp -p "$OLD_VISUAL_COMPARE_COPY" "$link"
      ;;
    none|"")
      ;;
  esac
}

rollback() {
  local rc=$?
  trap - ERR INT TERM

  if [[ "$ROLLBACK_ARMED" -eq 1 && -n "$BACKUP_DIR" && -d "$BACKUP_DIR" ]]; then
    warn "Install failed; restoring the previous managed Kiro Team Core files."

    python3 - "$KIRO_HOME" "$BACKUP_DIR" "$MANIFEST" <<'PY'
from pathlib import Path
import shutil
import sys

kiro = Path(sys.argv[1])
backup = Path(sys.argv[2])
manifest = Path(sys.argv[3])

new_manifest = backup / "new-manifest.txt"
if new_manifest.exists():
    for rel in sorted(
        (x.strip() for x in new_manifest.read_text().splitlines() if x.strip()),
        key=lambda x: len(Path(x).parts),
        reverse=True,
    ):
        p = kiro / rel
        if p.is_symlink() or p.is_file():
            p.unlink(missing_ok=True)

restore_root = backup / "files"
if restore_root.exists():
    for src in sorted(restore_root.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(restore_root)
        dst = kiro / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

old_manifest = backup / "old-manifest.txt"
if old_manifest.exists():
    manifest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(old_manifest, manifest)
else:
    manifest.unlink(missing_ok=True)

for p in sorted(kiro.rglob("*"), key=lambda x: len(x.parts), reverse=True):
    if p.is_dir():
        try:
            p.rmdir()
        except OSError:
            pass
PY

    restore_local_bin || true
  fi

  cleanup
  exit "$rc"
}

trap rollback ERR INT TERM
trap cleanup EXIT

log "Cloning canonical framework: $REPO_URL ($BRANCH)"
git clone --quiet --depth 1 --branch "$BRANCH" "$REPO_URL" "$SRC"
[[ -d "$SRC/.git" ]] || die "Clone did not produce a valid Git checkout."

mkdir -p "$STAGE"

for dir in agents steering skills; do
  [[ -d "$SRC/.kiro/$dir" ]] || die "Missing source directory: .kiro/$dir"
  cp -a "$SRC/.kiro/$dir" "$STAGE/$dir"
done

[[ -d "$SRC/templates" ]] || die "Missing source directory: templates"
cp -a "$SRC/templates" "$STAGE/templates"

[[ -d "$SRC/tools" ]] || die "Missing source directory: tools"
cp -a "$SRC/tools" "$STAGE/tools"

GLOBAL_DOCS=(
  AGENT_ROSTER.md
  SCOPE_GOVERNANCE.md
  WORKFLOW.md
  TOOLING.md
  WORKSPACE_HYGIENE.md
  SKILL_REGISTRY.md
  KIRO_CLI_SETUP.md
)

for doc in "${GLOBAL_DOCS[@]}"; do
  [[ -f "$SRC/$doc" ]] || die "Missing required framework document: $doc"
  cp "$SRC/$doc" "$STAGE/$doc"
done

log "Running static framework validation."
python3 - "$STAGE" <<'PY'
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]).resolve()
agents_dir = root / "agents"
steering_dir = root / "steering" / "agents"
skills_dir = root / "skills"

errors = []

agents = sorted(agents_dir.glob("*.md"))
if len(agents) != 30:
    errors.append(f"expected exactly 30 agent files, found {len(agents)}")

expected_nums = [f"{i:02d}" for i in range(1, 31)]
actual_nums = [p.name[:2] for p in agents]
if actual_nums != expected_nums:
    errors.append(f"agent numbering mismatch: {actual_nums}")

for agent in agents:
    text = agent.read_text(encoding="utf-8")

    if not text.startswith("---\n") or "\n---\n" not in text:
        errors.append(f"{agent.name}: invalid/missing frontmatter")
        continue

    fm = text.split("\n---\n", 1)[0][4:]

    for required in ("name", "description", "model"):
        if not re.search(rf"^{required}:\s*.+$", fm, re.M):
            errors.append(f"{agent.name}: missing {required}")

    if not re.search(r"^includeMcpJson:\s*false\s*$", fm, re.M):
        errors.append(f"{agent.name}: includeMcpJson must be false")

    steer = steering_dir / agent.name
    if not steer.is_file():
        errors.append(f"{agent.name}: matching steering file missing")

    for scheme, rel in re.findall(r'"(file|skill)://([^"]+)"', fm):
        if not rel.startswith("../"):
            errors.append(
                f"{agent.name}: resource is not runtime-relative: {scheme}://{rel}"
            )
            continue

        target = (agent.parent / rel).resolve()

        try:
            target.relative_to(root)
        except ValueError:
            errors.append(
                f"{agent.name}: resource escapes installed Kiro home: {scheme}://{rel}"
            )
            continue

        if not target.exists():
            errors.append(
                f"{agent.name}: missing resource: {scheme}://{rel}"
            )

    def list_block(key: str) -> list[str]:
        m = re.search(
            rf"^{re.escape(key)}:\n((?:\s+- .+\n?)*)",
            fm,
            re.M,
        )
        if not m:
            return []

        values = []
        for line in m.group(1).splitlines():
            value = re.sub(r"^\s*-\s*", "", line).strip().strip('"')
            if value:
                values.append(value)
        return values

    tools = set(list_block("tools"))
    allowed = set(list_block("allowedTools"))

    extra = sorted(allowed - tools)
    if extra:
        errors.append(
            f"{agent.name}: allowedTools not present in tools: {extra}"
        )

    selectors = {
        item[1:]
        for item in tools
        if item.startswith("@") and "/" not in item
    }

    mcp_names = set(
        re.findall(
            r"^\s{2}([A-Za-z0-9_-]+):\n\s{4}command:",
            fm,
            re.M,
        )
    )

    missing_servers = sorted(selectors - mcp_names)
    if missing_servers:
        errors.append(
            f"{agent.name}: MCP selectors without mcpServers: {missing_servers}"
        )

    unused_servers = sorted(mcp_names - selectors)
    if unused_servers:
        errors.append(
            f"{agent.name}: mcpServers not exposed in tools: {unused_servers}"
        )

skills = sorted(skills_dir.glob("*/SKILL.md"))
if not skills:
    errors.append("no skills found")

skill_names = set()
for skill in skills:
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text:
        errors.append(f"{skill.relative_to(root)}: invalid frontmatter")
        continue

    fm = text.split("\n---\n", 1)[0][4:]
    name_match = re.search(r"^name:\s*(\S.+)$", fm, re.M)
    desc_match = re.search(r"^description:\s*(\S.+)$", fm, re.M)

    if not name_match:
        errors.append(f"{skill.relative_to(root)}: missing skill name")
    else:
        name = name_match.group(1).strip()
        if name in skill_names:
            errors.append(f"duplicate skill name: {name}")
        skill_names.add(name)

    if not desc_match:
        errors.append(f"{skill.relative_to(root)}: missing skill description")

for rel in (
    "templates/project/PROJECT_STATUS.md",
    "templates/project/ASSIGNMENTS.md",
    "templates/project/DECISIONS.md",
    "templates/project/HANDOFF.md",
):
    if not (root / rel).is_file():
        errors.append(f"missing project-control template: {rel}")

for rel in (
    "tools/visual-compare/visual_compare.py",
    "tools/visual-compare/pyproject.toml",
    "tools/visual-compare/tests/test_visual_compare.py",
):
    if not (root / rel).is_file():
        errors.append(f"missing visual-compare component: {rel}")

if errors:
    print("STATIC VALIDATION FAILED", file=sys.stderr)
    for error in errors:
        print(f"  - {error}", file=sys.stderr)
    sys.exit(1)

print(
    f"Static validation passed: {len(agents)} agents, "
    f"{len(skills)} skills, resources/MCP references valid."
)
PY

python3 -m py_compile "$STAGE/tools/visual-compare/visual_compare.py"

if [[ "$DRY_RUN" -eq 1 ]]; then
  log "Dry run complete. Source cloned and validated; no runtime files changed."
  exit 0
fi

mkdir -p "$KIRO_HOME" "$LOCAL_BIN" "$KIRO_HOME/backups"

TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP_DIR="$KIRO_HOME/backups/team-core-$TIMESTAMP"
mkdir -p "$BACKUP_DIR/files"

NEW_MANIFEST="$TMP_ROOT/new-manifest.txt"
python3 - "$STAGE" > "$NEW_MANIFEST" <<'PY'
from pathlib import Path
import sys

root = Path(sys.argv[1])
for p in sorted(root.rglob("*")):
    if p.is_file():
        print(p.relative_to(root))
PY

cp "$NEW_MANIFEST" "$BACKUP_DIR/new-manifest.txt"

if [[ -f "$MANIFEST" ]]; then
  cp "$MANIFEST" "$BACKUP_DIR/old-manifest.txt"
fi

python3 - "$KIRO_HOME" "$BACKUP_DIR/files" "$MANIFEST" "$NEW_MANIFEST" <<'PY'
from pathlib import Path
import shutil
import sys

kiro = Path(sys.argv[1])
out = Path(sys.argv[2])
old_manifest = Path(sys.argv[3])
new_manifest = Path(sys.argv[4])

rels = set()

for manifest in (old_manifest, new_manifest):
    if manifest.exists():
        rels.update(
            x.strip()
            for x in manifest.read_text().splitlines()
            if x.strip()
        )

for rel in rels:
    src = kiro / rel
    if src.is_file() and not src.is_symlink():
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
PY

VC_LINK="$LOCAL_BIN/visual-compare"
if [[ -L "$VC_LINK" ]]; then
  OLD_VISUAL_COMPARE_TYPE="symlink"
  OLD_VISUAL_COMPARE_TARGET="$(readlink "$VC_LINK")"
elif [[ -f "$VC_LINK" ]]; then
  OLD_VISUAL_COMPARE_TYPE="file"
  OLD_VISUAL_COMPARE_COPY="$BACKUP_DIR/visual-compare.previous"
  cp -p "$VC_LINK" "$OLD_VISUAL_COMPARE_COPY"
else
  OLD_VISUAL_COMPARE_TYPE="none"
fi

ROLLBACK_ARMED=1

if [[ -f "$MANIFEST" ]]; then
  python3 - "$KIRO_HOME" "$MANIFEST" <<'PY'
from pathlib import Path
import sys

root = Path(sys.argv[1])
manifest = Path(sys.argv[2])

rels = [
    x.strip()
    for x in manifest.read_text().splitlines()
    if x.strip()
]

for rel in sorted(rels, key=lambda x: len(Path(x).parts), reverse=True):
    p = root / rel
    if p.is_file() or p.is_symlink():
        p.unlink(missing_ok=True)

for p in sorted(root.rglob("*"), key=lambda x: len(x.parts), reverse=True):
    if p.is_dir():
        try:
            p.rmdir()
        except OSError:
            pass
PY
fi

log "Installing Kiro Team Core into $KIRO_HOME"
cp -a "$STAGE/." "$KIRO_HOME/"
cp "$NEW_MANIFEST" "$MANIFEST"

rm -rf "$KIRO_HOME/.git" "$KIRO_HOME/.github" 2>/dev/null || true

VC_DIR="$KIRO_HOME/tools/visual-compare"

log "Creating isolated visual-compare environment."
rm -rf "$VC_DIR/.venv"
uv venv "$VC_DIR/.venv" >/dev/null
uv pip install   --python "$VC_DIR/.venv/bin/python"   "$VC_DIR[test]" >/dev/null

ln -sfn "$VC_DIR/.venv/bin/visual-compare" "$LOCAL_BIN/visual-compare"

log "Running visual-compare tests."
"$VC_DIR/.venv/bin/python" -m pytest "$VC_DIR/tests" -q
"$LOCAL_BIN/visual-compare" --help >/dev/null

if [[ "$SKIP_GRAPHIFY" -eq 0 ]]; then
  if ! command -v graphify >/dev/null 2>&1; then
    [[ -f "$SRC/scripts/install-graphify.sh" ]]       || die "Graphify is missing and scripts/install-graphify.sh was not found."
    log "Graphify is missing; installing official graphifyy tool."
    bash "$SRC/scripts/install-graphify.sh"
    hash -r
  fi

  command -v graphify >/dev/null 2>&1     || die "Graphify installation completed but the command is unavailable."

  graphify --help >/dev/null
  log "Graphify verified: $(graphify --version 2>&1 | head -n 1)"
fi

log "Validating installed runtime."
python3 - "$KIRO_HOME" <<'PY'
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]).resolve()
agents = sorted((root / "agents").glob("*.md"))
errors = []

if len(agents) != 30:
    errors.append(f"expected 30 installed agents, found {len(agents)}")

for agent in agents:
    text = agent.read_text(encoding="utf-8")
    if "\n---\n" not in text:
        errors.append(f"{agent.name}: invalid frontmatter")
        continue

    fm = text.split("\n---\n", 1)[0][4:]

    for scheme, rel in re.findall(r'"(file|skill)://([^"]+)"', fm):
        target = (agent.parent / rel).resolve()
        if not target.exists():
            errors.append(
                f"{agent.name}: unresolved {scheme}://{rel}"
            )

    tools_match = re.search(
        r"^tools:\n((?:\s+- .+\n?)*)",
        fm,
        re.M,
    )
    tools = set()
    if tools_match:
        for line in tools_match.group(1).splitlines():
            value = re.sub(r"^\s*-\s*", "", line).strip().strip('"')
            if value:
                tools.add(value)

    selectors = {
        item[1:]
        for item in tools
        if item.startswith("@") and "/" not in item
    }
    mcp_names = set(
        re.findall(
            r"^\s{2}([A-Za-z0-9_-]+):\n\s{4}command:",
            fm,
            re.M,
        )
    )

    missing = selectors - mcp_names
    if missing:
        errors.append(
            f"{agent.name}: missing MCP definitions for {sorted(missing)}"
        )

if errors:
    print("INSTALLED RUNTIME VALIDATION FAILED", file=sys.stderr)
    for error in errors:
        print(f"  - {error}", file=sys.stderr)
    sys.exit(1)

print(
    f"Installed runtime validation passed: {len(agents)} agents; "
    "all declared resources and MCP selectors resolve."
)
PY

log "Kiro CLI detected: $(kiro-cli --version 2>&1 | head -n 1)"

# Kiro Team Core intentionally uses the V3/unified agent harness because the
# framework depends on Markdown agent configs, skill:// resources, inline MCP
# servers, capability tags, and permissions blocks. CLI 2.x legacy validation
# parses agent files as JSON and is not valid for this framework.
if [[ "$TRY_KIRO_VALIDATION" -eq 1 ]]; then
  if kiro-cli --v3 agent list >/dev/null 2>&1; then
    log "Kiro V3 harness detected; validating that all 30 global agents are discoverable."
    AGENT_LIST_OUTPUT="$(kiro-cli --v3 agent list 2>&1)" || die "Kiro V3 agent discovery failed."

    missing_agents=0
    for agent_file in "$KIRO_HOME"/agents/*.md; do
      agent_name="$(basename "$agent_file" .md)"
      if ! grep -Fq "$agent_name" <<<"$AGENT_LIST_OUTPUT"; then
        warn "Kiro V3 agent list did not show: $agent_name"
        missing_agents=$((missing_agents + 1))
      fi
    done

    if [[ "$missing_agents" -ne 0 ]]; then
      die "Kiro V3 discovery is missing $missing_agents installed agent(s)."
    fi

    log "Kiro V3 discovery passed: all 30 installed agents are visible."
  else
    die "Kiro Team Core requires the V3 agent harness. 'kiro-cli --v3 agent list' failed."
  fi
fi

ROLLBACK_ARMED=0

if [[ "$KEEP_BACKUP" -eq 0 ]]; then
  rm -rf "$BACKUP_DIR"
  log "Successful-install backup removed (--no-backup)."
else
  log "Backup retained: $BACKUP_DIR"
fi

log "Installation complete."
log "Kiro runtime: $KIRO_HOME"
log "Installed agents: 30"
log "visual-compare: $LOCAL_BIN/visual-compare"

printf '\nFinal live Kiro smoke test:\n'
printf '  kiro-cli\n'
printf '  /agent list\n'
printf '  /agent swap 01-orchestrator\n'
