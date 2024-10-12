
# CS4348 Project 1 - Encryption and Logger System

## Files Included:
- `driver.py`: The main driver program that launches the logger and encryption subprocesses and handles user interaction.
- `encryption.py`: The encryption program that handles passkey setting, encryption, and decryption using the Vigenère cipher.
- `logger.py`: The logging program that logs all actions with timestamps to a log file.
- `logfile.txt`: A sample log file showing the actions logged during a test run of the program.
- `README.txt`: This readme file providing details about the project and how to run it.
- `writeup.pdf`: The write-up explaining the project approach, organization, issues encountered, and lessons learned.

## How to Compile and Run the Project:
### Requirements:
- **Python 3.x**
- **colorama library** (for colored terminal output)
    - Install it using the following command:
      ```
      pip install colorama
      ```

### Running the Project:
1. **Run the driver program**:
   ```bash
   python3 driver.py logfile.txt
   ```

2. The `driver.py` program will launch both `logger.py` and `encryption.py` as subprocesses. It provides a menu-based interface that allows you to:
   - Set a passkey (password) for encryption.
   - Encrypt strings.
   - Decrypt strings.
   - View encryption and decryption history.
   - Quit the program, terminating all subprocesses.

3. Logs will be stored in the `logfile.txt`, which will include actions like passkey setting, encryption, decryption, and program exit.

## Other Notes for the TA:
- The project does not require any specific IDE to run.
- History of strings is stored in-memory for the duration of the session. It will not persist after the program exits.
- The project works on the cs1 and cs2 machines as long as Python 3 and the `colorama` library are installed.

---

# Write-up

## Project Approach:
I approached this project by dividing the tasks into three distinct programs:
1. **Logger**: This program handles logging all the important actions such as encryption, decryption, and password setting with timestamps.
2. **Encryption**: This program deals with setting a passkey, encrypting and decrypting strings using the Vigenère cipher.
3. **Driver**: The driver acts as the user interface that launches the other two programs and facilitates communication through subprocesses.

The **driver.py** program serves as the coordinator between the user and the two other programs, ensuring that input from the user is correctly routed to either the logger or the encryption process.

## Project Organization:
The project is organized in such a way to maximize modularity. Each program has a clearly defined role:
- `logger.py` is responsible only for logging, ensuring that logs are centralized and organized.
- `encryption.py` focuses only on encryption, passkey management, and decryption.
- `driver.py` handles the overall flow, communication, and user interaction.

This organization helps in maintaining clean separation of concerns and makes it easier to debug, maintain, and extend the project.

## Problems Encountered:
The key challenges I encountered included:
1. **Subprocess Communication**: One of the major issues was handling broken pipes, where the subprocesses (logger or encryption) would terminate unexpectedly, leading to errors when trying to send data to them.
2. **History Management**: Originally, the history stored plaintext and encrypted strings together, causing confusion when users tried to decrypt plaintext strings by mistake.
3. **Correct Input Validation**: Ensuring valid inputs from the user and making sure the program doesn’t crash when invalid selections or empty inputs are provided was another hurdle.

## How I Fixed Them:
1. **Subprocess Communication Fix**: I fixed the broken pipe issue by checking whether the subprocess is still alive before sending any data. This avoids attempting to communicate with a terminated process.
2. **History Management Fix**: I reorganized the history to keep track of plaintext and encrypted strings separately. Now, the program only allows selecting encrypted strings when decrypting, preventing errors and confusion.
3. **Improved Input Handling**: I implemented robust input validation to handle cases such as invalid choices or empty inputs gracefully.

## What I Learned:
This project taught me how to handle subprocess communication using Python’s `subprocess` module. I also learned the importance of properly managing process lifecycles, handling errors like broken pipes, and ensuring graceful exits.

Additionally, I gained experience in managing a more complex user interface and enhancing user experience by adding features like color-coded outputs using `colorama`.

## Incomplete Features:
All core features of the project have been implemented, including encryption, decryption, logging, and history management. However, if I had more time, I would have:
- Implemented file-based history storage so that encryption and decryption history could persist across sessions.
- Enhanced the security by introducing a stronger encryption algorithm like AES alongside the Vigenère cipher for comparison.

## What I Would Do with More Time:
- **Implement Persistent History**: By saving the history to a file, users could continue from where they left off in subsequent sessions.
- **Improve Encryption Security**: Adding more modern encryption algorithms would make the program more applicable to real-world scenarios.
- **Unit Testing**: I would add unit tests for all critical functions like encryption, decryption, and logging to ensure consistent behavior and prevent regression.
- **Extended Input Validation**: A more thorough input validation system could be implemented, checking for things like minimum passkey length, invalid characters in inputs, etc.

