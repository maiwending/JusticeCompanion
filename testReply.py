from smartinmate_automation import SmartInmateAutomation
import config
import time

if __name__ == "__main__":
    bot = SmartInmateAutomation(config.SMARTINMATE_USERNAME, config.SMARTINMATE_PASSWORD, headless=False)
    bot.login()
    print("Logged in. Reading first message...")
    message = bot.read_first_message()
    print(f"Sender: {message['sender']}")
    print(f"Content: {message['content']}")
    reply_text = "This is an automated test reply. Please ignore."
    print("Replying to the message...")
    bot.reply_to_message(reply_text)
    print("Reply attempted. Check the browser to confirm.")
    input("Press Enter to close the browser...")
    bot.driver.quit()