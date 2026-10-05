import json
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
client = InferenceClient(token=os.environ.get("HF_TOKEN"))

with open("reports/profile.json", "r") as f:
    profile = json.load(f)

prompt = f"""You are a data-cleaning assistant. Analyse the provided dataset profile and identify potential data-quality problems in each column.
For every column, determine:

1. The likely meaning or role of the column based on its name and sample values.
2. The detected data type.
3. Whether missing, null, empty, or invalid values are present or likely.
4. Whether inconsistent formatting or categorical values are present.
5. Whether duplicate or suspicious values may exist.
6. Whether outliers or impossible values may be present, where applicable.
7. What cleaning or preprocessing action should be performed.

Return the result ONLY as valid JSON using this exact structure:
{{
"columns": [
{{
"column_name": "string",
"detected_type": "string",
"issues": [
"string"
],
"recommended_actions": [
"string"
]
}}
],
"dataset_level_issues": [
"string"
],
"general_recommendations": [
"string"
]
}}
Rules:

* Analyse only the information provided in the dataset profile.
* Do not invent values, columns, statistics, or patterns that are not supported by the provided information.
* If there is insufficient information to determine an issue, say so instead of guessing.
* Keep recommendations practical and suitable for automated data preprocessing.
* Do not modify the dataset yourself.
* Do not include Markdown, explanations, or code outside the JSON.
* Ensure the response is valid JSON that can be parsed directly by Python.

Dataset profile:
{json.dumps(profile, indent=2)}
"""

# Using a free, instruction-tuned model on HF's inference API.
# If this model is unavailable or rate-limited, swap the model name below.
response = client.chat_completion(
    messages=[{"role": "user", "content": prompt}],
    model="openai/gpt-oss-120b",
    max_tokens=3000,
)

suggestions = response.choices[0].message.content
print(suggestions)

with open("reports/ai_suggestions.txt", "w", encoding="utf-8") as f:
    f.write(suggestions)

print("\nSuggestions saved to reports/ai_suggestions.txt")
print("Check the output above -- free models often add extra text or")
print("markdown fences around the JSON. You may need to strip that")
print("before parsing it as JSON in apply_fixes.py.")