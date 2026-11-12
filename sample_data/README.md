# CallSense Sample Audio Data

This folder contains generated English MP3 recordings for functional testing of the Multilingual Call-Center Voice Analytics System.

- `sample_negative_customer_call.mp3`: a short synthetic customer message about a late order, dissatisfaction, and a refund request. Expected broad sentiment: negative; likely intent: order status/refund.
- `sample_positive_customer_call.mp3`: a short synthetic customer message expressing happiness with an order and service. Expected broad sentiment: positive.

These are computer-generated text-to-speech examples, not real customer recordings. Model outputs may vary. Use them for functional testing only; do not treat them as evaluation benchmarks.

## Usage

In the Streamlit app, open **Analyse Call**, upload one MP3 file, select the speech-recognition engine, and run analysis. Ensure the Colab API is running and the dashboard's API URL and key are configured.
