import os
import json # 雖然這次沒直接用到 loads，但保留著是好習慣
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from flask_cors import CORS

# 載入 .env 檔案中的環境變數
load_dotenv()

app = Flask(__name__)
# 設定 CORS，允許所有來源的請求
CORS(app)

# 初始化 OpenAI Client
client = OpenAI()
# --- 最終解決方案：使用「描述式指令」繞過 Bug ---
PROMPT_TEMPLATE = """
You are an expert-level JSON generator acting as a witty screenwriter.
Your task is to perform two actions based on the user's input, and then structure the entire output into a single, valid JSON object.

# Actions:
1.  **Create a Story**: Based on the character "{character}" and the theme "{theme}", write a short, humorous story in Traditional Chinese (under 200 characters). The story must have a setup, a twist, and a punchline.
2.  **Create Scenes**: Break the story into 3 key visual scenes. For each scene, write a `scene_description` in Traditional Chinese. Then, create a detailed, cinematic `video_prompt_english` for an AI video generator. Append ", 8k, best quality, cinematic lighting, cute and adorable style" to each English prompt.

# JSON Output Structure:
The final output must be a single JSON object.
- The root object must have a key named "story_t_chinese" with the story as its value.
- The root object must also have a key named "scenes" which must be an array of exactly 3 objects.
- Each object inside the "scenes" array must have three keys:
  - "scene_number": an integer (1, 2, or 3).
  - "scene_description": the Traditional Chinese description.
  - "video_prompt_english": the detailed English prompt.

Do not output any text, explanations, or markdown formatting outside of the single JSON object.
"""


@app.route('/generate-story', methods=['POST'])
def generate_story():
    try:
        print("--- 函式開始執行，準備接收前端資料 ---")
        data = request.json
        character = data.get('character')
        theme = data.get('theme')

        if not character or not theme:
            return jsonify({"error": "缺少 'character' 或 'theme' 參數"}), 400

        final_prompt = PROMPT_TEMPLATE.format(character=character, theme=theme)
        
        print("--- 準備呼叫 OpenAI API ---")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates content in JSON format."},
                {"role": "user", "content": final_prompt}
            ]
        )
        
        # --- 【最終偵錯步驟】：在嘗試解析前，先印出完整的 response 物件 ---
        print("----------- OpenAI 回傳的完整 Response 物件 -----------")
        print(response)
        print("-----------------------------------------------------")

        # 這行現在很可能會因為 KeyError 而出錯，但沒關係，上面的 print 會先執行
        result_text = response.choices[0].message.content
        
        cleaned_json_string = result_text.strip()
        
        json.loads(cleaned_json_string) 
        print("--- JSON 格式驗證通過，準備回傳給前端 ---")
        
        return cleaned_json_string, 200, {'Content-Type': 'application/json; charset=utf-8'}

    except Exception as e:
        print(f"!!!!!!!!!! 處理過程中發生嚴重錯誤 !!!!!!!!!!")
        print(f"錯誤類型 (Error Type): {type(e)}")
        print(f"錯誤訊息 (Error Message): {e}")
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return jsonify({"error": "後端伺服器在與 AI 溝通時發生嚴重錯誤"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)