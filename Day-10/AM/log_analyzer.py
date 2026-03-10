from collections import Counter, defaultdict
from typing import List, Dict, Any


# Simulated server log as a list of strings
# Simple format: "timestamp level module message"
LOG_LINES = [
    "2026-03-10 09:00:01 INFO auth User logged in",
    "2026-03-10 09:00:05 ERROR payments Payment failed for order 123",
    "2026-03-10 09:00:10 WARNING auth Suspicious login attempt",
    "2026-03-10 09:00:15 ERROR db DB connection timeout",
    "2026-03-10 09:00:20 INFO api Request /products",
    "2026-03-10 09:00:25 ERROR payments Payment failed for order 124",
    "2026-03-10 09:00:30 CRITICAL db DB down",
    "2026-03-10 09:00:35 INFO auth User logged out",
    "2026-03-10 09:00:40 ERROR api 500 Internal Server Error",
    "2026-03-10 09:00:45 WARNING api Slow response",
]


def parse_log_line(line: str) -> Dict[str, Any]:
    """
    Parse a log line into a dict:
    {'timestamp': ..., 'level': ..., 'module': ..., 'message': ...}
    """
    parts = line.split()
    if len(parts) < 4:
        return {
            "timestamp": "",
            "level": "",
            "module": "",
            "message": line.strip(),
        }

    # timestamp = first two tokens
    timestamp = " ".join(parts[0:2])
    level = parts[2]
    module = parts[3]
    message = " ".join(parts[4:]) if len(parts) > 4 else ""

    return {
        "timestamp": timestamp,
        "level": level,
        "module": module,
        "message": message,
    }


def analyze_logs(log_lines: List[str]) -> Dict[str, Any]:
    """
    Build an analyzer that:
    - Parses each line into a dict
    - Uses Counter to find:
        * Most common error messages
        * Most active modules
        * Distribution of log levels
    - Uses defaultdict(list) to group errors by module
    - Returns summary dict:
      {
        'total_entries': n,
        'error_rate': x,
        'top_errors': [...],
        'busiest_module': ...,
        'level_distribution': {...},
        'errors_by_module': {...}
      }
    """
    parsed = [parse_log_line(line) for line in log_lines]

    total_entries = len(parsed)

    level_counter = Counter()
    module_counter = Counter()
    error_message_counter = Counter()
    errors_by_module = defaultdict(list)

    for entry in parsed:
        level = entry.get("level", "")
        module = entry.get("module", "")
        message = entry.get("message", "")

        if level:
            level_counter[level] += 1

        if module:
            module_counter[module] += 1

        if level in ("ERROR", "CRITICAL"):
            error_message_counter[message] += 1
            errors_by_module[module].append(message)

    total_errors = sum(level_counter[lvl] for lvl in ("ERROR", "CRITICAL"))
    error_rate = (total_errors / total_entries) * 100 if total_entries else 0.0

    # most_common() returns list of (item, count) pairs.[web:118][web:122][web:127]
    top_errors = error_message_counter.most_common(3)

    # busiest module: one with max log entries
    busiest_module = None
    if module_counter:
        busiest_module = module_counter.most_common(1)[0][0]

    summary = {
        "total_entries": total_entries,
        "error_rate": error_rate,
        "top_errors": top_errors,
        "busiest_module": busiest_module,
        "level_distribution": dict(level_counter),
        "errors_by_module": dict(errors_by_module),
    }

    return summary


if __name__ == "__main__":
    summary = analyze_logs(LOG_LINES)

    print("Total entries:", summary["total_entries"])
    print(f"Error rate: {summary['error_rate']:.2f}%")
    print("Level distribution:", summary["level_distribution"])
    print("Busiest module:", summary["busiest_module"])
    print("Top errors (message, count):")
    for msg, count in summary["top_errors"]:
        print(f"  {count}x - {msg}")

    print("\nErrors by module:")
    for module, messages in summary["errors_by_module"].items():
        print(f"  {module}:")
        for m in messages:
            print(f"    - {m}")