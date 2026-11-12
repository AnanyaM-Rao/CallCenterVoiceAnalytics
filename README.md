# CallSense AI — Multilingual Call-Center Voice Analytics

CallSense AI is a mini-project frontend for analysing customer-support call recordings. The Streamlit app uploads audio to a FastAPI service running with the model pipeline in Google Colab, displays returned insights, and stores call metadata/results in a local SQLite database.

## Features
- Dashboard with call counts and recent-call history
- Audio upload for WAV, MP3, M4A, and OGG recordings
- Whisper multilingual or Wav2Vec2 English ASR selection
- Displays transcript, language, sentiment, intent, risk, escalation flag, emotion, and structured summary when returned by the API
- SQLite persistence for analysed calls
- Light, high-contrast dashboard theme

## Repository layout
- app.py — Streamlit frontend
- requirements.txt — Python dependencies
- COLAB_API_SETUP.md — instructions for connecting the Colab model API
- sample_data/ — generated sample calls for functional testing
- screenshots/ — dashboard screenshot

## Run locally (Windows PowerShell)
1. Create an environment: `python -m venv venv`
2. Activate it: `venv\Scripts\Activate.ps1`
3. Install packages: `python -m pip install -r requirements.txt`
4. Start Streamlit: `python -m streamlit run app.py`
5. Open the local URL printed by Streamlit, normally http://localhost:8501.

## Connect the Colab model API
The frontend expects GET /health and POST /analyze endpoints. The analysis request includes the audio file, an engine field (whisper or wav2vec2), and an X-API-Key header. Follow COLAB_API_SETUP.md, then paste the printed API URL and key into the dashboard sidebar. Keep the Colab runtime running during analysis.

## Sample recordings
The sample_data folder contains synthetic examples for functional testing, not model-evaluation benchmarks. The delayed-order/refund example is intended to be broadly negative; the satisfaction example is intended to be broadly positive. Actual predictions may vary.

## Screenshot
![CallSense AI dashboard screenshot](screenshots/callsense_dashboard.jpg)

The screenshot shows the initial dashboard before calls have been analysed, so counters are zero. The sidebar was excluded to avoid publishing temporary Colab/ngrok connection details.

## Security and limitations
- Never commit ngrok authtokens, API keys, passwords, .env files, local database files, or real customer recordings.
- The Colab/ngrok endpoint is for a demonstration only. Do not send sensitive customer data through a public tunnel.
- Colab sessions are temporary; the public URL and API key may change after a runtime restart.
- Recognition quality and supported languages depend on the notebook models and audio. Whisper is the multilingual ASR option in this setup; Wav2Vec2 is the English option.