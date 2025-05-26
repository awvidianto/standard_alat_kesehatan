import os
import json
import pandas as pd
import requests
from tqdm import tqdm
from dotenv import load_dotenv

# Load env
load_dotenv("config.env")
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = os.getenv("DEEPSEEK_API_ENDPOINT")
API_MODEL = os.getenv("DEEPSEEK_MODEL")

BASE_DIR = "files"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_excel_to_json():
    hospital = pd.read_excel(f"{BASE_DIR}/bhmp_hospital.xlsx", header=None, names=["BHMP_HOSPITAL"])
    brand = pd.read_excel(f"{BASE_DIR}/bhmp_hospital_brand.xlsx", header=None, names=["BHMP_HOSPITAL_BRAND"])
    standard = pd.read_excel(f"{BASE_DIR}/standard_name_db.xlsx", header=None, names=["STANDARD_NAME"])
    
    df = pd.concat([hospital, brand], axis=1)
    df.to_json(f"{OUTPUT_DIR}/combined_data.json", orient="records", indent=2)
    standard.to_json(f"{OUTPUT_DIR}/standard_name_list.json", orient="records", indent=2)

def load_json_batch(start, end):
    with open(f"{OUTPUT_DIR}/combined_data.json") as f:
        all_data = json.load(f)
    return all_data[start:end+1]

def load_standard_list():
    with open(f"{OUTPUT_DIR}/standard_name_list.json") as f:
        items = json.load(f)
    return [item["STANDARD_NAME"] for item in items]

def get_filtered_candidates(bhmp, brand, candidates, max_count=100):
    keywords = set(str(bhmp).lower().split() + str(brand).lower().split())
    matches = [s for s in candidates if any(k in s.lower() for k in keywords)]
    return matches[:max_count]

def query_deepseek(bhmp, brand, candidate_list):
    if not candidate_list:
        return ""
    
    prompt = f"""
Given the following medical supply:
BHMP: {bhmp}
Brand: {brand}

Choose the most appropriate STANDARD_NAME from the list below:
{chr(10).join(f"- {c}" for c in candidate_list)}

Reply only with one exact match from the list. If nothing matches, reply: None.
""".strip()

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": API_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "top_p": 1,
        "n": 1,
        "stream": False
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("❌ Error:", e)
        return ""

def match_and_save_json(start, end):
    batch = load_json_batch(start, end)
    candidates = load_standard_list()

    for row in tqdm(batch, desc=f"Matching {start}-{end}"):
        bhmp = str(row.get("BHMP_HOSPITAL", "") or "").strip()
        brand = str(row.get("BHMP_HOSPITAL_BRAND", "") or "").strip()

        if not bhmp or not brand:
            row["STANDARD_NAME"] = ""
            continue

        filtered = get_filtered_candidates(bhmp, brand, candidates)
        match = query_deepseek(bhmp, brand, filtered)
        row["STANDARD_NAME"] = "" if match.lower() == "none" else match

    with open(f"{OUTPUT_DIR}/matched_batch_{start}_{end}.json", "w") as f:
        json.dump(batch, f, indent=2)
    print(f"✅ Saved: matched_batch_{start}_{end}.json")

def convert_all_json_to_excel():
    files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith("matched_batch_") and f.endswith(".json")]
    full_data = []

    for file in sorted(files):
        with open(os.path.join(OUTPUT_DIR, file)) as f:
            full_data.extend(json.load(f))

    df = pd.DataFrame(full_data)
    df.to_excel(f"{OUTPUT_DIR}/final_matched_results.xlsx", index=False)
    print("✅ Merged to final_matched_results.xlsx")
