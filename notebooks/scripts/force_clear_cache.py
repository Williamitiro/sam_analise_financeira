import os
import shutil

def clear_pycache(root_dir):
    print(f"🧹 Clearing pycache in {root_dir}...")
    count = 0
    for root, dirs, files in os.walk(root_dir):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d))
                print(f"   Deleted {os.path.join(root, d)}")
                count += 1
        for f in files:
            if f.endswith(".pyc"):
                os.remove(os.path.join(root, f))
                print(f"   Deleted {os.path.join(root, f)}")
                count += 1
    print(f"✅ Cleared {count} cache items.")

if __name__ == "__main__":
    clear_pycache(os.path.dirname(os.path.abspath(__file__)))
