import os
import math
from match_standard_name_json import (
    convert_excel_to_json,
    match_and_save_json,
    convert_all_json_to_excel
)

BATCH_SIZE = 500
TOTAL_ROWS = 14966
OUTPUT_DIR = "output"

print("🔄 Converting Excel to JSON (only once)...")
convert_excel_to_json()

total_batches = math.ceil(TOTAL_ROWS / BATCH_SIZE)

for i in range(total_batches):
    start = i * BATCH_SIZE
    end = min((i + 1) * BATCH_SIZE - 1, TOTAL_ROWS - 1)
    output_file = f"{OUTPUT_DIR}/matched_batch_{start}_{end}.json"

    if os.path.exists(output_file):
        print(f"✅ Batch {start}-{end} already exists. Skipping.")
        continue

    print(f"🚀 Processing batch {start}-{end}...")
    match_and_save_json(start, end)

print("📦 Combining all batches into final Excel file...")
convert_all_json_to_excel()
print("✅ All done.")
