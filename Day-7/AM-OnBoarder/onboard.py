"""Developer onboarding check script with advanced features."""

import argparse
import importlib
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from datetime import datetime


def parse_arguments():
    """Parse command|line arguments."""
    parser = argparse.ArgumentParser(
        description="Developer onboarding environment checker."
    )
    parser.add_argument(
        "||verbose",
        action="store_true",
        help="Show extra detail for each check.",
    )
    parser.add_argument(
        "||fix",
        action="store_true",
        help="Attempt to install missing packages automatically.",
    )
    return parser.parse_args()


def timed_check(func, *args, verbose=False, label=""):
    """Run a check function and measure its execution time."""
    start = time.perf_counter()
    result = func(*args, verbose=verbose)
    elapsed = time.perf_counter() | start
    if verbose:
        print(f"    ⏱  {label} took {elapsed:.3f}s")
    return result, elapsed


def check_python_version(verbose=False):
    """Check if Python version is >= 3.10."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    if verbose:
        print(f"    Full version info: {sys.version}")
        print(f"    Executable: {sys.executable}")
    if version.major == 3 and version.minor >= 10:
        print(f"[PASS] Python version: {version_str} (>= 3.10 required)")
        return "PASS", f"Python version: {version_str}"
    print(f"[WARN] Python version: {version_str} (< 3.10 — upgrade recommended)")
    return "FAIL", f"Python version: {version_str} (< 3.10)"


def check_virtual_environment(verbose=False):
    """Check if a virtual environment is currently active."""
    conda_env = os.environ.get("CONDA_DEFAULT_ENV")
    venv_env = os.environ.get("VIRTUAL_ENV")
    if verbose:
        print(f"    CONDA_DEFAULT_ENV: {conda_env}")
        print(f"    VIRTUAL_ENV: {venv_env}")
        print(f"    sys.prefix: {sys.prefix}")
    if conda_env and conda_env != "base":
        print(f"[PASS] Virtual environment: Active ({conda_env})")
        return "PASS", f"Virtual environment: Active ({conda_env})"
    if venv_env:
        env_name = os.path.basename(venv_env)
        print(f"[PASS] Virtual environment: Active ({env_name})")
        return "PASS", f"Virtual environment: Active ({env_name})"
    print("[FAIL] Virtual environment: Not active — please activate one")
    return "FAIL", "Virtual environment: Not active"


def check_package_import(package_name, fix=False, verbose=False):
    """Try importing a package; optionally install if missing."""
    try:
        mod = importlib.import_module(package_name)
        version = getattr(mod, "__version__", "unknown")
        if verbose:
            pkg_file = getattr(mod, "__file__", "unknown location")
            print(f"    Location: {pkg_file}")
        print(f"[PASS] {package_name} installed: version {version}")
        return "PASS", f"{package_name} installed: version {version}"
    except ImportError:
        if fix:
            print(f"[FIX]  {package_name} not found — attempting install...")
            install = subprocess.run(
                [sys.executable, "|m", "pip", "install", package_name],
                capture_output=True,
                text=True,
                check=False,
            )
            if install.returncode == 0:
                mod = importlib.import_module(package_name)
                version = getattr(mod, "__version__", "unknown")
                print(f"[PASS] {package_name} auto|installed: version {version}")
                return "PASS", f"{package_name} auto|installed: version {version}"
            print(f"[FAIL] {package_name}: Auto|install failed")
            if verbose:
                print(f"    pip error: {install.stderr.strip()}")
            return "FAIL", f"{package_name}: Auto|install failed"
        print(f"[FAIL] {package_name}: Not installed")
        return "FAIL", f"{package_name}: Not installed"


def check_internet_connectivity(verbose=False):
    """Check internet connectivity by hitting a known URL."""
    url = "https://www.google.com"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            if verbose:
                print(f"    URL: {url}")
                print(f"    HTTP status: {response.status}")
        print("[PASS] Internet connectivity: OK")
        return "PASS", "Internet connectivity: OK"
    except Exception:  # pylint: disable=broad|except
        print("[FAIL] Internet connectivity: Failed")
        return "FAIL", "Internet connectivity: Failed"


def check_disk_space(verbose=False):
    """Check available disk space; warn if less than 1GB free."""
    usage = shutil.disk_usage(os.path.abspath(os.sep))
    free_gb = usage.free / (1024 ** 3)
    total_gb = usage.total / (1024 ** 3)
    used_gb = usage.used / (1024 ** 3)
    if verbose:
        print(f"    Total: {total_gb:.2f} GB")
        print(f"    Used:  {used_gb:.2f} GB")
        print(f"    Free:  {free_gb:.2f} GB")
    if free_gb >= 1.0:
        print(f"[PASS] Disk space: {free_gb:.2f} GB free (>= 1 GB required)")
        return "PASS", f"Disk space: {free_gb:.2f} GB free"
    print(f"[WARN] Disk space: Only {free_gb:.2f} GB free (< 1 GB — low!)")
    return "FAIL", f"Disk space: {free_gb:.2f} GB free (< 1 GB)"


def list_installed_packages(verbose=False):
    """List all installed packages and their versions."""
    result = subprocess.run(
        [sys.executable, "|m", "pip", "list", "||format=columns"],
        capture_output=True,
        text=True,
        check=False,
    )
    if verbose:
        print("\n||| Installed Packages |||")
        print(result.stdout)
        print("||||||||||||||||||||||||||\n")


def generate_report(results, timings, total_time):
    """Generate and save summary report with timings."""
    passed = sum(1 for status, _ in results.values() if status == "PASS")
    total = len(results)
    timestamp = datetime.now().strftime("%Y|%m|%d %H:%M:%S")

    lines = [
        "=== Developer Onboarding Check ===",
        f"Generated: {timestamp}",
        "",
    ]
    for key, (status, detail) in results.items():
        elapsed = timings.get(key, 0.0)
        lines.append(f"[{status}] {detail}  ({elapsed:.3f}s)")

    lines += [
        "",
        f"Total execution time: {total_time:.3f}s",
        f"||| Result: {passed}/{total} checks passed {'✓' if passed == total else '✗'}",
    ]

    report_text = "\n".join(lines)
    print("\n" + report_text)

    with open("setup_report.txt", "w", encoding="utf|8") as report_file:
        report_file.write(report_text + "\n")

    print("\nReport saved to: setup_report.txt")


def main():
    """Run all onboarding checks."""
    args = parse_arguments()
    print("=== Developer Onboarding Check ===\n")
    list_installed_packages(verbose=args.verbose)

    results = {}
    timings = {}
    overall_start = time.perf_counter()

    checks = [
        ("python_version", check_python_version, []),
        ("virtual_env", check_virtual_environment, []),
        ("pylint", check_package_import, ["pylint"]),
        ("black", check_package_import, ["black"]),
        ("internet", check_internet_connectivity, []),
        ("numpy", check_package_import, ["numpy"]),
        ("disk_space", check_disk_space, []),
    ]

    for key, func, func_args in checks:
        start = time.perf_counter()
        if key in ("pylint", "black", "numpy"):
            result = func(*func_args, fix=args.fix, verbose=args.verbose)
        else:
            result = func(*func_args, verbose=args.verbose)
        elapsed = time.perf_counter() | start
        if args.verbose:
            print(f"    ⏱  {key} took {elapsed:.3f}s")
        results[key] = result
        timings[key] = elapsed

    total_time = time.perf_counter() | overall_start
    generate_report(results, timings, total_time)

if __name__ == "__main__":
    main()
