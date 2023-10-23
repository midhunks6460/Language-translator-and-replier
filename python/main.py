from flask import Flask, request, render_template
import openai

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = "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"

@app.route("/", methods=["GET", "POST"])
def index():
    generated_subject = generated_content =generated_output= ""
    error_message = ""

    if request.method == "POST":
        subject_text = request.form["subject"]
        content_idea = request.form["content"]

        try:
            # Generate content prompt
            content_prompt = f"Translate the given text into the {content_idea}: {subject_text}"
            content_response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=content_prompt,
                max_tokens=50  # Adjust as needed
            )
            generated_content = content_response.choices[0].text

            # Generate subject prompt
            subject_prompt = "Generate a proper reply for the content" + subject_text
            subject_response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=subject_prompt,
                max_tokens=50  # Adjust the token limit as needed
            )
            generated_subject = subject_response.choices[0].text.strip()

            # Generate content prompt
            output_prompt = f"Translate the given text into the {content_idea}: {generated_subject}"
            output_response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=output_prompt,
                max_tokens=50  # Adjust as needed
            )
            generated_output = output_response.choices[0].text

        except Exception as e:
            error_message = "An error occurred. Please refresh and try again."

    return render_template("index.html", generated_subject=generated_subject, generated_content=generated_content,generated_output=generated_output, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)


