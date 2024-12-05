import openai

EVALUATION_CRITERIA = {
    "clarity": "How clear and unambiguous is the prompt?",
    "specificity": "Does the prompt specify what is expected in the output?",
    "relevance": "Is the prompt directly related to the intended task?",
    "completeness": "Does the prompt provide all necessary context for the task?",
    "neutrality": "Is the prompt free from bias or leading language?",
    "efficiency": "Is the prompt concise and free of unnecessary verbosity?",
}

class PromptEvaluator:
    def __init__(self, api_key):
        openai.api_key = api_key

    def query_model(self, prompt, criterion, question):
        evaluation_question = f"On a scale of 1 to 5, evaluate the following prompt based on {criterion}:\n\n" \
                              f"Prompt: {prompt}\n\n" \
                              f"Question: {question}\n\n" \
                              f"Provide only the numeric score (1-5) and a brief explanation."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an assistant that evaluates prompts."},
                      {"role": "user", "content": evaluation_question}],
            temperature=0.2
        )
        return response['choices'][0]['message']['content'].strip()

    def evaluate_prompt(self, prompt):
        scores = {}
        for criterion, question in EVALUATION_CRITERIA.items():
            response = self.query_model(prompt, criterion, question)
            try:
                score = int(response.split()[0])
                explanation = " ".join(response.split()[1:])
                scores[criterion] = {"score": score, "explanation": explanation}
            except (ValueError, IndexError):
                scores[criterion] = {"score": 0, "explanation": "Invalid response from model."}

        total_score = sum(entry["score"] for entry in scores.values())
        return scores, total_score
