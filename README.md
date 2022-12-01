# p2p-chat using ElGamal Encryption
# By Jeremy Boissevain
# CS 463
# 11/30/2022

# Developed and tested using Python 3.10. May not work on lower versions.

# Running Instructions:

To run via executable(Only works on Windows): 
    Navigate to the folder src\dist\chat
    Run the chat app using chat.exe in that folder.

To run via Python interpreter:
    Create a virtual environment and install requirements:
        In the command line, navigate to the root folder of the project.
        Run `python3 -m venv env`(`python -m venv env` in Windows) to create a virtual environment.
        Activate the environment using `source env/bin/ectivate` (`.\env\Scripts\activate` in Windows, or `.\env\Scripts\activate.ps1` for Powershell)
        Install the required packages using `python3 -m pip install -r requirements.txt` (`py -m pip install -r requirements.txt` in Windows)
        Run the chat using `python3 .\src\chat.py` (`py .\src\chat.py` in Windows)

To test using only one computer:
    Open two instances of the program, through either method described above
    Leave both IP Address fields as localhost.
    In the second window, change the server port to 3334, and the connect port to 3333, in order to match the server port of the first window.
    Press the "start server" button in both windows.
    Change your nickname in either window to whatever you would like.
    Press "connect to chat" in either window. 
    You can now enter text in the entry box on the bottom, and press send to send encrypted messages to the other window.

Controls:
    IP Address field: Public IP Address of the computer you want to connect to.
    Nickname field: The nickname you want to show up before your messages.
    Port field: The port of the server running on the peer you want to connect to.

    Server port: The port your own server process will bind to.

    start server button: Starts the server listening on the port specified in the server port Entry field

    Connect to chat button: Connects to specified IP and port in the top fields. YOU MUST START THE SERVER ON BOTH MACHINES BEFORE CONNECTING TO CHAT.