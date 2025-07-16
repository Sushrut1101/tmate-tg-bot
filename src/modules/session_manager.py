import subprocess
import uuid

sessions = {}

def create_session():
    session_id = str(uuid.uuid4())[:8]
    proc = subprocess.Popen(['tmate', '-F'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ssh_url = None

    while True:
        output = proc.stdout.readline().decode()
        if "ssh" in output:
            ssh_url = output.strip()
            break

    sessions[session_id] = (proc.pid, ssh_url)
    return session_id, ssh_url

def list_sessions():
    return sessions

def kill_session(session_id):
    if session_id in sessions:
        pid, _ = sessions.pop(session_id)
        subprocess.Popen(['kill', str(pid)])
        return True
    return False

def get_ssh_url(session_id):
    return sessions.get(session_id, (None, None))[1]
