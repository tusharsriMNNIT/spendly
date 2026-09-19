---
name: run-app
description: Start the Spendly Flask dev server and check it comes up cleanly. Use when asked to run, start, or verify the app works.
---

This project has no Makefile or run script — start it directly:

```
python app.py
```

- Runs on **port 5001** (not the Flask default 5000), with `debug=True`.
- If a virtualenv exists (`venv/`), activate it first: `source venv/bin/activate`.
- If dependencies aren't installed yet: `pip install -r requirements.txt`.
- After starting, curl `http://localhost:5001/` (or the relevant route) to confirm it responds before reporting success. Stop the server afterward rather than leaving it running in the background unless the user asked to keep it up.
