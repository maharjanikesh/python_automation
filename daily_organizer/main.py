import time
import os
import shutil
import schedule
import smtplib
import datetime
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD').replace(" ", "")

FOLDER_PATH = "E:\\downloads"

def organize_files():
    """Organizes files in the Downloads folder into categorized subfolders."""
    summary = []
    extensions = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
        "PDFs": [".pdf"],
        "Others": []
    }

    for filename in os.listdir(FOLDER_PATH):
        filepath = os.path.join(FOLDER_PATH, filename)
        if not os.path.isfile(filepath):
            continue
        _, exts = os.path.splitext(filename)
        moved = False

        for folder, ext in extensions.items():
            if exts.lower() in ext:
                dest_folder = os.path.join(FOLDER_PATH, folder)
                os.makedirs(dest_folder, exist_ok = True)
                shutil.move(filepath, os.path.join(dest_folder, filename))
                summary.append(f"Moved: {filename} -> {folder}")
                print( f"Moved: {filename} -> {folder}")
                moved = True
                break
        if not moved:
            dest_folder = os.path.join(FOLDER_PATH, "Others")
            os.makedirs(dest_folder, exist_ok=True)
            shutil.move(filepath, os.path.join(dest_folder, filename))
            print( f"Moved: {filename} -> Others")
            summary.append(f"Moved: {filename} -> Others")

    if not summary:
        return "No files to organize."
    return "\n".join(summary)
        
def send_email(summary):
    """Sends an email with the summary of organized files."""
    msg = EmailMessage()
    msg['Subject'] = f'Daily Organizer Summary - {datetime.date.today()}'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg.set_content(summary)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)
    print("Email sent successfully.")
    
def __main__():
    summary = organize_files()
    send_email(summary)
    print("Files organized successfully.")

schedule.every(1).minute.do(__main__)
# schedule.every().day.at("18:00").do(__main__)
print("Scheduler started. Waiting for the scheduled time...")
while True:
    schedule.run_pending()
    time.sleep(2)