import os
import signal
import subprocess
import threading
import uuid

sessions: dict[str, tuple[int, subprocess.Popen, dict]] = {}

def create_session() -> tuple[str, dict]:
    session_id = str(uuid.uuid4())[:8]
    proc = subprocess.Popen(
        ["tmate", "-F"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid,
        text=True,
    )

    urls = {
        "ssh_ro": None,
        "ssh_rw": None,
        "web_ro": None,
        "web_rw": None,
    }

    def reader():
        for raw in proc.stdout:
            line = raw.strip()
            low = line.lower()
            # read-only SSH
            if low.startswith("ssh session read only:"):
                urls["ssh_ro"] = line.split(":", 1)[1].strip()
            # read-write SSH
            elif low.startswith("ssh session:"):
                urls["ssh_rw"] = line.split(":", 1)[1].strip()
            # read-only Web
            elif low.startswith("web session read only:"):
                urls["web_ro"] = line.split(":", 1)[1].strip()
            # read-write Web
            elif low.startswith("web session:"):
                urls["web_rw"] = line.split(":", 1)[1].strip()

            # stop if we've got them all
            if all(urls.values()):
                break

    # spawn reader thread, wait up to 10s
    t = threading.Thread(target=reader, daemon=True)
    t.start()
    t.join(timeout=10)

    sessions[session_id] = (proc.pid, proc, urls)
    return session_id, urls

def kill_session(session_id: str) -> bool:
    entry = sessions.pop(session_id, None)
    if not entry:
        return False

    pid, proc, _ = entry
    try:
        os.killpg(os.getpgid(pid), signal.SIGTERM)
        proc.terminate()
        proc.wait(timeout=5)
        return True
    except Exception:
        return False

def list_sessions() -> list[str]:
    return list(sessions.keys())

def get_urls(session_id: str) -> dict | None:
    entry = sessions.get(session_id)
    return entry[2] if entry else None

def cleanup_all_sessions():
    for sid in list(sessions):
        kill_session(sid)
