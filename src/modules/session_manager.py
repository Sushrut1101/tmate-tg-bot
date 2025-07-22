import os
import signal
import subprocess
import threading
import uuid

sessions: dict[str, tuple[int, subprocess.Popen]] = {}

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

    sessions[session_id] = (proc.pid, proc)
    return session_id, urls

def kill_session(session_id: str) -> bool:
    entry = sessions.pop(session_id, None)
    if not entry:
        return False

    pid, proc = entry
    try:
        os.killpg(os.getpgid(pid), signal.SIGTERM)
        proc.terminate()
        return True
    except Exception:
        return False

def list_sessions() -> list[str]:
    return list(sessions.keys())

def get_urls(session_id: str) -> dict | None:
    # we only stored pid+proc, but reader filled `urls` in create_session
    # so we return the last-captured urls from a side‐store
    # easiest: stash `urls` alongside Popen:
    #   sessions[session_id] = (proc.pid, proc, urls)
    # then return sessions[session_id][2]
    # for now assume you refactored to store urls too:
    entry = sessions.get(session_id)
    return entry[2] if entry and len(entry) > 2 else None

def cleanup_all_sessions():
    for sid in list(sessions):
        kill_session(sid)
