# app.py
import streamlit as st
from style_analyzer import StyleAnalyzer

# Page configuration
st.set_page_config(
    page_title="Writing Style Analyzer",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .main {
            padding: 2rem;
        }
        .stTextInput>div>div>input {
            padding: 0.5rem;
        }
        .stTextArea>div>div>textarea {
            padding: 0.5rem;
        }
        .css-1d391kg {
            padding: 2rem 1rem;
        }
        .stButton>button {
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

class StreamlitApp:
    def __init__(self):
        self.init_session_state()
        self.analyzer = None

    def init_session_state(self):
        """Initialize session state variables."""
        if 'style_analysis' not in st.session_state:
            st.session_state.style_analysis = None
        if 'generated_article' not in st.session_state:
            st.session_state.generated_article = None

    def setup_sidebar(self):
        """Setup sidebar with API key input and about section."""
        with st.sidebar:
            st.title("⚙️ Settings")
            api_key = st.text_input("Enter OpenAI API Key", type="password")
            if api_key:
                self.analyzer = StyleAnalyzer(api_key)
                
            st.markdown("---")
            st.markdown("### About")
            st.markdown("""
            This app analyzes writing styles and generates articles 
            based on the analyzed style. Perfect for content creators 
            and marketing professionals.
            """)
        return api_key

    def style_analysis_tab(self, api_key):
        """Render the style analysis tab."""
        st.header("Writing Style Analysis")
        st.markdown("Provide three writing samples to analyze the writing style.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sample_1 = st.text_area("Writing Sample 1", height=200,
                                  placeholder="Enter your first writing sample here...")
            sample_2 = st.text_area("Writing Sample 2", height=200,
                                  placeholder="Enter your second writing sample here...")
        
        with col2:
            sample_3 = st.text_area("Writing Sample 3", height=200,
                                  placeholder="Enter your third writing sample here...")
            
            if st.button("Analyze Writing Style", type="primary", use_container_width=True):
                if not api_key:
                    st.error("Please enter your OpenAI API key in the sidebar.")
                elif not all([sample_1, sample_2, sample_3]):
                    st.error("Please provide all three writing samples.")
                else:
                    with st.spinner("Analyzing writing style..."):
                        try:
                            st.session_state.style_analysis = self.analyzer.analyze_writing(
                                sample_1, sample_2, sample_3
                            )
                            st.success("Analysis complete!")
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
        
        if st.session_state.style_analysis:
            st.markdown("### Analysis Results")
            st.markdown(st.session_state.style_analysis)

    def article_generation_tab(self, api_key):
        """Render the article generation tab."""
        st.header("Article Generation")
        
        if not st.session_state.style_analysis:
            st.warning("Please complete the style analysis first.")
        else:
            st.info("Style analysis is ready! You can now generate an article.")
            
            interview_transcript = st.text_area(
                "Interview Transcript",
                height=200,
                placeholder="Paste your interview transcript here..."
            )
            
            preliminary_notes = st.text_area(
                "Preliminary Notes",
                height=200,
                placeholder="Paste your preliminary notes here..."
            )
            
            if st.button("Generate Article", type="primary", use_container_width=True):
                if not api_key:
                    st.error("Please enter your OpenAI API key in the sidebar.")
                elif not all([interview_transcript, preliminary_notes]):
                    st.error("Please provide both interview transcript and preliminary notes.")
                else:
                    with st.spinner("Generating article..."):
                        try:
                            st.session_state.generated_article = self.analyzer.generate_article(
                                st.session_state.style_analysis,
                                interview_transcript,
                                preliminary_notes
                            )
                            st.success("Article generated successfully!")
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
            
            if st.session_state.generated_article:
                st.markdown("### Generated Article")
                st.markdown(st.session_state.generated_article)
                
                st.download_button(
                    label="Download Article",
                    data=st.session_state.generated_article,
                    file_name="generated_article.txt",
                    mime="text/plain"
                )

    def run(self):
        """Run the Streamlit application."""
        st.title("✍️ Writing Style Analyzer & Article Generator")
        
        api_key = self.setup_sidebar()
        
        tabs = st.tabs(["Style Analysis", "Article Generation"])
        
        with tabs[0]:
            self.style_analysis_tab(api_key)
        
        with tabs[1]:
            self.article_generation_tab(api_key)

if __name__ == "__main__":
    app = StreamlitApp()
    app.run()