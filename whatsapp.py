
import pyautogui
import webbrowser as wb
import time

wb.open("web.whatsapp.com")

while True:
    time.sleep(4)
    pyautogui.typewrite("Whatsapp messages with Python")
    time.sleep(2)
    pyautogui.press("enter")


