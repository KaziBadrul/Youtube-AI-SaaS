# Local implementation orchestrator

This is development tooling, independent of the product Django application. `TASKS.md` remains unchanged specification authority. Runtime state lives in `.orchestrator/state.json`. Only independent OpenCode review can authorize acceptance; the runner never assesses implementation quality itself.

## Setup and commands

Requires Python 3.10+ on macOS/Linux, Git with a configured author identity, and installed/authenticated Codex and OpenCode CLIs. Standard-library only; no package installation needed. Configuration is `.orchestrator/config.json`; no credentials belong there. Defaults are three repairs after the initial attempt, 7,200-second agent timeout, and automatic continuation after an accepted checkpoint. Optional tasks (currently T093) require explicit owner activation by adding their IDs to `activated_optional_tasks`; this does not authorize live provider work.

```sh
python3 -m unittest discover -s tests/orchestrator -v
python3 orchestrator.py --dry-run
python3 orchestrator.py status
# Only after separate owner authorization for the first real implementation run:
python3 orchestrator.py run
python3 orchestrator.py resume
python3 orchestrator.py pause
python3 orchestrator.py stop
python3 tools/orchestrator_dashboard.py
```

`python` also works if it resolves to Python 3. Dry-run is genuinely read-only: no subprocesses, agents, state writes, directories or commits. It prints T001's proposed implementation/review prompts and commands while reporting zero completed tasks on this initial repository. Capability probes are deferred to actual run/resume. No real implementation run was performed while building this tooling.

The existing tracked **empty** state.json is recognized as an uninitialized placeholder and preserved by status/dry-run. Nonempty invalid state is never silently replaced. Runtime files are ignored; because Git already tracks the placeholder, ignoring alone does not untrack it. Before real execution, the operator should separately checkpoint the planning/tooling baseline and remove only this runtime placeholder from Git's index (`git rm --cached .orchestrator/state.json`), retaining the file locally. This is not done automatically.

## Installed agent commands and authority

Verified locally from `codex --help`, `codex exec --help`, `opencode --help`, and `opencode run --help`: **codex-cli 0.159.2** and **opencode v2.0.21**. Actual runs recheck the required help capabilities and stop on mismatch, without guessing flags.

Codex:

```text
codex -a never exec --sandbox workspace-write --ignore-user-config --ephemeral --color never -C <repository> -o <attempt>/codex-final.txt -
```

The prompt is supplied over stdin. `exec` is noninteractive; `-a never` disables interactive approvals and reports denied commands as execution failures. The workspace-write sandbox is retained. The installed alternative `--dangerously-bypass-approvals-and-sandbox` was detected but is deliberately not used: unattended approval behavior does not require removing the filesystem sandbox. Global Codex configuration is ignored to avoid importing configured product connectors/hooks into this run; CLI authentication still uses its normal credential store.

OpenCode:

```text
opencode run --standalone --auto --format default --file <attempt>/reviewer-prompt.txt 'Review the attached task contract independently.'
```

`--auto` auto-approves permissions not explicitly denied; `--standalone` uses a private server and each invocation starts a fresh session. This installation's CLI help exposes **no read-only execution flag**. The reviewer is instructed to read/test only, and its before/after repository fingerprint must match. Tracked and nonignored untracked content changes invalidate review; no files are blindly restored because concurrent human authorship cannot be determined. Tests may write ignored build/cache artifacts. OpenCode therefore is unattended but is **not an OS-enforced read-only reviewer**. No unsupported permission flags or undocumented configuration are invented.

Agents receive a minimal environment without inherited product API keys. HOME is retained for agent login; this is not an isolation boundary for an unrestricted OpenCode shell. Prompts forbid product APIs, deployment, spend, external secrets, global configuration, agent-created commits and frozen specification changes. Existing dirty paths and protected documents are fingerprinted and checked. Filesystem checks detect violations after execution; they cannot prevent every external side effect. Agent-service inference itself uses the operator's CLI subscription/account and is distinct from product-provider access; these tests make no real agent calls.

For a stronger boundary, run the tooling and authenticated CLIs in a dedicated development account/VM with no product credentials or unrelated private files. This v1 does not install a sandbox, firewall, Tailscale, services or machine configuration. The Codex shell sandbox and review fingerprints are practical restrictions, not proof against malicious agents. Live capabilities/evidence remain blocked without separately supplied owner authority; this runner does not grant or infer that authority.

## State, repairs, checkpoints and recovery

The kernel `flock` permits one controller; lock metadata is diagnostic only. A stale lock file can be reused after the kernel releases ownership; its inode is never deleted. State writes use temporary file, fsync, atomic rename and directory fsync. Append-oriented events include task/run/attempt identity. Routine output events report byte counts rather than private content; redacted outputs live in private attempt logs. Attempt paths include run identity: `.orchestrator/runs/T001/<run-id>/attempt-01/`.

