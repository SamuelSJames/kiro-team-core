#!/usr/bin/env python3
"""OpenRouter image-generation MCP server (stdio).

Narrow, dedicated server for the Kiro agent team. Four tools:
  - list_image_models
  - generate_image
  - edit_image
  - get_image_model_capabilities

Secret handling: the OpenRouter API key is fetched at runtime from Infisical via
universal-auth (machine identity) and held only in memory. It is never written to
disk, logged, or returned. Authorization headers are never logged.
"""
from __future__ import annotations

import base64
import binascii
import datetime as _dt
import json
import logging
import os
import re
import sys
import uuid
from pathlib import Path
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

LOG = logging.getLogger("openrouter-image")
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,  # stdout is the MCP transport; logs go to stderr only
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

OPENROUTER_BASE = "https://openrouter.ai/api/v1"
OUTPUT_DIR = Path(os.environ.get("ORIMG_OUTPUT_DIR", "/data")).resolve()
HTTP_TIMEOUT = float(os.environ.get("ORIMG_HTTP_TIMEOUT", "180"))
# OpenRouter attribution headers (optional, non-secret)
REFERER = os.environ.get("ORIMG_HTTP_REFERER", "https://snsnetlabs.com/kiro-agents")
TITLE = os.environ.get("ORIMG_APP_TITLE", "Kiro Agent Image MCP")

_EXT_BY_MEDIA = {
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/webp": "webp",
    "image/svg+xml": "svg",
}


class ConfigError(RuntimeError):
    pass


# --------------------------------------------------------------------------- #
# Secret retrieval — Infisical universal-auth, in-memory only                  #
# --------------------------------------------------------------------------- #
def _resolve_openrouter_key() -> str:
    """Resolve the OpenRouter key.

    Priority:
      1. OPENROUTER_API_KEY already in env (e.g. injected by a trusted caller).
      2. Infisical universal-auth using INFISICAL_* env vars.
    The resolved key is returned to the caller to keep in memory; never persisted.
    """
    direct = os.environ.get("OPENROUTER_API_KEY")
    if direct:
        LOG.info("OpenRouter key sourced from OPENROUTER_API_KEY env")
        return direct

    api = os.environ.get("INFISICAL_API_URL")
    cid = os.environ.get("INFISICAL_CLIENT_ID")
    csec = os.environ.get("INFISICAL_CLIENT_SECRET")
    pid = os.environ.get("INFISICAL_PROJECT_ID")
    env = os.environ.get("INFISICAL_ENV", "prod")
    path = os.environ.get("INFISICAL_SECRET_PATH", "/llm")
    name = os.environ.get("INFISICAL_SECRET_NAME", "OPENROUTER_API")
    missing = [k for k, v in {
        "INFISICAL_API_URL": api, "INFISICAL_CLIENT_ID": cid,
        "INFISICAL_CLIENT_SECRET": csec, "INFISICAL_PROJECT_ID": pid,
    }.items() if not v]
    if missing:
        raise ConfigError(
            "No OPENROUTER_API_KEY and missing Infisical config: "
            + ", ".join(missing)
        )

    with httpx.Client(timeout=30) as c:
        r = c.post(
            f"{api}/api/v1/auth/universal-auth/login",
            json={"clientId": cid, "clientSecret": csec},
        )
        r.raise_for_status()
        token = r.json().get("accessToken", "")
        if not token:
            raise ConfigError("Infisical auth returned no accessToken")
        r = c.get(
            f"{api}/api/v3/secrets/raw/{name}",
            params={"workspaceId": pid, "environment": env, "secretPath": path},
            headers={"Authorization": f"Bearer {token}"},
        )
        r.raise_for_status()
        val = r.json().get("secret", {}).get("secretValue", "")
    if not val:
        raise ConfigError(
            f"Infisical secret {name} ({env}{path}) is empty/not found"
        )
    LOG.info("OpenRouter key resolved from Infisical (%s %s%s)", name, env, path)
    return val


