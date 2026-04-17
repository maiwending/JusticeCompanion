from smartinmate_automation import SmartInmateAutomation
import config
import time

if __name__ == "__main__":
    try:
        bot = SmartInmateAutomation(config.SMARTINMATE_USERNAME, config.SMARTINMATE_PASSWORD, headless=False)
        bot.login()
        print("Login attempted. Browser will remain open for 30 seconds for inspection.")
        time.sleep(30)
    except Exception as e:
        print(f"Exception during login: {e}")
    finally:
        input("Press Enter to close the browser...")
        bot.driver.quit()
