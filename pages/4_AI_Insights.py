import streamlit as st

from utils.session_manager import get_business_data
from modules.kpi_engine import generate_kpis
from modules.insight_engine import analyze_dataset
from modules.ai_engine import ask_gemini
from modules.dataset_detector import detect_dataset


st.title("🧠 AI Insights")


df = get_business_data()


if df is None:

    st.warning(
        "Please upload dataset first."
    )

    st.stop()



analysis = analyze_dataset(df)

dataset_type = detect_dataset(df)
kpis = generate_kpis(df,dataset_type)

columns = df.columns.tolist()

sample_rows = df.head(5).to_string()



context = f"""
You are a senior business intelligence analyst.

Dataset Type:
{dataset_type}


Dataset Columns:

{columns}


Sample Data:

{sample_rows}


Dataset Analysis:

Rows:
{analysis["rows"]}

Columns:
{analysis["columns"]}


KPIs:

{kpis}

"""


with st.spinner(
    "Gemini is analyzing your business data..."
):
    response = ask_gemini(
    context +
    """

Provide a complete business analysis.

Include:
1. Key business insights
2. Important trends
3. Risks or problems
4. Business recommendations

IMPORTANT ANALYTICAL RULES:

1. Use only metrics provided.
2. Do not invent business facts.
3. If information is unavailable, explicitly state "Not available in dataset".
4. Do not calculate financial impact unless the required column exists.
5. Separate observed facts from assumptions.
6. Avoid industry assumptions unless supported by dataset columns.
7. Do not describe possible scenarios as facts.
8. Clearly label assumptions as "Possible interpretation".
9. Do not mention industries (banking, retail, healthcare etc.) unless dataset columns prove it.
10. If trends cannot be calculated because dates are unavailable, state that time-based analysis is unavailable.
"""
)


st.subheader(
    "🤖 Gemini Business Insights"
)


st.write(response)