from modules.intent_engine import detect_intent
from modules.analysis_engine import analyze
from modules.ai_engine import ask_gemini
from modules.semantic_model import build_semantic_model


def answer_query(df, question):

    # Detect intent
    intent = detect_intent(question)


    # Try normal analysis first
    answer = analyze(
        df,
        intent,
        question
    )


    # If analysis engine found an answer
    if answer and not (
        "I don't have enough information" in str(answer)
        or
        "couldn't understand" in str(answer)
    ):

        return answer



    # -----------------------------
    # Gemini fallback
    # -----------------------------

    semantic = build_semantic_model(df)


    sample_data = df.head(5).to_string()


    prompt = f"""

You are an expert Business Intelligence Analyst.

Dataset columns:
{list(df.columns)}

Semantic meaning:
{semantic}

Sample data:
{sample_data}


User question:
{question}


Answer the user like a professional data analyst.
Give useful business insights.
Do not invent numbers.
If calculation is needed, explain what metric should be calculated.

"""


    response = ask_gemini(prompt)


    return {
        "type": "text",
        "data": response
    }