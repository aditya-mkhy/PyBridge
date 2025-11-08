# PyBridge

A small Python tool to simplify uploading and downloading files between your local machine and a PythonAnywhere webapp.  
Lightweight, scriptable, and built for automating deploy / file-management tasks.

> Simple, no-frills utility to manage files on PythonAnywhere from local scripts.

---

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

- Upload a local project or folder to a PythonAnywhere user webapp.
- Download files or the full site structure from PythonAnywhere to local disk.
- Enable / disable / reload a webapp via PythonAnywhere API.
- Simple local JSON-backed DB for tracking metadata.
- Minimal dependencies — uses `requests` and standard library.

---

## Project structure (important files)

```
PyBridge/
├─ data.db         # local DB file used by the tool
├─ db.py           # small JSON-backed DB helper
├─ pybridge.py     # main API client and utility functions
├─ util.py         # tiny logging helper
├─ README.md       # (this file)
├─ LICENSE         # MIT license
```

---

## Requirements

- Python 3.9 or newer  
- `requests` library

---

## Quick start — example usage

### 1) Import and initialize
```python
from pybridge import PyBridge

# Use your PythonAnywhere username and API token
username = "your-username"
token = "your_api_token_here"
pb = PyBridge(username=username, token=token)
```

### 2) Upload a folder or project
```python
project_path = "/path/to/your/project/"   # note trailing slash for directories
pb.upload(project_path)
```

### 3) Download files from the remote webapp
```python
save_path = "/path/to/save/remote/files/"
pb.download(save_path)
```

### 4) Manage the webapp
```python
pb.reload()   # reload the webapp
pb.enable()   # enable the webapp
pb.disable()  # disable the webapp
```

> The API client builds requests to the PythonAnywhere API endpoints. Make sure your username and token are valid and have the permissions required for the operations you call.

---

## Security & best practices

- **Keep your API token secret.** Do not hardcode tokens in public repositories.
- Run the tool only against accounts/webapps you control or trust.
- This tool writes files to disk when downloading from the remote — review remote contents before executing in a production environment.
- For CI or automation, use environment variables or a secure secret manager for the token.

---

## Troubleshooting

- `requests` errors / network problems: ensure internet access and that the token/username are correct.
- `Permission` or `401/403` responses: check your API token permissions on PythonAnywhere.
- Slow transfers: try wired connection or ensure remote files are not extremely large.
- If uploads appear to fail silently, run scripts from a terminal to see printed logs (util.log prints basic INFO messages).

---

## Development

- `db.py` contains simple helpers for reading/writing local DB (`data.db`).
- `util.py` contains a tiny `log()` function — you can replace it with a logger if desired.
- To extend: add CLI wrappers or click/argparse entry points for command-line usage.

---

## License

MIT License — see the `LICENSE` file.

---

## Credits

Developed as a compact helper to manage PythonAnywhere-hosted projects and files.
