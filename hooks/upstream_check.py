#!/usr/bin/env python3
# Print the newest MidnightBSD amd64 point release version, e.g. "4.0.6".
# Empty output means "nothing detected" and is not an error; a non-zero
# exit means detection itself is broken (network error, HTTP error, or a
# page that no longer matches the expected shape) and must be reported by
# the caller, never swallowed. A failure must NEVER print a plausible-but-
# wrong version -- the version is only printed after every step below has
# succeeded.
#
# Source of truth:
#   https://midnightbsd.org/ftp/MidnightBSD/releases/amd64/ISO-IMAGES/
# (this is the exact directory conf/midnightbsd-*.conf's VM_ISO_LINK
# points into, e.g.
#   ".../ISO-IMAGES/4.0.6/MidnightBSD-4.0.6--amd64-disc1.iso").
#
# Fetched and confirmed by hand (2026-07-26): the directory is a plain
# Apache-style autoindex, one row per release directory, e.g.
#   <a href="4.0.4/">4.0.4/</a>   2026-03-31 17:29   -
#   <a href="4.0.5/">4.0.5/</a>   2026-05-20 16:41   -
#   <a href="4.0.6/">4.0.6/</a>   2026-06-16 13:16   -
# alongside a mix of bare two-part MAJOR.MINOR "collector" directories that
# are NOT individual point releases (e.g. "4.0/", "3.0/", "2.0/" -- every
# X.Y.Z point release also has an earlier-dated bare "X.Y/" sibling in this
# listing). conf/*.conf's VM_RELEASE is always the full three-part point
# release ("4.0.6", never "4.0"), so the pattern requires exactly three
# dot-separated digit groups, which a bare "X.Y/" entry can never satisfy.
# At fetch time the newest real point release was 4.0.6 (2026-06-16),
# matching the current conf/midnightbsd-4.0.6.conf.
#
# stdlib only (urllib.request, re, sys, os) -- no external dependencies.

import os
import re
import sys
import urllib.request

URL = "https://midnightbsd.org/ftp/MidnightBSD/releases/amd64/ISO-IMAGES/"
TIMEOUT = 60
USER_AGENT = "anyvm-org-upstream-watcher/1.0"

# Exactly three dot-separated digit groups -- a bare "X.Y/" collector
# directory (no point-release digit) never matches.
PATTERN = re.compile(r'href="(\d+\.\d+\.\d+)/"')


def resolve_natural_key():
    """Return the engine's own natural_key, or fail loudly.

    watch.yml clones base-builder INTO the builder repo root, so at
    detection time it sits at "base-builder/" (relative to this hook's
    cwd, the builder repo root). A local checkout instead has it as a
    sibling, "../base-builder". Try both, in that order.

    There is deliberately NO local fallback copy. Ordering must be the
    single rule the engine uses -- a per-hook duplicate would have to be
    kept in sync by hand across every builder and would drift silently,
    and a hook that ranks versions differently from watch.py is worse
    than one that refuses to run. Both real contexts (CI and a local
    sibling checkout) always provide base-builder, so an ImportError here
    means the environment is wrong: report it as broken detection rather
    than guessing an order.
    """
    for candidate in ("base-builder", os.path.join("..", "base-builder")):
        if not os.path.isdir(candidate):
            continue
        path = os.path.abspath(candidate)
        if path not in sys.path:
            sys.path.insert(0, path)
        try:
            import gendata
            return gendata.natural_key
        except ImportError:
            continue
    raise ImportError(
        "base-builder/gendata.py not importable from %s; expected it at "
        "./base-builder (CI) or ../base-builder (local checkout)"
        % os.getcwd())


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode("utf-8", "replace")


def main():
    try:
        key = resolve_natural_key()
    except ImportError as e:
        sys.stderr.write("upstream_check: %s\n" % e)
        return 1
    try:
        html = fetch(URL)
    except Exception as e:
        sys.stderr.write("upstream_check: fetch of %s failed: %s\n"
                         % (URL, e))
        return 1
    versions = PATTERN.findall(html)
    if not versions:
        sys.stderr.write("upstream_check: no X.Y.Z release directory "
                         "found in %s; page shape may have changed\n" % URL)
        return 1
    newest = sorted(set(versions), key=key)[-1]
    print(newest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
