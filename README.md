# Workstyle 16 — Streamlit

A lightweight MBTI-inspired technical workstyle assessment for engineers and scientists.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Add `app.py` and `requirements.txt`.
3. In Streamlit Community Cloud, create a new app from the repository.
4. Set the main file path to `app.py`.
5. Deploy.

No database, API key, or external service is required.

## Notes

- 30 scenario-based questions.
- Choice click immediately advances to the next question.
- Results are based on four continuous axes and nearest-prototype distance across 16 workstyle archetypes.
- This is not an official MBTI assessment or a clinical personality instrument.
