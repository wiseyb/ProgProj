import os, shutil, ssl, subprocess, sys, tempfile, urllib.error, urllib.request, zipfile
from pathlib import Path, PurePosixPath


ARCHIVE_URL = "https://github.com/wiseyb/ProgProj/archive/refs/heads/main.zip"
PROTECTED_DIRS = {".git", ".github", "__pycache__", ".venv"}
DEV_MODE = True


def is_protected(path):
    return any(part.casefold() in PROTECTED_DIRS for part in path.parts)


def download_archive(destination):
    try:
        with urllib.request.urlopen(ARCHIVE_URL, timeout=60) as response:
            with open(destination, "wb") as archive_file:
                shutil.copyfileobj(response, archive_file)
    except urllib.error.URLError as error:
        if not isinstance(error.reason, ssl.SSLCertVerificationError):
            raise
        curl = shutil.which("curl.exe")
        if curl is None:
            raise
        print("Python certificate verification failed; retrying with Windows curl.")
        result = subprocess.run(
            [
                curl,
                "--fail",
                "--location",
                "--silent",
                "--show-error",
                "--ssl-no-revoke",
                "--output",
                str(destination),
                ARCHIVE_URL,
            ],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if result.returncode:
            raise urllib.error.URLError(
                result.stderr.strip() or f"curl exited with code {result.returncode}"
            ) from error


def sync_project(archive_path, destination):
    destination = Path(destination).resolve()
    running_installer = Path(__file__).resolve()
    updated = 0

    with zipfile.ZipFile(archive_path) as archive:
        members = [info for info in archive.infolist() if not info.is_dir()]
        roots = {PurePosixPath(info.filename).parts[0] for info in members}
        if len(roots) != 1:
            raise ValueError("Downloaded archive does not have one project root.")
        project_root = roots.pop()

        for info in members:
            member_path = PurePosixPath(info.filename)
            parts = member_path.parts
            if (
                len(parts) < 2
                or parts[0] != project_root
                or member_path.is_absolute()
                or "\\" in info.filename
                or ".." in parts
                or any(part.endswith(":") for part in parts)
                or is_protected(Path(*parts[1:]))
            ):
                continue

            relative_path = Path(*parts[1:])
            target = destination / relative_path
            if target.resolve() == running_installer:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)

            if target.is_file() and target.stat().st_size == info.file_size:
                with archive.open(info) as incoming, target.open("rb") as current:
                    if all(
                        new_chunk == old_chunk
                        for new_chunk, old_chunk in zip(
                            iter(lambda: incoming.read(1024 * 1024), b""),
                            iter(lambda: current.read(1024 * 1024), b""),
                        )
                    ):
                        continue

            temporary_path = None
            try:
                with archive.open(info) as incoming, tempfile.NamedTemporaryFile(
                    dir=target.parent, delete=False
                ) as temporary:
                    temporary_path = Path(temporary.name)
                    shutil.copyfileobj(incoming, temporary)
                os.replace(temporary_path, target)
            finally:
                if temporary_path is not None:
                    temporary_path.unlink(missing_ok=True)

            updated += 1
            print(f"Updated: {relative_path}")

    print(f"Sync complete. Updated {updated} file(s); local-only files were kept.")


def main():
    destination = Path(__file__).resolve().parent
    if DEV_MODE:
        print("DEV MODE enabled. Skipping project update.")
    else:
        with tempfile.TemporaryDirectory(prefix="progproj-installer-") as temp_dir:
            archive_path = Path(temp_dir) / "project.zip"
            print("Downloading project...")
            download_archive(archive_path)
            print(f"Syncing project into {destination}...")
            sync_project(archive_path, destination)

    app_path = destination / "app.py"
    if not app_path.is_file():
        raise FileNotFoundError(f"Application entry point not found: {app_path}")
    print(f"Launching {app_path.name}...")
    return subprocess.run(
        [sys.executable, str(app_path)], cwd=destination, check=False
    ).returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, urllib.error.URLError, zipfile.BadZipFile, ValueError) as error:
        print(f"Launcher failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
