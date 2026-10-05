"""Separate coordinated backup/purge process, without generation authority."""
from alpha.processes import refuse_unconfigured_execution

def main():
    return refuse_unconfigured_execution("maintenance")

if __name__ == "__main__":
    raise SystemExit(main())
