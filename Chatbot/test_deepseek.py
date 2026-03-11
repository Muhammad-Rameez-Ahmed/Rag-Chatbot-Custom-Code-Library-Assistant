# # test_openrouter.py
# from openai import OpenAI

# client = OpenAI(
#     api_key="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",
#     base_url="https://openrouter.ai/api/v1",
#     timeout=60
# )

# try:
#     response = client.chat.completions.create(
#         model="deepseek/deepseek-chat-v3-0324:free",
#         messages=[{"role": "user", "content": "Say hello"}]
#     )
#     print("SUCCESS:", response.choices[0].message.content)
# except Exception as e:
#     print(f"ERROR: {type(e).__name__}: {e}")

# from openai import OpenAI

# client = OpenAI(
#     api_key="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",  # nai key yahan
#     base_url="https://openrouter.ai/api/v1",
#     timeout=60
# )

# try:
#     response = client.chat.completions.create(
#         model="deepseek/deepseek-chat-v3-0324:free",
#         messages=[{"role": "user", "content": "Say hello"}]
#     )
#     print("SUCCESS:", response.choices[0].message.content)
# except Exception as e:
#     print(f"ERROR: {type(e).__name__}: {e}")



from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1",
    timeout=60
)

try:
    response = client.chat.completions.create(
         model="qwen/qwen3-coder:free",
        messages=[{"role": "user", "content": "Say hello"}]
    )
    print("SUCCESS:", response.choices[0].message.content)
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")   


# import requests

# response = requests.get(
#     "https://openrouter.ai/api/v1/models",
#     headers={"Authorization": "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"}
# )

# models = response.json()["data"]

# # Sirf free models print karo
# for m in models:
#     if ":free" in m["id"]:
#         print(m["id"])    