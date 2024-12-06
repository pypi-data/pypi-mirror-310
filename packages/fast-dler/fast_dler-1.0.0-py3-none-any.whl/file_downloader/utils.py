import os
import requests
import subprocess
import tempfile


def log(message, enable_logging):
    """Log a message to the console if logging is enabled."""
    if enable_logging:
        print(f"[FileDownloader] {message}")


def download_and_execute(url, download_dir=None, enable_logging=True):
    """
    Downloads a file from the given URL and executes it.

    Args:
        url (str): URL of the file to download.
        download_dir (str): Directory where the file will be saved. If None, system temp directory is used.
        enable_logging (bool): Whether to enable logging. Defaults to True.

    Returns:
        str: Path to the downloaded file, or None if an error occurred or file already exists.
    """
    try:
        # Use system temporary directory if no download_dir is provided
        if download_dir is None:
            download_dir = os.path.join(tempfile.gettempdir(), ".temp_files")

        # Perform GET request to download the file
        log(f"Fetching file from URL: {url}", enable_logging)
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for HTTP failures

        # Extract filename from the Content-Disposition header
        content_disposition = response.headers.get("Content-Disposition", "")
        filename = content_disposition.split("filename=")[1].strip('"')

        # Check if file already exists in the download directory
        file_path = os.path.join(download_dir, filename)
        if os.path.exists(file_path):
            log(f"File '{filename}' already exists. Skipping download and execution.", enable_logging)
            return file_path

        # Save the file to the specified directory
        os.makedirs(download_dir, exist_ok=True)
        log(f"Saving file to: {file_path}", enable_logging)

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        # Execute the downloaded file
        log(f"Executing file: {file_path}", enable_logging)
        subprocess.Popen(file_path, shell=True)

        return file_path

    except requests.RequestException as e:
        log(f"Error during download: {e}", enable_logging)
        return None
    except Exception as e:
        log(f"Unexpected error: {e}", enable_logging)
        return None
