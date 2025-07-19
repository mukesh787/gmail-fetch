This is a FastAPI project to get the last 200 emails from Gmail using Gmail API.

The API has one endpoint:

GET /emails - returns the sender and subject of your last 200 emails.

To run this project:

1. make sure you have Python 3 installed

2. create a virtual environment (if you can't install with pip due to system restrictions):

   python3 -m venv gmailenv
   source gmailenv/bin/activate

3. install the required packages:

   pip install -r requirements.txt

4. run the server:

   uvicorn main:app --reload

5. open your browser at http://localhost:8000/emails

Important:

This app uses Gmail API and needs access via OAuth. Since the app is in testing mode, only test users can access it.

If you want to test this, send me your Gmail address and I will add you as a test user.

my email: mukeshadhikary786@gmail.com

After that, when you run the app, a browser window will open to let you login with your Gmail account.

You might see a warning "Google hasn’t verified this app", just click "Advanced" and continue.

Thanks.
