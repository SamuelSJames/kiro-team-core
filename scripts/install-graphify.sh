#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'

# install-graphify.sh
# Installs the official Graphify CLI package (graphifyy) as a user-scoped uv tool.
# Intentionally DOES NOT run `graphify install`, because Kiro Team Core manages
# its own Graphify skill and steering files.

readonly PACKAGE="graphifyy"
readonly COMMAND="graphify"

log()  { printf '[graphify-install] %s\n' "$*"; }
warn() { printf '[graphify-install] WARNING: %s\n' "$*" >&2; }
die()  { printf '[graphify-install] ERROR: %s\n' "$*" >&2; exit 1; }

on_error() {
    local exit_code=$?
    local line_no=${1:-unknown}
    printf '[graphify-install] ERROR: installation failed at line %s (exit %s)\n' \
        "$line_no" "$exit_code" >&2
    exit "$exit_code"
}
trap 'on_error "$LINENO"' ERR

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

version_ge() {
    python3 - "$1" "$2" <<'PY'
import sys
def parse(v):
    parts = []
    for p in v.split("."):
        n = "".join(ch for ch in p if ch.isdigit())
        if n == "":
            break
        parts.append(int(n))
    return tuple(parts)
sys.exit(0 if parse(sys.argv[1]) >= parse(sys.argv[2]) else 1)
PY
}

log "Starting Graphify installation."

case "$(uname -s)" in
    Linux) ;;
    *) die "This installer is intended for the Linux/WSL Kiro environment." ;;
esac

if grep -qi microsoft /proc/version 2>/dev/null; then
    log "WSL environment detected."
else
    warn "WSL was not detected; continuing because this is still Linux."
fi

command_exists python3 || die "python3 is required but was not found."
command_exists uv || die "uv is required but was not found. Install uv first, then rerun this script."

PY_VERSION="$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')"
if ! version_ge "$PY_VERSION" "3.10"; then
    die "Python >= 3.10 is required; found Python ${PY_VERSION}."
fi
log "Python ${PY_VERSION} OK."

UV_VERSION="$(uv --version 2>/dev/null || true)"
[[ -n "$UV_VERSION" ]] || die "uv is installed but did not return a version."
log "${UV_VERSION}."

UV_BIN_DIR="$(uv tool dir --bin 2>/dev/null || true)"
[[ -n "$UV_BIN_DIR" ]] || die "Could not determine the uv tool binary directory."
mkdir -p "$UV_BIN_DIR"

case ":${PATH}:" in
    *":${UV_BIN_DIR}:"*) ;;
    *) export PATH="${UV_BIN_DIR}:${PATH}" ;;
esac

if uv tool list 2>/dev/null | grep -Eq '^graphifyy([[:space:]]|$)'; then
    log "Graphify is already installed; upgrading ${PACKAGE}."
    uv tool install --upgrade "$PACKAGE"
else
    log "Installing official package ${PACKAGE}."
    uv tool install "$PACKAGE"
fi

GRAPHIFY_BIN="${UV_BIN_DIR}/${COMMAND}"
[[ -x "$GRAPHIFY_BIN" ]] || die "Install completed, but ${GRAPHIFY_BIN} is missing or not executable."

if ! command_exists "$COMMAND"; then
    warn "${COMMAND} is not yet visible through the shell PATH."
    log "Updating the shell PATH using uv."
    uv tool update-shell
    export PATH="${UV_BIN_DIR}:${PATH}"
fi

VERSION_OUTPUT="$("$GRAPHIFY_BIN" --version 2>&1)" || die "Graphify installed but '${COMMAND} --version' failed."
[[ -n "$VERSION_OUTPUT" ]] || die "Graphify returned an empty version string."

HELP_OUTPUT="$("$GRAPHIFY_BIN" --help 2>&1)" || die "Graphify installed but '${COMMAND} --help' failed."
grep -qi 'graphify' <<<"$HELP_OUTPUT" || die "Graphify help output did not look valid."

uv tool list | grep -Eq '^graphifyy([[:space:]]|$)' \
    || die "uv tool registry does not show ${PACKAGE} after installation."

log "Graphify CLI installed and verified."
log "Version: ${VERSION_OUTPUT}"
log "Binary: ${GRAPHIFY_BIN}"
log "Kiro integration was NOT installed by Graphify."
log "Kiro Team Core will provide the managed Graphify skill/steering integration."

printf '\nNext verification command:\n  graphify --version\n'
