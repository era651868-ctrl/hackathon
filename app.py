import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
import os

# --- 1. PAGE SETUP & THEME ---
st.set_page_config(
    page_title="DocuMind AI | Tech Doc Generator",
    page_icon="📝",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stTextArea textarea { background-color: #1e293b !important; color: #f8fafc !important; font-family: monospace; }
    .stSelectbox div { background-color: #1e293b !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. VERTEX AI CORE SETUP ---
@st.cache_resource
def init_vertex():
    try:
        if os.path.exists("key.json"):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
        
        # Explicitly tracking your active 2026 project context
        vertexai.init(project="election-assistant-495111", location="us-central1")
        return GenerativeModel("gemini-2.5-flash")
    except Exception as e:
        st.error(f"Cloud Engine Error: {e}")
        return None

ai_model = init_vertex()

# --- 3. UI SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("📝 DocuMind AI")
    st.caption("Automated Technical Documentation Agent")
    st.markdown("---")
    doc_style = st.selectbox(
        "Select Output Format:",
        ["Standard README.md", "Detailed API Reference", "Architectural Overview", "Code Logic & Flow Explainer"]
    )
    st.markdown("---")
    st.info("💡 Target: Upload or paste complex code snippets to generate structured developer resources instantly.")

# --- 4. MAIN WORKSPACE ---
st.title("🚀 Technical Documentation Generator")
st.write("Automatically transform messy raw code into clear, production-grade technical documentation.")

# Code Input Field
raw_code = st.text_area("Paste your source code here (Python, Java, C, etc.):", height=300, placeholder="# Paste code here...")

if st.button("✨ Generate Documentation"):
    if not raw_code.strip():
        st.warning("Please provide source code to analyze.")
    elif ai_model is None:
        st.error("AI backend offline. Check Google Cloud IAM settings.")
    else:
        with st.spinner("Analyzing code architecture and parsing metadata..."):
            try:
                # Custom system framing matching the user's design parameters
                system_prompt = f"""
                You are a Senior Principal Technical Writer. Analyze the following source code and generate a professional, exhaustive {doc_style} in clean Markdown format.
                Include:
                1. High-level architecture explanation.
                2. Functional breakdown (classes, functions, parameters, and return types).
                3. Computational complexity indicators if applicable.
                4. Clear code usage examples.
                
                Code to review:
                {raw_code}
                """
                
                response = ai_model.generate_content(system_prompt)
                
                st.success("🎉 Documentation Generated Successfully!")
                st.markdown("---")
                
                # Render the Markdown directly in the UI
                st.markdown(response.text)
                
                # Download Button for the generated asset
                st.download_button(
                    label="📥 Download Markdown File",
                    data=response.text,
                    file_name="README.md",
                    mime="text/markdown"
                )
                st.balloons()
                
            except Exception as e:
                st.error(f"Error during document synthesis: {e}")
  
