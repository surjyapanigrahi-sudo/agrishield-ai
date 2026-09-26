# Streamlit Community Cloud deployment

Deploy `app.py` from the `main` branch with Python **3.12**.

Streamlit Community Cloud does not change the Python version of an existing
deployment in place. If the app is currently on Python 3.14, delete and
redeploy it, open **Advanced settings**, and select Python 3.12 before clicking
**Deploy**. Keep `requirements.txt`, `best_v1.pt`, `best_v2.pt`, and `samples/`
in the repository root.

The `runtime.txt` file records the intended runtime for platforms that support
it; Community Cloud's Python selector is the authoritative setting.
