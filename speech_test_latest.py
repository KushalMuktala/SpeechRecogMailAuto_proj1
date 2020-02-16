import random
import time
import test_db
import speech_recognition as sr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)

    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"

    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def mail_send():
    email = 'kushalmuktala@gmail.com'
    password = 'hpsrules'
    send_to_email = 'kushalmuktala@gmail.com'
    subject = 'Test with subj'  # The subject line
    message = 'This is my message'

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()  # You now need to convert the MIMEMultipart object to a string to send
    server.sendmail(email, send_to_email, text)
    server.quit()

if __name__ == "__main__":

    WORDS = ["approved"]
    NUM_GUESSES = 3
    PROMPT_LIMIT = 5

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    word = random.choice(WORDS)
    time.sleep(3)

    for i in range(NUM_GUESSES):

        for j in range(PROMPT_LIMIT):
            print('Guess {}. Speak!'.format(i + 1))
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")

        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        print("You said: {}".format(guess["transcription"]))

        guess_is_correct = guess["transcription"].lower() == word.lower()
        user_has_more_attempts = i < NUM_GUESSES - 1

        if guess_is_correct:
            mail_send()
            print("Correct! Status Approved".format(word))
            break
        elif user_has_more_attempts:
            print("Incorrect. Try again.\n")
        else:
            print("Sorry, try running it again.".format(word))
            break



