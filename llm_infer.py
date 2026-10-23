import json
import ollama
from schemas import PhishingAnalysis
from pydantic import ValidationError

PROMPT_TEMPLATE = """
You are a strict cybersecurity expert analyzing a webpage for phishing.

CRITICAL RULES:
1. A regular search box (asking for 'q', 'query') is NOT a credential form.
2. Subdomains belong to the main domain.
3. If safe, the verdict MUST be "benign" and the "indicators" list MUST be exactly []. Do not invent indicators.

Webpage Data:
{page_data}

DO NOT output schema definitions. Output ONLY a valid JSON object exactly matching this structure, filled with your analysis:
{{
  "verdict": "phish" or "benign",
  "confidence": 1.0,
  "impersonated_brand": null,
  "brand_domain_match": null,
  "indicators": [],
  "rationale": "Your explanation here."
}}
"""

def analyze_page_with_llm(compact_data: dict) -> dict:
    prompt = PROMPT_TEMPLATE.format(
        page_data=json.dumps(compact_data, indent=2)
    )

    print("Model soch raha hai... (CPU par thoda time lag sakta hai)")
    
    try:
        response = ollama.chat(
            model='phreshphish_ai',  # <--- YAHAN CHANGE KIYA HAI
            messages=[{'role': 'user', 'content': prompt}],
            format='json',
            options={'temperature': 0.1}
        )
        
        raw_output = response['message']['content']
        parsed_json = json.loads(raw_output)
        validated_result = PhishingAnalysis(**parsed_json)
        return validated_result.model_dump()

    except ValidationError as e:
        print("\n[Error] Model ne schema tod diya. Validation Error:")
        print(e)
        return {"error": "schema_validation_failed", "raw_output": raw_output}
    except Exception as e:
        print(f"\n[Error] Inference failed: {e}")
        return {"error": str(e)}