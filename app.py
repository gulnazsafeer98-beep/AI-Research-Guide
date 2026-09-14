import os
import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI Research Guide Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling for clean UI layout
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        font-weight: bold;
        border-radius: 6px;
    }
    .stButton>button:hover {
        background-color: #004999;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("📚 AI Research Guide & Idea Generator")
    st.markdown("Transform your general interests into structured, academic-grade research proposals, clear objectives, and step-by-step methodologies.")

    # Sidebar inputs for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        api_key = st.secrets["GROQ_API_KEY"]

        st.divider()
        
        st.subheader("🎯 Parameters")
        platform = st.selectbox(
            "Platform / Venue",
            ["Academic Journal / Conference", "Research Community / Workshop"]
        )
        
        target_audience = st.selectbox(
            "Target Audience",
            ["Researchers", "University Students", "Industry Professionals", "General Audience"]
        )
        
        writing_tone = st.selectbox(
            "Writing Tone",
            ["Professional", "Academic", "Simple & Educational"]
        )
        
        content_length = st.selectbox(
            "Content Length",
            ["Short (Concise summary)", "Medium (Standard breakdown)", "Detailed (In-depth blueprint)"]
        )

    # Main Panel Input Form
    st.subheader("💡 Research Focus")
    research_field = st.text_input("Research Field or Domain", placeholder="e.g., Artificial Intelligence, Renewable Energy, Public Health")
    research_topic_interest = st.text_area("Specific Area of Interest / Problem Statement", placeholder="e.g., Applying LLMs to automate medical record parsing while preserving privacy.")

    generate_btn = st.button("Generate Research Guide 🚀")

    if generate_btn:
        if not api_key:
            st.error("Please provide a valid Groq API Key in the sidebar or via Streamlit Secrets.")
            return
        
        if not research_field or not research_topic_interest:
            st.warning("Please fill in both your research field and your area of interest.")
            return

        # Initialize Groq Client
        client = Groq(api_key=api_key)

        # Construct Prompt
        system_prompt = (
            "You are an expert academic research advisor and mentor. Your task is to provide structured, "
            "practical, and rigorous research guidance tailored to the user's explicit parameters."
        )
        
        user_prompt = f"""
        Generate a comprehensive research guide based on the following parameters:
        - Research Field: {research_field}
        - Specific Interest / Topic: {research_topic_interest}
        - Platform: {platform}
        - Target Audience: {target_audience}
        - Writing Tone: {writing_tone}
        - Content Detail Scope: {content_length}

        Provide the output cleanly structured with markdown headings for the following sections:
        1. **Relevant Research Topics & Titles**: Give 3 distinct, compelling research topic ideas within this domain.
        2. **Research Objectives**: Clear, specific, and measurable primary and secondary objectives.
        3. **Potential Research Gaps**: What existing literature or current approaches miss, and how this work addresses it.
        4. **Strategic Focus & Recommendations**: Crucial guidance on where to concentrate efforts.
        5. **Step-by-Step Research Methodology / Guidance**: Actionable roadmap from literature review to evaluation and final write-up.
        """

        with st.spinner("Synthesizing research structure via Groq (openai/gpt-oss-120b)..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    model="openai/gpt-oss-120b",
                    temperature=0.7,
                    max_tokens=2500
                )
                
                guide_output = chat_completion.choices[0].message.content
                
                st.success("Research Guide Successfully Generated!")
                st.markdown("---")
                st.markdown(guide_output)
                
                # Download option
                st.download_button(
                    label="Download Research Guide (.md)",
                    data=guide_output,
                    file_name="ai_research_guide.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"An error occurred while communicating with the Groq API: {e}")

if __name__ == "__main__":
    main()
