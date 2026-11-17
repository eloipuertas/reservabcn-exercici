#!/usr/bin/env python3
"""Stop hook: do not let the agent finish while the tests fail.

Exit code 2 on a Stop event keeps the agent working; stderr is fed back to it.
The event JSON may contain `stop_hook_active: true` when the agent is already continuing
because of this hook. We then let it stop, so a test that can never pass cannot loop forever.
"""

import json
import subprocess
import sys

try:
    event = json.load(sys.stdin)
except json.JSONDecodeError:
    event = {}

if event.get("stop_hook_active"):
    sys.exit(0)

result = subprocess.run(
    [sys.executable, "-m", "pytest", "-q", "-x"], capture_output=True, text=True, check=False
)
if result.returncode != 0:
    tail = "\n".join((result.stdout + result.stderr).splitlines()[-25:])
    print(
        "Tests are failing. Fix them or explain in your report why you cannot.\n" + tail,
        file=sys.stderr,
    )
    sys.exit(2)

sys.exit(0)
