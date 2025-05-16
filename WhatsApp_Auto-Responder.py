import pyautogui
import time
import pyperclip
import webbrowser

# Enable failsafe: move mouse to top-left corner to abort script
pyautogui.FAILSAFE = True

try:
    webbrowser.open("https://web.whatsapp.com/")
    time.sleep(8)
    pyautogui.click(384, 381,button='left')
    time.sleep(10)

    # For chatgpt operations
    webbrowser.open("https://chatgpt.com/")
    time.sleep(6)
    # Prompt for the chatgpt to understand how is it suppose to unterstand
    pyautogui.write("Reply in a friendly manner as if you are a me and reply as brief as possible: ")
    time.sleep(2)
    pyautogui.hotkey('enter')
    time.sleep(10)
    # Back to the watsapp web to copy the chat 
    pyautogui.hotkey('ctrl','1')

    # Full screen
    pyautogui.hotkey('F11')

    # Click to activate window
    pyautogui.click(500, 500, button='left')
    time.sleep(1)

    # Select the chat
    pyautogui.click(382, 306, button='left')
    while True:
        time.sleep(5)
        # Selecting the chat history to feed chatgpt
        pyautogui.moveTo(698, 152)
        pyautogui.mouseDown()
        pyautogui.dragTo(1478, 1007, duration=1.0)  # Slower drag
        pyautogui.mouseUp()

        # Wait, copy, then read clipboard
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        pyautogui.click(698, 152, button='Left')
        chat_history = pyperclip.paste()

        # Pasting the copied chat to the gpt
        time.sleep(1)
        pyautogui.hotkey('ctrl', '2')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('enter')
        time.sleep(10)

        # Copying the responce from the gpt
        pyautogui.moveTo(360, 70)
        pyautogui.mouseDown()
        pyautogui.dragTo(1570, 1033, duration=1.0)  # Slower drag
        pyautogui.mouseUp()

        # Coying the responce from the gpt
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.5)
        pyautogui.click(698, 152, button='Left')
        new_chat_history = pyperclip.paste()

        if new_chat_history == chat_history:
            continue
        else:
            if ":" in new_chat_history:
                # Take the part after the first colon and remove any leading/trailing spaces
                message = new_chat_history.split(":", 1)[1].strip()  
            else:
                # If no colon, take the whole response as message
                message = new_chat_history.strip()  
            
            # Only process the message if it's non-empty
            if message:
                if chat_history != message:
                    pyautogui.hotkey('ctrl', '1')
                    pyautogui.write(message)  # Only send the message after the colon
                    pyautogui.hotkey('enter')
            else:
                print("Received an empty or irrelevant response, skipping.")
            
            time.sleep(3)

except Exception as e:
    print("An error occurred:", e)
    
except ValueError as v:
    print(f"There was value error{v}")
