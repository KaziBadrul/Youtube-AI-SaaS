"""Separate production process; provider/alignment/FFmpeg execution belongs here."""
from alpha.processes import refuse_unconfigured_execution

def main():
    return refuse_unconfigured_execution("production worker")

if __name__ == "__main__":
    raise SystemExit(main())
