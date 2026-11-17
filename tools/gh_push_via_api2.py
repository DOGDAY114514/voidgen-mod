import base64
import json
import os
import subprocess
import sys

REPO = "DOGDAY114514/voidgen-mod"
ROOT = r"D:\AI\voidgen-mod"
GH = r"D:\AI\tools\gh-cli\bin\gh.exe"
LOCAL = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
env = dict(os.environ, GH_CONFIG_DIR=r"D:\AI\tools\gh-config", GH_REPO=REPO)
TMP = os.path.join(ROOT, "build", "ghapi")
os.makedirs(TMP, exist_ok=True)


def gh(args, payload=None, jq=None):
    cmd = [GH] + args
    if payload is not None:
        p = os.path.join(TMP, "payload.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(payload, f)
        cmd += ["--input", p]
    if jq:
        cmd += ["--jq", jq]
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if r.returncode != 0:
        print("GH FAIL:", " ".join(args), r.stderr[:500])
        sys.exit(1)
    return r.stdout.strip()


main_sha = gh(["api", f"repos/{REPO}/commits/main", "--jq", ".sha"])
base_tree = gh(["api", f"repos/{REPO}/commits/{main_sha}", "--jq", ".commit.tree.sha"])
print("remote main:", main_sha, "local:", LOCAL)
if main_sha == LOCAL:
    print("already pushed")
    sys.exit(0)

diff = subprocess.run(["git", "-C", ROOT, "diff", "--name-status", LOCAL + "^", LOCAL],
                      capture_output=True, text=True).stdout.strip().splitlines()
print("changed files:", len(diff))

entries = []
for line in diff:
    parts = line.split("\t")
    status, path = parts[0], parts[1]
    if status.startswith("D"):
        entries.append({"path": path, "mode": "100644", "type": "blob", "sha": None})
        print("del", path)
        continue
    full = os.path.join(ROOT, path.replace("/", os.sep))
    mode = subprocess.run(["git", "-C", ROOT, "ls-tree", LOCAL, "--", path],
                          capture_output=True, text=True).stdout.split(" ")[0].strip() or "100644"
    b64 = base64.b64encode(open(full, "rb").read()).decode()
    sha = gh(["api", f"repos/{REPO}/git/blobs", "--jq", ".sha"], payload={"content": b64, "encoding": "base64"})
    entries.append({"path": path, "mode": mode, "type": "blob", "sha": sha})
    print("add", path, sha[:10])

tree = gh(["api", f"repos/{REPO}/git/trees", "--jq", ".sha"],
          payload={"base_tree": base_tree, "tree": entries})
msg = subprocess.run(["git", "-C", ROOT, "log", "-1", "--pretty=%B", LOCAL],
                     capture_output=True, text=True).stdout.strip()
commit = gh(["api", f"repos/{REPO}/git/commits", "--jq", ".sha"],
            payload={"message": msg, "tree": tree, "parents": [main_sha],
                     "author": {"name": "DOGDAY114514", "email": "DOGDAY114514@users.noreply.github.com"},
                     "committer": {"name": "DOGDAY114514", "email": "DOGDAY114514@users.noreply.github.com"}})
gh(["api", "-X", "PATCH", f"repos/{REPO}/git/refs/heads/main", "--jq", ".object.sha"],
   payload={"sha": commit, "force": False})
new_main = gh(["api", f"repos/{REPO}/commits/main", "--jq", ".sha"])
print("new remote main:", new_main, "match:", new_main == commit)
