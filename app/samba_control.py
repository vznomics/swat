import os

SMB_CONF_PATH = "/etc/samba/smb.conf"

def list_shares():
    shares = []
    with open(SMB_CONF_PATH, "r") as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith("[") and line.endswith("]\n"):
            shares.append(line.strip("[]\n"))
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
