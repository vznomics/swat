
import os

SMB_CONF_PATH = "/etc/samba/smb.conf"

def parse_bool(value: str) -> bool:
    return value.strip().lower() in ("yes", "true", "1")

def list_shares():
    shares = []
    current_share = None

    with open(SMB_CONF_PATH, "r") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith(";") or line.startswith("#"):
                continue

            if line.startswith("[") and line.endswith("]"):
                if current_share:
                    shares.append(current_share)
                share_name = line.strip("[]")
                current_share = {
                    "name": share_name,
                    "path": "",
                    "readonly": False,
                    "read_users": [],
                    "write_users": []
                }
            elif current_share and "=" in line:
                key, value = line.split("=", 1)
                key = key.strip().lower()
                value = value.strip()

                if key == "path":
                    current_share["path"] = value
                elif key == "read only":
                    current_share["readonly"] = parse_bool(value)
                elif key == "read list":
                    current_share["read_users"] = [u.strip() for u in value.split(",")]
                elif key == "write list":
                    current_share["write_users"] = [u.strip() for u in value.split(",")]

    if current_share:
        shares.append(current_share)

    return shares

def add_share(name: str, path: str, readonly: bool = False):
    config = f"""
[{name}]
   path = {path}
   browseable = yes
   read only = {"yes" if readonly else "no"}
   guest ok = yes
"""
    with open(SMB_CONF_PATH, "a") as f:
        f.write(config)
    os.system("smbcontrol all reload-config")

def remove_share(name: str):
    with open(SMB_CONF_PATH, "r") as f:
        lines = f.readlines()
    new_lines = []
    skip = False
    for line in lines:
        if line.strip() == f"[{name}]":
            skip = True
        elif skip and line.startswith("["):
            skip = False
        if not skip:
            new_lines.append(line)
    with open(SMB_CONF_PATH, "w") as f:
        f.writelines(new_lines)
    os.system("smbcontrol all reload-config")
