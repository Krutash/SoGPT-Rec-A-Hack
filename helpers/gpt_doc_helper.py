import openai

# OpenAI GPT setup
openai.api_key = "your_openai_api_key"

# Summarize an uploaded document
def summarize_document(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    prompt = f"Summarize the following document:\n\n{content}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Analyze document contents
def analyze_document(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    prompt = f"Analyze the following document and identify key insights:\n\n{content}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300
    )
    return response.choices[0].text.strip()