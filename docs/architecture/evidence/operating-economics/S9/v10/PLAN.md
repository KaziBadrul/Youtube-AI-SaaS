# V10 whole-guest test plan

Native ARM64 Lima 2.2.1 / Apple Virtualization.framework, Ubuntu 24.04 official server cloud image (620,224,512 bytes), 1 vCPU, 2 GiB configured guest physical RAM, 50 GiB sparse root disk, no swap, no containers/Rosetta. All workload inputs copied into guest ext4; no shared media/cache filesystem during measurement. Systemd, SSH, networking, journald and normal guest services remain active and measured. No primary environment settings changed.

Download Lima (38,328,082 bytes) and Ubuntu image, apt FFmpeg/Python venv dependencies and pinned PyPI native ARM64 stack as necessary. Existing model/font/media reused. Package receipts retained.

Preserve historical sources. Measure guest idle, web+worker baseline, existing local Whisper base, fresh 112-scene ten-minute S6 render, unchanged full S6 validation, unchanged V9 five-project full-memory backup serialized, cancellation/lock release only after group cessation. Keep web/probes alive across phases; sample global /proc/meminfo, vmstat, PSI, RSS, disk, CPU and kernel logs. No swap/cache dropping/overcommit changes to force success.

A failure stays a failure. Completion alone is insufficient safety evidence. Report headroom; absent an established numeric safety policy, low/unproven headroom is MARGINAL rather than resource-qualified. OOM/unusable required behavior is UNSAFE. True guest unavailable means BLOCKED with no container substitute. Overall S9 remains evidence-gated, not automatically PASS. No production/TASKS/provider/cloud/credit/allowance/tokenizer work.
