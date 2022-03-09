import os
import git
import json
import wget
import shutil
import tempfile
from pathlib import Path


def clone():
    temp_dir = tempfile.mkdtemp()
    git.Repo.clone_from(os.getenv("REPO"), temp_dir, branch=os.getenv("BRANCH"), depth=1)
    shutil.move(os.path.join(temp_dir, os.path.join(os.getenv("ASSETS_DIR"), os.getenv("ASSETS_FILE"))), '/tmp')
    shutil.rmtree(temp_dir)


def parse_json():
    list_of_urls = list()
    with open(os.path.join("/tmp", os.getenv("ASSETS_FILE"))) as assets:
        json_data = json.load(assets)
        data = json_data.get("data")
        if not (data is None):
            if type(data) is list:
                for asset in data:
                    url = asset.get("url")
                    if not (url is None):
                        list_of_urls.append(url)
                    else:
                        raise RuntimeWarning("Expected key url, but not found")
            else:
                raise TypeError("Expected list. Obtained %s" % type(json_data.get("data")))
        else:
            raise KeyError("Missing data key")
    return list_of_urls


def download(urls):
    for url in urls:
        file_name = url[url.rindex('/')+1:]
        file_path = Path(os.path.join("/tmp", file_name))
        if not file_path.is_file():
            wget.download(url, "/tmp")


def main():
    # clone()
    urls = parse_json()
    download(urls)


if __name__ == "__main__":
    main()
