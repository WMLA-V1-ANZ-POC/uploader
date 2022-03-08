import os
import git
import shutil
import tempfile


def main():
    temp_dir = tempfile.mkdtemp()
    git.Repo.clone_from(os.getenv("REPO"), temp_dir, branch=os.getenv("BRANCH"), depth=1)
    shutil.move(os.path.join(temp_dir, 'data/assets.json'), '.')
    shutil.rmtree(temp_dir)


if __name__ == "__main__":
    main()