Dirty working trees are recorded exactly. Pre-existing staged changes block execution. Unstaged unrelated changes may survive, but any overlap with agent changes blocks before review/checkpoint. Scope comes from the exact task contract; Codex's changed-file report must equal actual changed paths. Protected decisions/instructions/tooling, `.env`, key/secret patterns, generated media, binary assets and symlinks cannot be automatically checkpointed. New legitimate documentation outside frozen paths is allowed. Conservative filters can require human review for legitimate assets. Secret scanning is defense in depth and cannot guarantee detection of every unknown credential format.

A PASS receipt leads to a durable checkpoint intent, isolated Git index, `commit-tree`, and compare-and-swap `update-ref`; only accepted paths enter the tree. No `git add -A`, hooks, push, history rewrite or hard reset. The normal index is reconciled for accepted paths only; concurrent overlapping staged edits block. Checkpoint token/tree/parent/commit support recovery across commit-before-state crashes. Existing user changes are not included. Atomic Git objects/ref updates form a local checkpoint; no remote operation occurs.

Pause prevents launching another agent after the current agent ends. Stop/Ctrl+C/SIGTERM terminate only the currently owned subprocess group, escalating after three seconds. Stop writes a mailbox; it never kills a PID from stale state. Agents' own background service/daemon behavior cannot be exhaustively controlled by process groups; OpenCode is launched standalone and leftover group children receive termination.

`resume` can continue a durably completed implementation into independent review, restart an interrupted review of unchanged files, or reconcile an interrupted accepted checkpoint. It does not blindly rerun an interrupted implementation, infer completion from files, clear a blocker, or repeat product operations. If a recorded process identity is still live, resume refuses to launch another agent; operator inspection is required. PID reuse is checked against recorded `ps` start/group/command identity, never accepted solely from a PID.

Malformed reports/verdicts, crashes, timeouts, ambiguous modifications, missing decisions or exhausted repairs stop as BLOCKED/HUMAN_REVIEW_REQUIRED. Blocked `resume` does not auto-unblock. Operator reconciliation is deliberately manual in v1: stop the controller, inspect attempt receipts/logs/working tree, settle the blocker, then explicitly reconcile backed-up runtime state with the task's existing acceptance history. Never manufacture PASS or remove reservations/provider history. No unblock control appears in the dashboard. A changed TASKS.md hash requires human reconciliation before execution continues.

## Monitoring from desktop and phone

Default monitoring URL: **http://127.0.0.1:8765**. The dashboard uses a separate standard-library HTTP server and polls every two seconds. It exposes only read-only status and fixed assets; no shell/Git/task execution endpoints. The server uses field allowlists, output truncation, secret-pattern redaction, text-only rendering and no environment/config/prompt downloads. Redaction is best-effort: monitor output only on a trusted network, because arbitrary sensitive prose or unrecognized credentials cannot be guaranteed removed. Runtime logs should remain private.

Same LAN:

```sh
python3 tools/orchestrator_dashboard.py --host 0.0.0.0 --port 8765
```

The server prints discovered LAN URLs. On the phone, join the same trusted Wi-Fi and open the Mac's `http://<LAN-IP>:8765`. If discovery fails, find the IP in macOS System Settings → Wi-Fi → Details → TCP/IP, or use `ipconfig getifaddr en0` for the applicable interface. The macOS firewall may require allowing incoming access to this Python process; do not disable the firewall. There is no dashboard authentication, so explicit LAN binding makes logs visible to peers that can reach the port.

Existing Tailscale:

```sh
tailscale ip -4
python3 tools/orchestrator_dashboard.py --host <Mac-tailnet-IP> --port 8765
```

Open `http://<Mac-tailnet-IP>:8765` on a phone already connected to the same authorized tailnet. Restrict reachability using your existing tailnet access policy. Binding directly to the tailnet address is preferable for away-from-home monitoring; do not use public port forwarding, public tunnels or Tailscale Funnel. Tailscale is neither installed nor configured by this tooling. Binding to a specific tailnet address does not also open a localhost listener; use the printed tailnet URL on the Mac as well.

## Verification boundary

Automated tests use disposable Git repositories and fake injected agents/fake Python executables, never real Codex/OpenCode inference. They cover parser/dependencies/optional activation, strict receipts, failures/repairs/cutoff, scoped checkpoints, dirty overlap, crash recovery, atomic state, locks, controls, process groups, dashboard redaction/read-only HTTP and side-effect-free dry-run. Real agent authentication, model availability, terminal formatting and unattended end-to-end integration remain unproven until the separately authorized first real run. Functional tooling completion is not independent acceptance of any Txxx task.
