# Flask Web Application: ID Verification with GPT-4o-mini

This project is a Flask-based web application designed to verify user-entered data against a submitted ID. By integrating the GPT-4o-mini model, it provides an intelligent and streamlined approach to ensure data accuracy and compliance.

## Installation

1. Clone the repository:
   Open a terminal (e.g., Command Prompt or PowerShell) and run:
   ```cmd
   git clone https://github.com/json-commits/springboard_software_dev_assesment.git
   cd your-repo-name
   
2. Set up a virtual environment:
   ```cmd
    python -m venv venv
    venv\Scripts\activate
   
3. Install the required Python libraries:
    ```cmd
    pip install -r requirements.txt
   
4. Make a .env containing the following format:
    ```cmd
    OPENAI_API_KEY = "[YOUR TOKEN HERE]"
   
5. Start the Flask development server:
    ```cmd
    flask run
   
6. Open your browser and navigate to:
    ```cmd
   http://127.0.0.1:5000/

## Usage
1. Navigate to the web application in your browser.
2. Enter the required details (e.g., name, date of birth, validity date).
3. Upload a scanned copy or image of your ID.
4. Click the "Submit" button.
5. View the verification results provided by GPT-4o-mini.

## Project Structure
    .
    ├── app.py             # Main Flask application
    ├── templates/         # HTML templates
    ├── static/            # Static files (CSS, JS, images)
    ├── uploads/            # Uploaded files to temporary storage
    ├── requirements.txt   # Python dependencies
    ├── README.md          # Project documentation
    └── venv/              # Virtual environment (not included in Git)
    └── .env              # Environment variables (not included in Git)
