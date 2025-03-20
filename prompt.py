from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate(
    input_variables=["chat_history", "cv_info", "user_input"],
    template="""
    Here is the conversation history so far:
    {chat_history}

    Additional relevant CV Information:
    {cv_info}

    Now, answer the following question in a professional and structured manner:
    User's Question: {user_input}
    AI's Response:
    """
)
