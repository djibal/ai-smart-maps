import subprocess

def test_links():
    r = subprocess.run(
        ["python", "scripts/check_links.py"],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
