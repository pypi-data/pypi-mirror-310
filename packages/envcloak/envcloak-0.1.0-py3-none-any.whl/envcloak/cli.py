import os
from pathlib import Path
import click
from envcloak.encryptor import encrypt_file, decrypt_file
from envcloak.generator import generate_key_file, generate_key_from_password_file
from envcloak.utils import add_to_gitignore


@click.group()
def main():
    """
    EnvCloak: Securely manage encrypted environment variables.
    """
    pass


@click.command()
@click.option(
    "--input", "-i", required=False, help="Path to the input file (e.g., .env)."
)
@click.option(
    "--directory",
    "-d",
    required=False,
    help="Path to the directory of files to encrypt.",
)
@click.option(
    "--output",
    "-o",
    required=True,
    help="Path to the output file or directory for encrypted files.",
)
@click.option(
    "--key-file", "-k", required=True, help="Path to the encryption key file."
)
def encrypt(input, directory, output, key_file):
    """
    Encrypt environment variables from a file or all files in a directory.
    """
    if not input and not directory:
        raise click.UsageError("You must provide either --input or --directory.")
    if input and directory:
        raise click.UsageError(
            "You must provide either --input or --directory, not both."
        )

    with open(key_file, "rb") as kf:
        key = kf.read()

    if input:
        # Encrypt a single file
        encrypt_file(input, output, key)
        click.echo(f"File {input} encrypted -> {output} using key {key_file}")
    elif directory:
        # Encrypt all files in the directory
        input_dir = Path(directory)
        output_dir = Path(output)

        if not input_dir.is_dir():
            raise click.UsageError(
                f"The specified directory does not exist: {directory}"
            )
        if not output_dir.exists():
            output_dir.mkdir(parents=True)

        for file in input_dir.iterdir():
            if file.is_file():  # Skip directories
                output_file = output_dir / (file.name + ".enc")
                encrypt_file(str(file), str(output_file), key)
                click.echo(
                    f"File {file} encrypted -> {output_file} using key {key_file}"
                )


@click.command()
@click.option(
    "--input",
    "-i",
    required=False,
    help="Path to the encrypted input file (e.g., .env.enc).",
)
@click.option(
    "--directory",
    "-d",
    required=False,
    help="Path to the directory of encrypted files.",
)
@click.option(
    "--output",
    "-o",
    required=True,
    help="Path to the output file or directory for decrypted files.",
)
@click.option(
    "--key-file", "-k", required=True, help="Path to the decryption key file."
)
def decrypt(input, directory, output, key_file):
    """
    Decrypt environment variables from a file or all files in a directory.
    """
    if not input and not directory:
        raise click.UsageError("You must provide either --input or --directory.")
    if input and directory:
        raise click.UsageError(
            "You must provide either --input or --directory, not both."
        )

    with open(key_file, "rb") as kf:
        key = kf.read()

    if input:
        # Decrypt a single file
        decrypt_file(input, output, key)
        click.echo(f"File {input} decrypted -> {output} using key {key_file}")
    elif directory:
        # Decrypt all files in the directory
        input_dir = Path(directory)
        output_dir = Path(output)

        if not input_dir.is_dir():
            raise click.UsageError(
                f"The specified directory does not exist: {directory}"
            )
        if not output_dir.exists():
            output_dir.mkdir(parents=True)

        for file in input_dir.iterdir():
            if file.is_file() and file.suffix == ".enc":  # Only decrypt .enc files
                output_file = output_dir / file.stem  # Remove .enc from filename
                decrypt_file(str(file), str(output_file), key)
                click.echo(
                    f"File {file} decrypted -> {output_file} using key {key_file}"
                )


@click.command()
@click.option(
    "--output", "-o", required=True, help="Path to save the generated encryption key."
)
@click.option(
    "--no-gitignore", is_flag=True, help="Skip adding the key file to .gitignore."
)
def generate_key(output, no_gitignore):
    """
    Generate a new encryption key.
    """
    output_path = Path(output)

    generate_key_file(output_path)
    if not no_gitignore:
        add_to_gitignore(output_path.parent, output_path.name)


@click.command()
@click.option(
    "--password", "-p", required=True, help="Password to derive the encryption key."
)
@click.option(
    "--salt", "-s", required=False, help="Salt for key derivation (16 bytes as hex)."
)
@click.option(
    "--output", "-o", required=True, help="Path to save the derived encryption key."
)
@click.option(
    "--no-gitignore", is_flag=True, help="Skip adding the key file to .gitignore."
)
def generate_key_from_password(password, output, salt, no_gitignore):
    """
    Derive an encryption key from a password and salt.
    """
    output_path = Path(output)

    generate_key_from_password_file(password, output_path, salt)
    if not no_gitignore:
        add_to_gitignore(output_path.parent, output_path.name)


@click.command()
@click.option(
    "--input", "-i", required=True, help="Path to the encrypted file to re-encrypt."
)
@click.option(
    "--old-key-file", "-ok", required=True, help="Path to the old encryption key."
)
@click.option(
    "--new-key-file", "-nk", required=True, help="Path to the new encryption key."
)
@click.option("--output", "-o", required=True, help="Path to the re-encrypted file.")
def rotate_keys(input, old_key_file, new_key_file, output):
    """
    Rotate encryption keys by re-encrypting a file with a new key.
    """
    with open(old_key_file, "rb") as okf:
        old_key = okf.read()
    with open(new_key_file, "rb") as nkf:
        new_key = nkf.read()
    # Decrypt with old key and re-encrypt with new key
    temp_decrypted = f"{output}.tmp"
    decrypt_file(input, temp_decrypted, old_key)
    encrypt_file(temp_decrypted, output, new_key)
    os.remove(temp_decrypted)  # Clean up temporary file
    click.echo(f"Keys rotated for {input} -> {output}")


# Add all commands to the main group
main.add_command(encrypt)
main.add_command(decrypt)
main.add_command(generate_key)
main.add_command(generate_key_from_password)
main.add_command(rotate_keys)


if __name__ == "__main__":
    main()