# key cached in-process only
_KEY: str | None = None


def _key() -> str:
    global _KEY
    if _KEY is None:
        _KEY = _resolve_openrouter_key()
    return _KEY


def _auth_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_key()}",
        "Content-Type": "application/json",
        "HTTP-Referer": REFERER,
        "X-Title": TITLE,
    }


# --------------------------------------------------------------------------- #
# Helpers                                                                      #
# --------------------------------------------------------------------------- #
def _redact(text: str) -> str:
    """Strip anything that looks like a bearer token from error text."""
    return re.sub(r"(?i)bearer\s+[A-Za-z0-9._\-]+", "Bearer <redacted>", text)


def _sanitize_slug(s: str, maxlen: int = 40) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-._")
    return (s[:maxlen] or "img").lower()


def _unique_path(model: str, idx: int, ext: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stem = f"{ts}_{_sanitize_slug(model.replace('/', '-'))}_{idx}_{uuid.uuid4().hex[:8]}"
    p = (OUTPUT_DIR / f"{stem}.{ext}").resolve()
    # defense-in-depth: never escape OUTPUT_DIR
    if OUTPUT_DIR not in p.parents and p.parent != OUTPUT_DIR:
        raise ConfigError("refusing to write outside output directory")
    while p.exists():  # never overwrite
        p = (OUTPUT_DIR / f"{stem}_{uuid.uuid4().hex[:4]}.{ext}").resolve()
    return p


def _resolve_output_dir(output_directory: str | None) -> Path:
    """Resolve an optional caller-supplied subdir, confined under OUTPUT_DIR."""
    if not output_directory:
        return OUTPUT_DIR
    sub = Path(output_directory)
    if sub.is_absolute():
        cand = sub.resolve()
    else:
        cand = (OUTPUT_DIR / sub).resolve()
    if OUTPUT_DIR != cand and OUTPUT_DIR not in cand.parents:
        raise ConfigError(
            f"output_directory must stay under {OUTPUT_DIR}"
        )
    cand.mkdir(parents=True, exist_ok=True)
    return cand


def _err(e: Exception) -> list[TextContent]:
    if isinstance(e, httpx.HTTPStatusError):
        body = _redact(e.response.text)[:600]
        msg = f"OpenRouter HTTP {e.response.status_code}: {body}"
    elif isinstance(e, httpx.TimeoutException):
        msg = f"OpenRouter request timed out after {HTTP_TIMEOUT}s"
    elif isinstance(e, httpx.HTTPError):
        msg = f"HTTP error contacting OpenRouter: {_redact(str(e))}"
    else:
        msg = f"{type(e).__name__}: {_redact(str(e))}"
    LOG.error(msg)
    return [TextContent(type="text", text=json.dumps({"ok": False, "error": msg}))]


def _ok(obj: Any) -> list[TextContent]:
    return [TextContent(type="text", text=json.dumps(obj, indent=2))]


def _models_cache_fetch(client: httpx.Client) -> list[dict]:
    r = client.get(f"{OPENROUTER_BASE}/images/models", headers=_auth_headers())
    r.raise_for_status()
    return r.json().get("data", [])


def _supports_refs(m: dict) -> bool:
    """Authoritative reference-image check: a model supports image-to-image when
    'input_references' is in its supported_parameters. Fall back to the coarser
    architecture.input_modalities signal."""
    sp = m.get("supported_parameters", {}) or {}
    if isinstance(sp, dict) and "input_references" in sp:
        return True
    in_mod = (m.get("architecture", {}) or {}).get("input_modalities", []) or []
    return "image" in in_mod


def _summarize_model(m: dict) -> dict:
    sp = m.get("supported_parameters", {}) or {}
    # pull aspect/resolution value lists when present
    def _vals(key: str):
        v = sp.get(key)
        if isinstance(v, dict):
            return v.get("values")
        return None
    pricing = m.get("pricing") or m.get("price")  # best-effort; may be absent
    return {
        "id": m.get("id"),
        "name": m.get("name"),
        "supported_parameters": sorted(sp.keys()) if isinstance(sp, dict) else sp,
        "aspect_ratios": _vals("aspect_ratio"),
        "resolutions": _vals("resolution"),
        "supports_reference_image": _supports_refs(m),
        "supports_streaming": m.get("supports_streaming"),
        "pricing": pricing,
        "endpoints": m.get("endpoints"),
    }


def _build_gen_body(args: dict) -> dict:
    body: dict[str, Any] = {
        "model": args["model"],
        "prompt": args["prompt"],
    }
    for opt in ("aspect_ratio", "resolution", "quality", "output_format"):
        if args.get(opt):
            body[opt] = args[opt]
    n = int(args.get("n", 1) or 1)
    if n < 1 or n > 10:
        raise ConfigError("n must be between 1 and 10")
    body["n"] = n
    return body


def _save_images(data: list[dict], model: str, out_dir: Path) -> list[dict]:
    saved = []
    for i, item in enumerate(data):
        b64 = item.get("b64_json")
        if not b64:
            continue
        media = item.get("media_type") or "image/png"
        ext = _EXT_BY_MEDIA.get(media, "png")
        try:
            raw = base64.b64decode(b64, validate=True)
        except (binascii.Error, ValueError) as ex:
            raise ConfigError(f"invalid base64 image data at index {i}: {ex}")
        # place under resolved out_dir (may be subdir of OUTPUT_DIR)
        global OUTPUT_DIR
        _orig = OUTPUT_DIR
        try:
            OUTPUT_DIR = out_dir
            p = _unique_path(model, i, ext)
        finally:
            OUTPUT_DIR = _orig
        p.write_bytes(raw)
        saved.append({"path": str(p), "media_type": media, "bytes": len(raw)})
    return saved


def _file_to_data_url(path_str: str) -> str:
    p = Path(path_str).resolve()
    if not p.is_file():
        raise ConfigError(f"reference_image not found: {path_str}")
    data = p.read_bytes()
    if len(data) > 16 * 1024 * 1024:
        raise ConfigError("reference_image exceeds 16MB")
    ext = p.suffix.lower().lstrip(".")
    media = {
        "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "webp": "image/webp", "gif": "image/gif",
    }.get(ext, "image/png")
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{media};base64,{b64}"


# --------------------------------------------------------------------------- #
# MCP server + tool registry                                                   #
# --------------------------------------------------------------------------- #
app = Server("openrouter-image")

_GEN_OPTS = {
    "aspect_ratio": {"type": "string", "description": "e.g. 1:1, 16:9, 9:16, auto"},
    "resolution": {"type": "string", "description": "tier: 512, 768, 1K, 2K, 4K"},
    "quality": {"type": "string", "description": "auto, low, medium, high, xhigh, max"},
    "output_format": {"type": "string", "description": "png, jpeg, webp, svg"},
    "n": {"type": "integer", "description": "number of images (1-10), default 1"},
    "output_directory": {
        "type": "string",
        "description": "optional subdir under the server output dir",
    },
}


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_image_models",
            description=(
                "List OpenRouter image-generation models with slug, supported "
                "parameters, aspect ratios/resolutions (when available), "
                "reference-image capability, and pricing (when available). "
                "Returns a compact summary, not raw API dumps."
            ),
            inputSchema={"type": "object", "properties": {}, "additionalProperties": False},
        ),
        Tool(
            name="get_image_model_capabilities",
            description=(
                "Return the supported parameters, endpoints, and capabilities "
                "for a single image model slug. Call before generation/editing."
            ),
            inputSchema={
                "type": "object",
                "properties": {"model": {"type": "string", "description": "model slug"}},
                "required": ["model"],
                "additionalProperties": False,
            },
        ),
        Tool(
            name="generate_image",
            description=(
                "Generate image(s) from a text prompt via OpenRouter POST "
                "/api/v1/images. Saves decoded images to the server's persistent "
                "output dir and returns paths, model, media type and reported "
                "cost. Never returns raw base64."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string"},
                    "model": {"type": "string"},
                    **_GEN_OPTS,
                },
                "required": ["prompt", "model"],
                "additionalProperties": False,
            },
        ),
        Tool(
            name="edit_image",
            description=(
                "Image-to-image: guide generation with a local reference image. "
                "Verifies the model supports input_references, encodes the file "
                "as a data URL, sends via input_references, saves output, returns "
                "paths + cost. Never prints the reference base64."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string"},
                    "model": {"type": "string"},
                    "reference_image": {"type": "string", "description": "local file path"},
                    **_GEN_OPTS,
                },
                "required": ["prompt", "model", "reference_image"],
                "additionalProperties": False,
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "list_image_models":
            with httpx.Client(timeout=HTTP_TIMEOUT) as c:
                models = _models_cache_fetch(c)
            return _ok({"ok": True, "count": len(models),
                        "models": [_summarize_model(m) for m in models]})

        if name == "get_image_model_capabilities":
            slug = arguments["model"]
            with httpx.Client(timeout=HTTP_TIMEOUT) as c:
                models = _models_cache_fetch(c)
            match = next((m for m in models if m.get("id") == slug), None)
            if not match:
                return _ok({"ok": False, "error": f"unknown model slug: {slug}",
                            "hint": "call list_image_models for valid slugs"})
            return _ok({"ok": True, "model": _summarize_model(match)})

        if name == "generate_image":
            body = _build_gen_body(arguments)
            out_dir = _resolve_output_dir(arguments.get("output_directory"))
            with httpx.Client(timeout=HTTP_TIMEOUT) as c:
                r = c.post(f"{OPENROUTER_BASE}/images",
                           headers=_auth_headers(), json=body)
                r.raise_for_status()
                resp = r.json()
            saved = _save_images(resp.get("data", []), body["model"], out_dir)
            usage = resp.get("usage", {}) or {}
            return _ok({"ok": True, "model": body["model"], "images": saved,
                        "cost": usage.get("cost"), "usage": usage,
                        "created": resp.get("created")})

        if name == "edit_image":
            slug = arguments["model"]
            with httpx.Client(timeout=HTTP_TIMEOUT) as c:
                models = _models_cache_fetch(c)
                match = next((m for m in models if m.get("id") == slug), None)
                if not match:
                    return _ok({"ok": False, "error": f"unknown model slug: {slug}"})
                if not _supports_refs(match):
                    sp = sorted((match.get("supported_parameters", {}) or {}).keys())
                    return _ok({"ok": False,
                                "error": f"model {slug} does not support reference images "
                                         f"(input_references not in supported_parameters={sp})"})
                data_url = _file_to_data_url(arguments["reference_image"])
                body = _build_gen_body(arguments)
                body["input_references"] = [
                    {"type": "image_url", "image_url": {"url": data_url}}
                ]
                out_dir = _resolve_output_dir(arguments.get("output_directory"))
                r = c.post(f"{OPENROUTER_BASE}/images",
                           headers=_auth_headers(), json=body)
                r.raise_for_status()
                resp = r.json()
            saved = _save_images(resp.get("data", []), slug, out_dir)
            usage = resp.get("usage", {}) or {}
            return _ok({"ok": True, "model": slug, "images": saved,
                        "cost": usage.get("cost"), "usage": usage,
                        "created": resp.get("created")})

        return _ok({"ok": False, "error": f"unknown tool: {name}"})
    except KeyError as e:
        return _err(ConfigError(f"missing required argument: {e}"))
    except Exception as e:  # noqa: BLE001 - surface a clean error to the client
        return _err(e)


async def _main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG.info("openrouter-image MCP starting; output dir=%s", OUTPUT_DIR)
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())


if __name__ == "__main__":
    import anyio
    anyio.run(_main)
