from openai import OpenAI
from prompt import prompt_template
from embeddings import retrieve_releveant_cv_sections, load_cv
import os

print("Starting up CV Chatbot")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Check if the API key is set
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("✅ OpenAI API Key Found!")  # Confirms that the key exists
else:
    print("❌ ERROR: OPENAI_API_KEY Not Found!")  # If not found, will print an error

print("Loading CV")
load_cv()
chat_history = []


def chat_with_gpt(prompt):
    # print("Getting a response from OpenAI GPT-40 Mini...")
    # Retrieve relevant CV information
    relevant_cv_info = retrieve_releveant_cv_sections(prompt)

    # Keep last 3 exchanges in the prompt to avoid making the prompt too long
    # only keeps last 3 exchanges (6 messages user + AI)
    history_text = "\n".join(chat_history[-4:])

    # Apply Prompt Format
    full_prompt = prompt_template.format(
        chat_history=history_text,
        cv_info=relevant_cv_info,
        user_input=prompt
    )

    # Call OpenAI API

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are a professional AI assistant that helps users "
                "understand resumes and CVs."
                "Always provide structured, concise, "
                "and professional answers. "
                "If the CV does not contain the exact answer, analyze "
                "the user's experience and make "
                "a reasonable inference based on relevant "
                "skills, roles, and expertise. "
                "Clearly state if the CV does not explicitly confirm "
                "the answer, but explain why the "
                "user may or may not have the capability "
                "based on their experience. "
                "Avoid fabricating credentials or making "
                "unsupported claims."},
            {"role": "user", "content": full_prompt}
        ],
        max_tokens=300,
        temperature=0.7,
        top_p=0.9,)

    # Print response
    # print("Response from OpenAI:")
    # print(response.choices[0].message.content)
    chat_history.append(f"User: {prompt}")
    chat_history.append(f"AI: {response.choices[0].message.content}")
    return response.choices[0].message.content
