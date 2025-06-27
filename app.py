import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.ingestion import ingest_files
from src.transformation import preprocess, enrich
from src.validation import validate_and_profile
from src.loader import save_to_parquet
import base64


# Page setup
st.set_page_config(page_title="🌾 Nishant - Agri Sensor Pipeline", layout="wide")

# Remove default top padding
st.markdown("""
    <style>
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=STIX+Two+Text&display=swap');

    /* Apply to everything */
    html, body, [class*="css"]  {
        font-family: 'STIX Two Text', serif !important;
    }

    /* Specific Streamlit classes to override */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown, .stText, .stHeader, .stSubheader,
    .stButton > button, .stDownloadButton > button,
    .stDataFrame, .stAlert, .stSelectbox label,
    .stTextInput, .stFileUploader label, .stForm, .stFormLabel {
        font-family: 'STIX Two Text', serif !important;
    }

    /* Table headers in DataFrames */
    .css-1d391kg, .css-1cpxqw2 {
        font-family: 'STIX Two Text', serif !important;
    }

    /* Remove top padding if needed */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    </style>
""", unsafe_allow_html=True)



# Page title


# Layout
left_col, right_col = st.columns(2)

# --- Left Container: Control Panel ---
with left_col:
    st.image("headertitle.png", use_container_width=True)
    # st.title("Agricultural Sensor Data Processing Dashboard")
    with st.container(height=428, border=True):  # ✅ fixed-height scrollable container
        st.subheader("Pipeline Control Panel")

        # Track data source in session state
        if "use_sample_file" not in st.session_state:
            st.session_state.use_sample_file = False

        # File uploader
        uploaded_files = st.file_uploader("Upload Parquet files", type=["parquet"], accept_multiple_files=True)

        # Use sample file button
        if st.button("📂 Use Sample Data"):
            st.session_state.use_sample_file = True
            st.success("✅ Using default file: sample_sensor_data.parquet")

        # If files uploaded manually, reset sample flag
        if uploaded_files:
            st.session_state.use_sample_file = False
            st.success(f"{len(uploaded_files)} file(s) uploaded.")

        run_pipeline = st.button("🚀 Run Full Pipeline")

        # ✅ Add PDF Viewer
        import base64
        with open("pipeline_process.pdf", "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        # pdf_display = f"""
        # <iframe
        #     src="data:application/pdf;base64,{base64_pdf}"
        #     width="100%"
        #     height="500"
        #     type="application/pdf"
        #     style="border: 1px solid #ccc; border-radius: 4px;"
        # ></iframe>
        # """
        st.markdown("### 📄 Complete Explanation of Pipeline")
        st.markdown("[🔗 View on GitHub](https://github.com/nishant0363/Datapipeline-processing-dashboard?tab=readme-ov-file#)")

        # st.markdown(pdf_display, unsafe_allow_html=True)



# --- Right Container: Output and Charts ---
with right_col:
    st.image("satsureheader.jpg", use_container_width=True)
    with st.container(height=428, border=True):  # ✅ fixed-height scrollable container
        if run_pipeline and (uploaded_files or st.session_state.use_sample_file):
            with st.spinner("Running pipeline..."):
                if st.session_state.use_sample_file:
                    df = pd.read_parquet("sample_sensor_data.parquet")
                else:
                    # Save uploaded files to disk
                    for file in uploaded_files:
                        with open(f"data/raw/{file.name}", "wb") as f:
                            f.write(file.getbuffer())
                    df = ingest_files()
                    df = preprocess(df)
                    df = enrich(df)
                    validate_and_profile(df)
                    save_to_parquet(df)

            st.success("Pipeline executed successfully!")

            # Load reports
            dq = pd.read_csv("data/data_quality_report.csv")
            gaps = pd.read_csv("data/data_gaps_report.csv")

            st.subheader("Data Quality Report")
            st.dataframe(dq, use_container_width=True)
            st.download_button("⬇ Download Quality Report", data=open("data/data_quality_report.csv", "rb"), file_name="data_quality_report.csv")

            st.subheader("Gaps in Sensor Data")
            st.dataframe(gaps, use_container_width=True)
            st.download_button("⬇ Download Gaps Report", data=open("data/data_gaps_report.csv", "rb"), file_name="data_gaps_report.csv")

            st.subheader("Sensor Trends")
            selected_sensor = st.selectbox("Select a sensor", df['sensor_id'].unique())
            selected_type = st.selectbox("Select reading type", df['reading_type'].unique())

            df_plot = df[(df['sensor_id'] == selected_sensor) & (df['reading_type'] == selected_type)].sort_values('timestamp')
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.lineplot(data=df_plot, x='timestamp', y='value', marker="o", ax=ax)
            ax.set_title(f"{selected_type.capitalize()} Readings for Sensor {selected_sensor}")
            ax.set_xlabel("Timestamp")
            ax.set_ylabel("Value")
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)

            if st.session_state.use_sample_file:
                pass
            else:
                st.subheader("Anomalous Readings")
                anomaly_df = df[(df['anomalous_reading']) & (df['reading_type'] == selected_type)]
                st.dataframe(anomaly_df[['sensor_id', 'timestamp', 'reading_type', 'value']], use_container_width=True)
        else:
            st.info("⬅️ Upload sensor data or click **Use Sample Data**, then click **Run Full Pipeline** to begin.")


# st.markdown("""<hr style="margin-top:2rem;margin-bottom:0.5rem;">""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; font-size:13px; padding:0.5rem 1rem;">
    <strong>Nishant</strong> &nbsp; | &nbsp;
    📧 <a href="mailto:nishant0363@gmail.com" target="_blank">nishant0363@gmail.com</a> &nbsp; | &nbsp;
    📱 <a href="tel:+919306145426" target="_blank">+91-9306145426</a> &nbsp; | &nbsp;
    🌐 <a href="https://nishant0363.github.io/projects.com" target="_blank">Portfolio</a> &nbsp; | &nbsp;
    💼 <a href="https://www.linkedin.com/in/nishant3603/" target="_blank">LinkedIn</a> &nbsp; | &nbsp;
    🐙 <a href="https://github.com/nishant0363" target="_blank">GitHub</a> &nbsp; | &nbsp;
    📄 <a href="https://drive.google.com/file/d/1hOJqhdY38XSEGrRRrjJsipSg2taqWYu-/view?usp=drive_link" target="_blank">Resume</a>
</div>
""", unsafe_allow_html=True)