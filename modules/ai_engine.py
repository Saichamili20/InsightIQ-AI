import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()


api_key = os.getenv("GOOGLE_API_KEY")


genai.configure(
    api_key=api_key
)


model = genai.GenerativeModel(
    "gemini-2.5-flash"
)



def ask_gemini(prompt):

    try:

        response = model.generate_content(
            prompt
        )

        return response.text


    except Exception as e:

        error = str(e)

        if "429" in error:

            return """
            ⚠️ AI Insights temporarily unavailable.

            Gemini API daily limit has been reached.
            Please try again later.
            """

        return f"Gemini Error: {error}"