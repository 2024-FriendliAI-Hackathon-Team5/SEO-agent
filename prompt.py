rag_prompt = """
    Referring to the title and content of the given blog post, edit the blog post by refering relevant content.
    Write Modified blog post in Korean.

    Content: {content}

    Related content:
    {context}

    Modified blog post: 

    """

feedback_prompt = """
    Previous Response: {response}
    Feedback: {feedback}
    Modified Response:
    """