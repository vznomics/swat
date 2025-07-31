import re
from pathlib import Path

SMB_CONF_PATH = Path("/etc/samba/smb.conf")

def list_shares():
    shares = []
    current = {}
    with SMB_CONF_PATH.open("r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            if current:
                shares.append(current)
                current = {}
            current["name"] = line[1:-1]
            current["read_users"] = []
            current["write_users"] = []
            current["readonly"] = False
        elif "=" in line:
            key, value = map(str.strip, line.split("=", 1))
            key = key.lower()
            if key == "path":
                current["path"] = value
            elif key == "read list":
                current["read_users"] = [u.strip() for u in value.split(",")]
            elif key == "write list":
                current["write_users"] = [u.strip() for u in value.split(",")]
            elif key == "read only":
                current["readonly"] = value.lower() in ("yes", "true")

    if current:
        shares.append(current)
    return [s for s in shares if s["name"] not in ("global", "")]

def add_share(name, path, readonly=False, read_users=None, write_users=None):
    read_users = read_users or []
    write_users = write_users or []
    block = f"""\n[{name}]
   path = {path}
   read only = {"yes" if readonly else "no"}
   read list = {", ".join(read_users)}
   write list = {", ".join(write_users)}\n"""
    with SMB_CONF_PATH.open("a") as f:
        f.write(block)

def remove_share(name):
    with SMB_CONF_PATH.open("r") as f:
        content = f.read()

    pattern = re.compile(rf"(?s)\n\[{re.escape(name)}\].*?(?=\n\[|\Z)")
    new_content = re.sub(pattern, "", content)

    with SMB_CONF_PATH.open("w") as f:
        f.write(new_content)

def update_share(original_name, new_name, new_path, read_users, write_users, readonly):
    remove_share(original_name)
    add_share(new_name, new_path, readonly, read_users, write_users)
