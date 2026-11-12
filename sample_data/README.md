# CallSense Sample Audio Data

This folder contains generated English WAV recordings for testing the Multilingual Call-Center Voice Analytics System.

- `sample_negative_customer_call.wav`: simulated customer reporting a delayed order, expressing frustration, and requesting a refund. Expected broad sentiment: negative; likely intent: order status/refund.
- `sample_positive_customer_call.wav`: simulated customer expressing satisfaction with delivery, product, and support. Expected broad sentiment: positive.

These are synthetic text-to-speech examples, not real customer recordings. Model outputs may vary. Use them for functional testing only; do not treat them as evaluation benchmarks.

## Usage

In the Streamlit app, open **Analyse Call**, upload one WAV file, select the speech-recognition engine, and run analysis. Ensure the Colab API is running and the dashboard's API URL and key are configured.
