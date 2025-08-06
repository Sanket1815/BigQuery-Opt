# import google.generativeai as genai

# # Replace with your API key
# GEMINI_API_KEY = "AIzaSyBz2gFcPofGXi-sSznRxvLbIiGO7swCKqk"  

# genai.configure(api_key=GEMINI_API_KEY)

# # List available models
# models = genai.list_models()
# for model in models:
#     print(model.name)  # e.g., 'models/gemini-1.5-pro'

# from google.cloud import bigquery
# client = bigquery.Client()
# query_job = client.query("SELECT 1")
# print("✅ Job created:", query_job.job_id)
# print("✅ Result:", list(query_job.result())[0])

from google.auth import default
creds, project = default()
print("✅ Using credentials from:", creds.service_account_email if hasattr(creds, 'service_account_email') else creds)
