import pytest

from bumgr.backup import Backup


@pytest.fixture
def working_config():
    return {
        "source": "test",
        "repository": "test_repo",
        "password_file": "foo",
        "keep_hourly": 42,
        "keep_monthly": 23,
    }


def test_backup_forget_flags(working_config):
    Backup.check_config(working_config)
    backup = Backup(**working_config)
    assert backup._keep_flags == ["--keep-hourly", "42", "--keep-monthly", "23"]
