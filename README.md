# 📱 Mobile Usage Insight AI

A powerful AI-powered assistant that answers natural language questions about your future mobile usage patterns — specifically for **Instagram** and **WhatsApp** — using time series forecasting and LLMs. This project was built as part of an AI/ML internship at SourceFuse.

---

## 🚀 Features

- 📊 **Forecast-based insights** on mobile usage metrics (Usage Time, Notifications, Times Opened)
- 🤖 **LLM integration (LLaMA 3.1–8B Instruct)** via RunPod serverless vLLM
- 🧠 Smart query parsing to detect the app (Instagram/WhatsApp) and metric (usage, notifications, times opened)
- 🔍 Data-driven, context-aware answers from future trend summaries
- 🌐 **Streamlit UI** for an intuitive, interactive interface
- 📁 Easy-to-load JSON forecasts and modular backend

---


---

## 🧪 Forecasting Data

- Built from CSV forecasts for 6 categories:
  - `instagram_usage_forecast_filtered.json`
  - `instagram_notifications_forecast_filtered.json`
  - `instagram_times_opened_forecast_filtered.json`
  - `whatsapp_usage_forecast_filtered.json`
  - `whatsapp_notifications_forecast_filtered.json`
  - `whatsapp_times_opened_forecast_filtered.json`
- Only relevant fields retained: `date (ds)`, `trend`, and `predicted_value (yhat)`

---

## 🧠 Tech Stack

| Component        | Tool/Library                        |
|------------------|-------------------------------------|
| LLM              | Meta LLaMA 3.1–8B Instruct (via RunPod vLLM) |
| Time Series Data | Forecasts from Prophet              |
| Interface        | Streamlit                           |
| Integration API  | OpenAI-compatible API via RunPod    |
| Language         | Python                              |
| Environment      | dotenv (`.env`) for secrets         |

---

## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/mobile-usage-insight-ai.git
   cd mobile-usage-insight-ai
2. **Add your .env file**
   RUNPOD_TOKEN=your_runpod_token
   RUNPOD_CHATBOT_URL=https://api.runpod.ai/...
   MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct
3. **Run the Streamlit app**
   streamlit run week4.py


![image](https://github.com/user-attachments/assets/37aa3d83-49b4-423a-b5f1-52ded8902667)

