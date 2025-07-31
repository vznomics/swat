import os

def authenticate_user(username: str, password: str) -> bool:
    return (
        username == os.getenv("SWAT_ADMIN", "admin") and
        password == os.getenv("SWAT_PASSWORD", "changeme")
    )
