import os
import json
import shutil
import tempfile
from pathlib import Path
import pytest
from click.testing import CliRunner
from unittest.mock import patch
from envcloak.cli import main
from envcloak.generator import derive_key


@pytest.fixture
def isolated_mock_files():
    """
    Provide isolated mock files in a temporary directory for each test.
    Prevents modification of the original mock files.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        mock_dir = Path("tests/mock")

        # Copy all mock files to the temporary directory
        for file in mock_dir.iterdir():
            if file.is_file():
                shutil.copy(file, temp_dir_path / file.name)

        yield temp_dir_path
        # Cleanup is handled automatically by TemporaryDirectory


@pytest.fixture(scope="module")
def test_dir():
    """
    Create a temporary directory for tests and ensure cleanup after all tests.
    """
    temp_dir = Path("tests/temp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_files(test_dir):
    """
    Fixture for mock files within the `tests/temp` directory.
    """
    mock_dir = Path("tests/mock")
    input_file = mock_dir / "variables.env"
    encrypted_file = mock_dir / "variables.env.enc"
    decrypted_file = test_dir / "variables.env.decrypted"
    key_file = test_dir / "mykey.key"
    password = "JustGiveItATry"
    salt = "e3a1c8b0d4f6e2c7a5b9d6f0c3e8f1a2"

    # Derive the key using the password and salt
    derived_key = derive_key(password, bytes.fromhex(salt))
    key_file.write_bytes(derived_key)

    return input_file, encrypted_file, decrypted_file, key_file


@pytest.fixture
def runner():
    """
    Fixture for Click CLI Runner.
    """
    return CliRunner()


@patch("envcloak.cli.encrypt_file")
def test_encrypt(mock_encrypt_file, runner, isolated_mock_files):
    """
    Test the `encrypt` CLI command.
    """
    input_file = isolated_mock_files / "variables.env"
    encrypted_file = isolated_mock_files / "variables.temp.enc"  # Use unique temp file
    key_file = isolated_mock_files / "mykey.key"

    def mock_encrypt(input_path, output_path, key):
        assert os.path.exists(input_path), "Input file does not exist"
        with open(output_path, "w") as f:
            f.write(json.dumps({"ciphertext": "encrypted_data"}))

    mock_encrypt_file.side_effect = mock_encrypt

    result = runner.invoke(
        main,
        [
            "encrypt",
            "--input",
            str(input_file),
            "--output",
            str(encrypted_file),
            "--key-file",
            str(key_file),
        ],
    )

    assert result.exit_code == 0
    assert "File" in result.output
    mock_encrypt_file.assert_called_once_with(
        str(input_file), str(encrypted_file), key_file.read_bytes()
    )


@patch("envcloak.cli.decrypt_file")
def test_decrypt(mock_decrypt_file, runner, mock_files):
    """
    Test the `decrypt` CLI command.
    """
    _, encrypted_file, decrypted_file, key_file = mock_files

    # Use a unique temporary output file
    temp_decrypted_file = decrypted_file.with_name("variables.temp.decrypted")

    def mock_decrypt(input_path, output_path, key):
        assert os.path.exists(input_path), "Encrypted file does not exist"
        with open(output_path, "w") as f:
            f.write("DB_USERNAME=example_user\nDB_PASSWORD=example_pass")

    mock_decrypt_file.side_effect = mock_decrypt

    result = runner.invoke(
        main,
        [
            "decrypt",
            "--input",
            str(encrypted_file),
            "--output",
            str(temp_decrypted_file),
            "--key-file",
            str(key_file),
        ],
    )

    assert result.exit_code == 0
    assert "File" in result.output
    mock_decrypt_file.assert_called_once_with(
        str(encrypted_file), str(temp_decrypted_file), key_file.read_bytes()
    )

    # Clean up: Remove temp decrypted file
    if temp_decrypted_file.exists():
        temp_decrypted_file.unlink()


@patch("envcloak.cli.add_to_gitignore")
@patch("envcloak.cli.generate_key_file")
def test_generate_key_with_gitignore(
    mock_generate_key_file, mock_add_to_gitignore, runner, test_dir
):
    """
    Test the `generate-key` CLI command with default behavior (adds to .gitignore).
    """
    # Use a unique temporary file for the key
    key_file = test_dir / "temp_random.key"

    result = runner.invoke(main, ["generate-key", "--output", str(key_file)])

    assert result.exit_code == 0
    mock_generate_key_file.assert_called_once_with(key_file)
    mock_add_to_gitignore.assert_called_once_with(key_file.parent, key_file.name)

    # Cleanup
    if key_file.exists():
        key_file.unlink()


@patch("envcloak.cli.add_to_gitignore")
@patch("envcloak.cli.generate_key_file")
def test_generate_key_no_gitignore(
    mock_generate_key_file, mock_add_to_gitignore, runner, test_dir
):
    """
    Test the `generate-key` CLI command with the `--no-gitignore` flag.
    """
    key_file = test_dir / "temp_random.key"

    result = runner.invoke(
        main, ["generate-key", "--output", str(key_file), "--no-gitignore"]
    )

    assert result.exit_code == 0
    mock_generate_key_file.assert_called_once_with(key_file)
    mock_add_to_gitignore.assert_not_called()

    # Cleanup
    if key_file.exists():
        key_file.unlink()


@patch("envcloak.cli.add_to_gitignore")
@patch("envcloak.cli.generate_key_from_password_file")
def test_generate_key_from_password_with_gitignore(
    mock_generate_key_from_password_file, mock_add_to_gitignore, runner, mock_files
):
    """
    Test the `generate-key-from-password` CLI command with default behavior (adds to .gitignore).
    """
    _, _, _, key_file = mock_files
    temp_key_file = key_file.with_name("temp_password_key.key")  # Unique temp file
    password = "JustGiveItATry"
    salt = "e3a1c8b0d4f6e2c7a5b9d6f0c3e8f1a2"

    mock_generate_key_from_password_file.return_value = None

    result = runner.invoke(
        main,
        [
            "generate-key-from-password",
            "--password",
            password,
            "--salt",
            salt,
            "--output",
            str(temp_key_file),
        ],
    )

    assert result.exit_code == 0
    mock_generate_key_from_password_file.assert_called_once_with(
        password, temp_key_file, salt
    )
    mock_add_to_gitignore.assert_called_once_with(
        temp_key_file.parent, temp_key_file.name
    )

    # Cleanup
    if temp_key_file.exists():
        temp_key_file.unlink()


@patch("envcloak.cli.add_to_gitignore")
@patch("envcloak.cli.generate_key_from_password_file")
def test_generate_key_from_password_no_gitignore(
    mock_generate_key_from_password_file, mock_add_to_gitignore, runner, mock_files
):
    """
    Test the `generate-key-from-password` CLI command with the `--no-gitignore` flag.
    """
    _, _, _, key_file = mock_files
    temp_key_file = key_file.with_name("temp_password_key.key")  # Unique temp file
    password = "JustGiveItATry"
    salt = "e3a1c8b0d4f6e2c7a5b9d6f0c3e8f1a2"

    result = runner.invoke(
        main,
        [
            "generate-key-from-password",
            "--password",
            password,
            "--salt",
            salt,
            "--output",
            str(temp_key_file),
            "--no-gitignore",
        ],
    )

    assert result.exit_code == 0
    mock_generate_key_from_password_file.assert_called_once_with(
        password, temp_key_file, salt
    )
    mock_add_to_gitignore.assert_not_called()

    # Cleanup
    if temp_key_file.exists():
        temp_key_file.unlink()


@patch("envcloak.cli.decrypt_file")
@patch("envcloak.cli.encrypt_file")
def test_rotate_keys(mock_encrypt_file, mock_decrypt_file, runner, isolated_mock_files):
    """
    Test the `rotate-keys` CLI command.
    """
    encrypted_file = isolated_mock_files / "variables.env.enc"
    temp_decrypted_file = isolated_mock_files / "temp_variables.decrypted"
    key_file = isolated_mock_files / "mykey.key"
    temp_new_key_file = key_file.with_name("temp_newkey.key")
    temp_new_key_file.write_bytes(os.urandom(32))

    tmp_file = str(temp_decrypted_file) + ".tmp"

    def mock_decrypt(input_path, output_path, key):
        assert os.path.exists(input_path), "Encrypted file does not exist"
        with open(output_path, "w") as f:
            f.write("Decrypted content")

    def mock_encrypt(input_path, output_path, key):
        assert os.path.exists(input_path), "Decrypted file does not exist"
        with open(output_path, "w") as f:
            f.write(json.dumps({"ciphertext": "re-encrypted_data"}))

    mock_decrypt_file.side_effect = mock_decrypt
    mock_encrypt_file.side_effect = mock_encrypt

    result = runner.invoke(
        main,
        [
            "rotate-keys",
            "--input",
            str(encrypted_file),
            "--old-key-file",
            str(key_file),
            "--new-key-file",
            str(temp_new_key_file),
            "--output",
            str(temp_decrypted_file),
        ],
    )

    assert result.exit_code == 0
    assert "Keys rotated" in result.output
    mock_decrypt_file.assert_called_once_with(
        str(encrypted_file), tmp_file, key_file.read_bytes()
    )
    mock_encrypt_file.assert_called_once_with(
        tmp_file, str(temp_decrypted_file), temp_new_key_file.read_bytes()
    )

    assert not os.path.exists(tmp_file), f"Temporary file {tmp_file} was not deleted"

    # Cleanup
    if temp_decrypted_file.exists():
        temp_decrypted_file.unlink()
    if temp_new_key_file.exists():
        temp_new_key_file.unlink()


def test_encrypt_with_mixed_input_and_directory(runner, mock_files):
    """
    Test the `encrypt` CLI command with mixed `--input` and `--directory` usage.
    """
    input_file, _, _, key_file = mock_files
    directory = "mock_directory"
    output_path = "output_directory"

    result = runner.invoke(
        main,
        [
            "encrypt",
            "--input",
            str(input_file),
            "--directory",
            directory,
            "--output",
            output_path,
            "--key-file",
            str(key_file),
        ],
    )

    assert result.exit_code != 0
    assert "You must provide either --input or --directory, not both." in result.output


def test_decrypt_with_mixed_input_and_directory(runner, mock_files):
    """
    Test the `decrypt` CLI command with mixed `--input` and `--directory` usage.
    """
    _, encrypted_file, _, key_file = mock_files
    directory = "mock_directory"
    output_path = "output_directory"

    result = runner.invoke(
        main,
        [
            "decrypt",
            "--input",
            str(encrypted_file),
            "--directory",
            directory,
            "--output",
            output_path,
            "--key-file",
            str(key_file),
        ],
    )

    assert result.exit_code != 0
    assert "You must provide either --input or --directory, not both." in result.output


@patch("envcloak.cli.encrypt_file")
def test_encrypt_with_force(mock_encrypt_file, runner, isolated_mock_files):
    """
    Test the `encrypt` CLI command with the `--force` flag.
    """
    input_file = isolated_mock_files / "variables.env"
    existing_encrypted_file = (
        isolated_mock_files / "variables.temp.enc"
    )  # Existing file
    key_file = isolated_mock_files / "mykey.key"

    # Create a mock existing encrypted file
    existing_encrypted_file.write_text("existing content")

    def mock_encrypt(input_path, output_path, key):
        assert os.path.exists(input_path), "Input file does not exist"
        with open(output_path, "w") as f:
            f.write(json.dumps({"ciphertext": "encrypted_data"}))

    mock_encrypt_file.side_effect = mock_encrypt

    # Invoke with --force
    result = runner.invoke(
        main,
        [
            "encrypt",
            "--input",
            str(input_file),
            "--output",
            str(existing_encrypted_file),
            "--key-file",
            str(key_file),
            "--force",
        ],
    )

    assert result.exit_code == 0
    assert "Overwriting existing file" in result.output
    mock_encrypt_file.assert_called_once_with(
        str(input_file), str(existing_encrypted_file), key_file.read_bytes()
    )

    # Ensure the file was overwritten
    with open(existing_encrypted_file, "r") as f:
        assert json.load(f)["ciphertext"] == "encrypted_data"


@patch("envcloak.cli.decrypt_file")
def test_decrypt_with_force(mock_decrypt_file, runner, mock_files):
    """
    Test the `decrypt` CLI command with the `--force` flag.
    """
    _, encrypted_file, decrypted_file, key_file = mock_files

    # Create a mock existing decrypted file
    decrypted_file.write_text("existing content")

    def mock_decrypt(input_path, output_path, key):
        assert os.path.exists(input_path), "Encrypted file does not exist"
        with open(output_path, "w") as f:
            f.write("DB_USERNAME=example_user\nDB_PASSWORD=example_pass")

    mock_decrypt_file.side_effect = mock_decrypt

    # Invoke with --force
    result = runner.invoke(
        main,
        [
            "decrypt",
            "--input",
            str(encrypted_file),
            "--output",
            str(decrypted_file),
            "--key-file",
            str(key_file),
            "--force",
        ],
    )

    assert result.exit_code == 0
    assert "Overwriting existing file" in result.output
    mock_decrypt_file.assert_called_once_with(
        str(encrypted_file), str(decrypted_file), key_file.read_bytes()
    )

    # Ensure the file was overwritten
    with open(decrypted_file, "r") as f:
        assert f.read() == "DB_USERNAME=example_user\nDB_PASSWORD=example_pass"


def test_encrypt_without_force_conflict(runner, isolated_mock_files):
    """
    Test the `encrypt` CLI command without the `--force` flag when a conflict exists.
    """
    input_file = isolated_mock_files / "variables.env"
    existing_encrypted_file = isolated_mock_files / "variables.temp.enc"
    key_file = isolated_mock_files / "mykey.key"

    # Create a mock existing encrypted file
    existing_encrypted_file.write_text("existing content")

    # Invoke without --force
    result = runner.invoke(
        main,
        [
            "encrypt",
            "--input",
            str(input_file),
            "--output",
            str(existing_encrypted_file),
            "--key-file",
            str(key_file),
        ],
    )

    assert "already exists" in result.output


def test_decrypt_without_force_conflict(runner, mock_files):
    """
    Test the `decrypt` CLI command without the `--force` flag when a conflict exists.
    """
    _, encrypted_file, decrypted_file, key_file = mock_files

    # Create a mock existing decrypted file
    decrypted_file.write_text("existing content")

    # Invoke without --force
    result = runner.invoke(
        main,
        [
            "decrypt",
            "--input",
            str(encrypted_file),
            "--output",
            str(decrypted_file),
            "--key-file",
            str(key_file),
        ],
    )

    assert "already exists" in result.output


@patch("envcloak.cli.encrypt_file")
def test_encrypt_with_force_directory(mock_encrypt_file, runner, isolated_mock_files):
    """
    Test the `encrypt` CLI command with the `--force` flag for a directory.
    """
    directory = isolated_mock_files / "mock_directory"
    output_directory = isolated_mock_files / "output_directory"
    key_file = isolated_mock_files / "mykey.key"

    # Create mock files in the directory
    directory.mkdir()
    (directory / "file1.env").write_text("content1")
    (directory / "file2.env").write_text("content2")

    # Create a mock existing output directory
    output_directory.mkdir()
    (output_directory / "file1.env.enc").write_text("existing encrypted content")

    def mock_encrypt(input_path, output_path, key):
        with open(output_path, "w") as f:
            f.write(json.dumps({"ciphertext": "encrypted_data"}))

    mock_encrypt_file.side_effect = mock_encrypt

    # Invoke with --force
    result = runner.invoke(
        main,
        [
            "encrypt",
            "--directory",
            str(directory),
            "--output",
            str(output_directory),
            "--key-file",
            str(key_file),
            "--force",
        ],
    )

    assert "Overwriting existing file" in result.output
    mock_encrypt_file.assert_any_call(
        str(directory / "file1.env"),
        str(output_directory / "file1.env.enc"),
        key_file.read_bytes(),
    )
    mock_encrypt_file.assert_any_call(
        str(directory / "file2.env"),
        str(output_directory / "file2.env.enc"),
        key_file.read_bytes(),
    )


@patch("envcloak.cli.decrypt_file")
def test_decrypt_with_force_directory(mock_decrypt_file, runner, isolated_mock_files):
    """
    Test the `decrypt` CLI command with the `--force` flag for a directory.
    """
    directory = isolated_mock_files / "mock_directory"
    output_directory = isolated_mock_files / "output_directory"
    key_file = isolated_mock_files / "mykey.key"

    # Create mock encrypted files in the directory
    directory.mkdir()
    (directory / "file1.env.enc").write_text("encrypted content1")
    (directory / "file2.env.enc").write_text("encrypted content2")

    # Create a mock existing output directory
    output_directory.mkdir()
    (output_directory / "file1.env").write_text("existing decrypted content")

    def mock_decrypt(input_path, output_path, key):
        with open(output_path, "w") as f:
            f.write("decrypted content")

    mock_decrypt_file.side_effect = mock_decrypt

    # Invoke with --force
    result = runner.invoke(
        main,
        [
            "decrypt",
            "--directory",
            str(directory),
            "--output",
            str(output_directory),
            "--key-file",
            str(key_file),
            "--force",
        ],
    )

    assert "Overwriting existing file" in result.output
    mock_decrypt_file.assert_any_call(
        str(directory / "file1.env.enc"),
        str(output_directory / "file1.env"),
        key_file.read_bytes(),
    )
    mock_decrypt_file.assert_any_call(
        str(directory / "file2.env.enc"),
        str(output_directory / "file2.env"),
        key_file.read_bytes(),
    )
