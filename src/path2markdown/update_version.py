import os
from datetime import datetime

version_file = "src/path2markdown/version.py"

def update_version(new_version):
    release_date = datetime.now().strftime("%Y-%m-%d")
    with open(version_file, "w") as f:
        f.write(f'__version__ = "{new_version}"\n')
        f.write(f'__release_date__ = "{release_date}"\n')
    print(f"Updated version to {new_version} and release date to {release_date}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python update_version.py <new_version>")
        sys.exit(1)
    update_version(sys.argv[1])

