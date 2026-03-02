"""Developer onboarding check script."""

import importlib
import os
import subprocess
import sys
import urllib.request
from datetime import datetime


def check_python_version():
    """Check if Python version is >= 3.10."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    if version.major == 3 and version.minor >= 10:
        print(f"[PASS] Python version: {version_str} (>= 3.10 required)")
        return "PASS", f"Python version: {version_str}"
    print(f"[WARN] Python version: {version_str} (< 3.10 — upgrade recommended)")
    return "FAIL", f"Python version: {version_str} (< 3.10)"


def check_virtual_environment():
    """Check if a virtual environment is currently active."""
    # Works for both venv and Conda environments
    conda_env = os.environ.get("CONDA_DEFAULT_ENV")
    venv_env = os.environ.get("VIRTUAL_ENV")

    if conda_env and conda_env != "base":
        print(f"[PASS] Virtual environment: Active ({conda_env})")
        return "PASS", f"Virtual environment: Active ({conda_env})"
    if venv_env:
        env_name = os.path.basename(venv_env)
        print(f"[PASS] Virtual environment: Active ({env_name})")
        return "PASS", f"Virtual environment: Active ({env_name})"

    print("[FAIL] Virtual environment: Not active — please activate one")
    return "FAIL", "Virtual environment: Not active"


def check_package_import(package_name):
    """Try importing a package and return its version."""
    try:
        mod = importlib.import_module(package_name)
        version = getattr(mod, "__version__", "unknown")
        print(f"[PASS] {package_name} installed: version {version}")
        return "PASS", f"{package_name} installed: version {version}"
    except ImportError:
        print(f"[FAIL] {package_name}: Not installed")
        return "FAIL", f"{package_name}: Not installed"


def check_internet_connectivity():
    """Check internet connectivity by hitting a known URL."""
    url = "https://www.google.com"
    try:
        with urllib.request.urlopen(url, timeout=5):
            print("[PASS] Internet connectivity: OK")
            return "PASS", "Internet connectivity: OK"
    except Exception:  # pylint: disable=broad-except
        print("[FAIL] Internet connectivity: Failed")
        return "FAIL", "Internet connectivity: Failed"


def list_installed_packages():
    """List all installed packages and their versions."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format=columns"],
        capture_output=True,
        text=True,
        check=False,
    )
    print("\n--- Installed Packages ---")
    print(result.stdout)
    print("--------------------------\n")


def generate_report(results):
    """Generate and save summary report."""
    passed = sum(1 for status, _ in results.values() if status == "PASS")
    total = len(results)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "=== Developer Onboarding Check ===",
        f"Generated: {timestamp}",
        "",
    ]
    for label, (status, detail) in results.items():
        lines.append(f"[{status}] {detail}")

    lines += [
        "",
        f"--- Result: {passed}/{total} checks passed {'✓' if passed == total else '✗'}",
    ]

    report_text = "\n".join(lines)
    print("\n" + report_text)

    with open("setup_report.txt", "w", encoding="utf-8") as report_file:
        report_file.write(report_text + "\n")

    print("\nReport saved to: setup_report.txt")


def main():
    """Run all onboarding checks."""
    print("=== Developer Onboarding Check ===\n")
    list_installed_packages()

    results = {}
    results["python_version"] = check_python_version()
    results["virtual_env"] = check_virtual_environment()
    results["pylint"] = check_package_import("pylint")
    results["black"] = check_package_import("black")
    results["internet"] = check_internet_connectivity()
    results["numpy"] = check_package_import("numpy")

    generate_report(results)


if __name__ == "__main__":
    main()
