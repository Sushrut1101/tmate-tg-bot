from datetime import datetime

def ts() -> str:
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def info(user_id: int, command: str, response: str = ""):
    print(f"[{ts()}] [INFO] {user_id} - Used {command}")
    if response:
        for line in response.strip().splitlines():
            print(f"           {line}")

def deny(user_id: int, command: str):
    print(f"[{ts()}] [DENY] {user_id} - Unauthorized user tried {command}")
