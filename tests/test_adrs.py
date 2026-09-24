import subprocess

def test_adrs_valid():
    r = subprocess.run(
        ["python", "scripts/validate_adrs.py"],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
