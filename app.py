import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="ClaimAudit", page_icon="🕵️‍♂️", layout="wide")

# --- GROQ CLIENT ---
@st.cache_resource
def get_groq_client():
    api_key = None
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY not found.")
        st.stop()
    return Groq(api_key=api_key)

client = get_groq_client()

# --- AUDIT PROMPT ---
audit_prompt = """You are an expert medical billing auditor. 
I will provide you with a batch of clinical notes. 
Your job is to find "Denial Risks" — missing information that would cause an insurance company to deny the claim.

Look specifically for:
1. Missing duration (e.g., "fever" but no "for how many days").
2. Missing dosage (e.g., "prescribed Panadol" but no "500mg").
3. Mismatch between Assessment and Plan.
4. Vague statements (e.g., "feeling unwell" without specific symptoms).

Output ONLY a markdown table with four columns:
| Note # | Issue Found | Why it's a risk | Suggested Fix |
|---|---|---|---|

If a note has no issues, write "Passed Audit" in the Issue Found column. Do not output anything else."""

# --- UI LAYOUT ---
st.title("🕵️‍♂️ ClaimAudit")
st.write("Scan batches of clinical notes to find denial risks *before* they are sent to insurance.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Paste Batch of Notes")
    st.write("Paste multiple notes below, separated by `---`.")
    
    # File uploader for text files
    uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"])
    
    default_text = ""
    if uploaded_file is not None:
        default_text = uploaded_file.read().decode("utf-8")
        
    notes_input = st.text_area(
        "Batch Notes:", 
        value=default_text,
        height=400, 
        placeholder="NOTE 1:\nSUBJECTIVE:\nPatient has fever.\nASSESSMENT:\nViral fever.\nPLAN:\nParacetamol.\n\n---\n\nNOTE 2:\nSUBJECTIVE:\nPatient has 3 days of abdominal pain..."
    )
    
    audit_btn = st.button("🚨 Audit Batch", use_container_width=True)

with col2:
    st.subheader("2. Audit Report")
    
    if audit_btn:
        if not notes_input.strip():
            st.warning("Please paste some notes first.")
        else:
            with st.spinner("Auditing notes for denial risks..."):
                try:
                    response = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[
                            {"role": "system", "content": audit_prompt},
                            {"role": "user", "content": f"Here are the notes:\n\n{notes_input}"}
                        ],
                        temperature=0.1
                    )
                    report = response.choices[0].message.content
                    st.success("Audit complete!")
                    st.markdown(report)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    else:
        st.info("The audit report will appear here.")

# Footer
st.divider()
st.caption("ClaimAudit · For demonstration purposes only. Always verify audit results with a certified medical coder.")
