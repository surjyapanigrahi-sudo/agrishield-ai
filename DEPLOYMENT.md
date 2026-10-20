# Streamlit Community Cloud deployment

Deploy `app.py` from the `main` branch with Python **3.12**.

Streamlit Community Cloud does not change the Python version of an existing
deployment in place. If the app is currently on Python 3.14, delete and
redeploy it, open **Advanced settings**, and select Python 3.12 before clicking
**Deploy**. Keep `requirements.txt`, `best_v1.pt`, `best_v2.pt`, and `samples/`
in the repository root.

The `runtime.txt` file records the intended runtime for platforms that support
it; Community Cloud's Python selector is the authoritative setting.

## Community Cloud settings

- Repository: `surjyapanigrahi-sudo/agrishield-ai`
- Branch: `main`
- Entry point: `app.py`
- Python: `3.12`

The Streamlit app does not need an OpenAI API key. OpenAI credentials belong in
the n8n credential store used by the advisory workflow. The webhook endpoints
can be overridden with the `N8N_WEBHOOK_URL` and `N8N_FEEDBACK_WEBHOOK_URL`
environment variables. Never commit API keys or access tokens to this repository.

After each deployment, confirm in the Cloud logs that dependencies installed,
`best_v2.pt` loaded, and the app completed its first script run.
