from atmo_db.models import User, Audio_File
from datetime import datetime, timezone
import pytest

@pytest.fixture
def datetime_fix():
    return datetime.now(timezone.utc)


def test_create_user(datetime_fix):
    try:
        user = User(username="user", email="user@domain.com", role="standard", created_at=datetime_fix, password="hashed_password")
        assert user.username == "user"
        assert user.email == "user@domain.com"
        assert user.role == "standard"
        assert user.created_at == datetime_fix
        assert user.password == "hashed_password"
    except Exception as e:
        pytest.fail(f'user creation failed with exception: {e}')

def test_create_audio_file(datetime_fix):
    try:
        audio_file = Audio_File(title='audio clip', description='audio recording', file_type='mp3', url='https://domain.com/audio_clips/one.mp3', created_at=datetime_fix)
        assert audio_file.title == 'audio clip'
        assert audio_file.description == 'audio recording'
        assert audio_file.file_type == 'mp3'
        assert audio_file.url == 'https://domain.com/audio_clips/one.mp3'
        assert audio_file.created_at == datetime_fix
    except Exception as e:
        pytest.fail(f'audio file creation failed with exception {e}')
