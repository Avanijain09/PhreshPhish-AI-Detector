import streamlit as st
import json
from extractor import compact_html
from llm_infer import analyze_page_with_llm

# --- Page Configuration ---
st.set_page_config(
    page_title="PhreshPhish | AI Phishing Detector",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Header Section ---
st.title("🛡️ PhreshPhish AI")
st.markdown("### Next-Gen Phishing Detection powered by Llama-3.2")
st.write("Enter the URL and HTML source code of a webpage below to analyze its threat level. Our custom fine-tuned 3B parameter AI model will evaluate it for advanced phishing indicators.")

st.divider()

# --- Input Section ---
url_input = st.text_input("🌐 Webpage URL", placeholder="https://example.com/secure-login")
html_input = st.text_area("💻 HTML Source Code", height=250, placeholder="Paste the raw HTML source code of the webpage here...")

# --- Analysis Action ---
if st.button("Analyze Webpage", type="primary", use_container_width=True):
    if not url_input or not html_input:
        st.warning("⚠️ Please provide both the URL and HTML source code to proceed with the analysis.")
    else:
        # Loading State with Status Container
        with st.status("Running analysis pipeline...", expanded=True) as status:
            st.write("🔍 Extracting critical DOM features and sanitizing payload...")
            compact_data = compact_html(url_input, html_input)
            
            st.write("🧠 Querying custom Llama-3.2 model (Inference may take 10-30 seconds)...")
            result = analyze_page_with_llm(compact_data)
            
            status.update(label="Analysis Complete!", state="complete", expanded=False)
            
        # --- Results Display ---
        st.divider()
        st.subheader("📊 Analysis Results")
        
        verdict = result.get("verdict", "unknown").lower()
        
        # 1. Verdict Banner
        if verdict == "phish":
            st.error("🚨 **THREAT DETECTED:** This webpage exhibits strong indicators of a phishing attack. Proceed with extreme caution.")
        elif verdict == "benign":
            st.success("✅ **SAFE:** No significant phishing indicators were found. This webpage appears legitimate.")
        else:
            st.warning("⚠️ **INCONCLUSIVE:** The model could not determine a definitive verdict.")
            
        # 2. Key Metrics Columns
        col1, col2 = st.columns(2)
        with col1:
            confidence = result.get("confidence", 0) * 100
            st.metric("Model Confidence", f"{confidence:.1f}%")
        with col2:
            brand = result.get("impersonated_brand")
            st.metric("Impersonated Brand", brand if brand else "None Detected")
            
        # 3. Rationale
        st.markdown("### 📝 AI Rationale")
        st.info(result.get("rationale", "No explanation provided by the model."))
        
        # 4. Technical Details (For recruiters/developers)
        with st.expander("🔎 Threat Indicators (Extracted Features)"):
            indicators = result.get("indicators", [])
            if indicators:
                for ind in indicators:
                    severity = ind.get('severity', 'low').upper()
                    st.markdown(f"- **{ind.get('type', 'Unknown')}** ({severity} severity): {ind.get('evidence', 'No evidence')}")
            else:
                st.write("No suspicious structural indicators flagged by the extractor.")
                
        with st.expander("⚙️ Developer Data (Raw JSON Output)"):
            st.write("**Sanitized DOM Payload (Input to LLM):**")
            st.json(compact_data)
            st.write("**Raw LLM Output:**")
            st.json(result)