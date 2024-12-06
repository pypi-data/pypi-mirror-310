import shutil
import os

dist_dir = "dist"
if os.path.exists(dist_dir) and os.path.isdir(dist_dir):
    shutil.rmtree(dist_dir)
    print(f"Removed {dist_dir} directory")
else:
    print(f"{dist_dir} directory does not exist")
