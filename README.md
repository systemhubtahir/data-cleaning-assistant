# Data Cleaning Assistant

## What it does

A human-in-the-loop data cleaning pipeline: profiles a messy dataset, sends the profile (not raw data) to an LLM for column-level fix suggestions, and requires manual review/accept/reject/modify before applying any fix.

## Tools used

Python, pandas, Hugging Face Inference API (openai/gpt-oss-120b), python-dotenv

## Run locally

1. Create `.env` with your `HF_TOKEN`
2. `pip install -r requirements.txt`
3. `python profile_data.py`
4. `python clean_with_ai.py`
5. `python apply_fixes.py`

## Results

21 → 20 rows after removing an exact duplicate the AI couldn't detect. Normalized fragmented Yes/Y/No/N values to booleans. Replaced a hidden literal `"N/a"` string (in both Paying Customer and Address) with real NaN — caught by manual `.unique()` inspection after the AI's profile-based check missed it. Fixed stray characters in names with a targeted regex. Standardized phone numbers to 10-digit strings, including a fix for a pandas-specific float-coercion bug the AI's suggestion didn't account for.

## Step 6 Review (AI suggestion vs. my decision)

| Column | Decision | Why |
| --- | --- | --- |
| CustomerID | Override | AI couldn't confirm duplicates from column metrics alone; I manually caught and removed the Anakin Skywalker duplicate |
| First_Name | Accept | Safe whitespace trim |
| Last_Name | Modify | AI's fix too broad (would strip valid hyphenated names); used targeted regex instead |
| Phone_Number | Modify | AI missed a pandas-specific bug (`.0` getting baked into mixed-null numeric columns); added a fix step |
| Address | Modify | AI's profile showed 0 missing values, but manual `.unique()` check found a hidden `"N/a"` string it missed |
| Paying Customer | Accept | AI correctly caught Yes/Y/No/N/N-a fragmentation |
| Do_Not_Contact | Accept | AI correctly normalized booleans, preserved real NaNs |
| Not_Useful_Column | Accept | AI correctly flagged for removal |

## Limitations

* The AI's analysis is only as good as the profile summary it receives — it missed both the CustomerID duplicate and the Address `"N/a"` string because neither was included in what was sent to it. Manual spot-checks caught both.
* The AI's suggestions lacked pandas-specific implementation detail (e.g., the float-coercion issue in Phone_Number) — useful for *what* to fix, not always *how* to implement it safely.

## Current status

Complete — profiling, AI suggestion, manual review, and fix application all run end-to-end, verified against real output.
