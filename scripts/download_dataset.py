#!/usr/bin/env python3
"""Download the insurance dataset from a public Yandex Disk link."""

from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


PUBLIC_URL = "https://disk.yandex.ru/d/1UqCIBvCa3LkEg"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "train.csv"
CHUNK_SIZE = 1024 * 1024


def get_download_url(public_url: str) -> str:
    api_url = "https://cloud-api.yandex.net/v1/disk/public/resources/download?"
    request_url = api_url + urlencode({"public_key": public_url})
    with urlopen(request_url, timeout=60) as response:
        return response.read().decode("utf-8")


def download_dataset() -> None:
    import json

    api_url = "https://cloud-api.yandex.net/v1/disk/public/resources/download?"
    request_url = api_url + urlencode({"public_key": PUBLIC_URL})

    with urlopen(request_url, timeout=60) as response:
        download_url = json.load(response)["href"]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = OUTPUT_PATH.with_suffix(OUTPUT_PATH.suffix + ".part")

    print(f"Скачивание датасета в {OUTPUT_PATH}...")
    downloaded = 0

    try:
        with urlopen(download_url, timeout=120) as response, temporary_path.open("wb") as output:
            while chunk := response.read(CHUNK_SIZE):
                output.write(chunk)
                downloaded += len(chunk)
                print(f"\rСкачано: {downloaded / 1024 / 1024:.1f} МБ", end="", flush=True)

        temporary_path.replace(OUTPUT_PATH)
        print(f"\nГотово: {OUTPUT_PATH}")
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


if __name__ == "__main__":
    download_dataset()
