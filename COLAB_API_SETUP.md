# Connect the Streamlit app to the Google Colab model API

The local Streamlit frontend expects a FastAPI service started from the Colab notebook.

## Before starting the API
Run the notebook cells that load the models and define the inference function named analyze_call2(audio, engine). The function must return a dictionary containing at least transcript, sentiment, intent, and summary. Other result fields, such as language, risk_score, risk_level, ESCALATION_FLAG, and voice_emotion, are optional.

## Install API dependencies in Colab
Run this in a new Colab cell:

    !pip -q install fastapi uvicorn pyngrok python-multipart nest-asyncio

## Start the API
Use the FastAPI cell from your model notebook/setup. It must expose:
- GET /health — returns a small JSON status response.
- POST /analyze — accepts a multipart audio file, a form field named engine (whisper or wav2vec2), and an X-API-Key header.

The API should decode uploaded audio to mono 16 kHz float32 samples and call analyze_call2(audio, engine). Start the server on port 8000 and expose it through ngrok.

Generate a fresh random API key at runtime. Add your ngrok authtoken privately inside the Colab session; never commit the real token or API key to GitHub.

## Connect from Streamlit
1. Copy the API URL and API key printed by the running Colab cell.
2. Paste both into the CallSense AI sidebar.
3. Click Test Colab connection. A successful setup responds to GET /health.
4. Select Whisper for multilingual ASR or Wav2Vec2 for English ASR.
5. Open Analyze Call, upload a WAV/MP3/M4A/OGG recording, and click Analyze call.

## Start Streamlit locally (Windows PowerShell)
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    python -m streamlit run app.py

## Troubleshooting
- 404 on /health: the entered URL may point to a different app or an API cell that does not define the /health route. Check the current ngrok URL and restart the API cell.
- 401 on /analyze: the API key in Streamlit does not match the key printed by the current Colab runtime.
- 500 on /analyze: inspect the Colab output; model inference may have raised an exception or returned a value that cannot be converted to JSON.
- Connection refused or tunnel error: make sure the Colab runtime and FastAPI server cell are still running.

## Limitations and safety
- Colab sessions are temporary; the ngrok URL and API key can change after a runtime restart.
- Whisper is the multilingual ASR option in this setup; Wav2Vec2 is the English option.
- Model recognition quality depends on audio quality and the models loaded by the notebook.
- This public tunnel is for a demonstration only. Do not upload real or sensitive customer calls.
