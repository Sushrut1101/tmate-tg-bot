# 🧵 Tmate Telegram Bot

A minimal Telegram bot to manage [tmate](https://tmate.io/) sessions via chat commands.

---

## ✨ Features

- Create disposable SSH + Web sessions  
- View & share session URLs via `/show`  
- Kill sessions manually or all at once  
- Access restricted via `AUTHORIZED_USERS`  
- Lightweight, single-file `.env` config  
- Fully async, zero-zombie subprocess handling

---

## 💬 Commands

| Command              | Description                                |
|----------------------|--------------------------------------------|
| `/start`             | Show welcome message                       |
| `/help`              | Show command list and usage info           |
| `/new`               | Spawn new tmate session                    |
| `/list`              | List all active sessions                   |
| `/show <id>`         | Display SSH + Web URLs for a session       |
| `/kill <id>`         | Terminate a specific session               |
| `/killall`           | Kill all active sessions                   |

Unauthorized users will see `⛔ You are not allowed to use this bot!`.

---

## ⚙️ Configuration

Create a `.env` file in the project root:

```.env
BOT_TOKEN=your_telegram_bot_token
AUTHORIZED_USERS=12345678,987654321  # Telegram user IDs (comma-separated)
```

Alternatively, export them before launching:

```bash
export BOT_TOKEN=your_telegram_bot_token
export AUTHORIZED_USERS=12345678,987654321
```

---

## 🚀 Run

Use [`uv`](https://github.com/astral-sh/uv) for fast dependency resolution:

```bash
uvx -n .
```
