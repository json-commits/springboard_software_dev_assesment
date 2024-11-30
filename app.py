import os, base64
import datetime
from http.client import responses

from flask import Flask, render_template, request
from dotenv import load_dotenv
from openai import OpenAI
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Loads API Keys
load_dotenv()

# Initializes the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# Flask Initialization
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index(msg=""):  # put application's code here
    if request.method == 'POST':
        return verify()

    return render_template('index.html')


# Verify input
def verify():
    # Check if file was attached
    if 'file' not in request.files:
        return render_template('index.html', msg="No file part")

    # Check if file exists
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', msg="No selected file")

    # Check if the file is valid
    if file and allowed_file(file.filename):
        # Saves and sanitizes the file
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        b64file = encode_image(f'./uploads/{filename}')

        # Sends the file over to GPT and removes it from storage
        reply = openai_verify(b64file, request.form)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return render_template('index.html', msg=reply)

    return render_template('index.html', msg="File not valid")


# GPT Verification
def openai_verify(file, form):
    # Builds the message giving context to GPT
    substitute_list = {"first_name": "First Name", "last_name": "Last Name", "id_no": "ID No.",
                       "date_of_birth": "Date of Birth", "valid_date": "Valid Date"}

    message_to_send = (f"Today is {datetime.datetime.today().date().strftime("%Y-%m-%d")}\n"
                       f"Are there any discrepancies between the provided information to the ones found in the image?\n")

    for form_value in form:
        message_to_send += f"\t{substitute_list[form_value]}: "
        if form[form_value] == '':
            message_to_send += "None given\n"
            continue

        message_to_send += f"{form[form_value]}\n"

    message_to_send += ("\nReply in this format if valid '[Valid] Confidence score: [0-100]'\n"
                        "If invalid reply in this format '[Invalid] Confidence score: [0-100] Reason: ...'\n")
    print(message_to_send)

    # Sends the prompt
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": message_to_send,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{file}"
                        },
                    },
                ],
            }
        ],
    )
    print(form)
    print(response)
    return response.choices[0].message.content


if __name__ == '__main__':
    app.run()
