# test_openai.py
import os
import traceback
from openai import OpenAI
from dotenv import load_dotenv

print("--- 正在載入 .env 檔案 ---")
load_dotenv()
print("--- .env 檔案載入完畢 ---")

# 檢查 API Key 是否被成功讀取
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("\n錯誤：在 .env 檔案中找不到 OPENAI_API_KEY。")
else:
    print(f"--- 成功讀取到 API Key (開頭為: {api_key[:5]}...) ---")

try:
    print("--- 正在初始化 OpenAI client ---")
    client = OpenAI()
    print("--- Client 初始化成功 ---")

    print("--- 準備發送一個最簡單的 API 請求 ---")
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! In one word, what is the color of the sky?"}
      ]
    )
    print("--- API 請求成功！ ---")
    print("\n[成功的回應]:")
    print(completion.choices[0].message.content)

except Exception as e:
    print("\n!!!!!!!!!! 獨立測試過程中發生錯誤 !!!!!!!!!!")
    print(f"錯誤類型 (Error Type): {type(e)}")
    print(f"錯誤訊息 (Error Message): {e}")
    print("\n--- 詳細錯誤追蹤 (Traceback) ---")
    traceback.print_exc()
    print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")