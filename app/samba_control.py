
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
