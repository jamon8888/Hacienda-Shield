"""Compatibility checks for the Hacienda Shield rebrand."""

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent


def test_canonical_server_module_exists():
    assert (ROOT_DIR / "server" / "hacienda_shield_server.py").exists()


def test_legacy_import_alias_exposes_engine():
    from pii_shield_server import PIIEngine
    from hacienda_shield_server import PIIEngine as NewPIIEngine

    assert PIIEngine is NewPIIEngine


def test_new_setup_scripts_exist():
    assert (ROOT_DIR / "setup_hacienda_shield.py").exists()
    assert (ROOT_DIR / "setup_hacienda_shield.bat").exists()
    assert (ROOT_DIR / "setup_hacienda_shield.sh").exists()


def test_legacy_setup_python_wrapper_delegates():
    wrapper = (ROOT_DIR / "setup_pii_shield.py").read_text(encoding="utf-8")
    assert "from setup_hacienda_shield import main" in wrapper


def test_legacy_setup_batch_wrapper_delegates():
    wrapper = (ROOT_DIR / "setup_pii_shield.bat").read_text(encoding="utf-8")
    assert "setup_hacienda_shield.py" in wrapper


def test_legacy_setup_shell_wrapper_delegates():
    wrapper = (ROOT_DIR / "setup_pii_shield.sh").read_text(encoding="utf-8")
    assert "setup_hacienda_shield.py" in wrapper
