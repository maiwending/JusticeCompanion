from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from config import SMARTINMATE_URL

# Handles Selenium automation for smartinmate.com
class SmartInmateAutomation:
    def __init__(self, username, password, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.username = username
        self.password = password
        self.logged_in = False

    def login(self):
        self.driver.get(SMARTINMATE_URL)
        # TODO: Update selectors as needed for the login form
        time.sleep(2)
        username_input = self.driver.find_element(By.ID, 'memUsername')
        password_input = self.driver.find_element(By.ID, 'memPassword')
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(3)
        self.logged_in = True

    def read_first_message(self):
        if not self.logged_in:
            self.login()
        time.sleep(3)
        # Find the first message row by class 'row-fluid'
        first_message = self.driver.find_element(By.CSS_SELECTOR, '.row-fluid')
        first_message.click()
        time.sleep(2)
        # Get the full body text
        body_text = self.driver.find_element(By.TAG_NAME, 'body').text
        # Extract sender: find the line with the sender (between <p> and 'View All')
        sender = ''
        for line in body_text.split('\n'):
            if 'View All' in line:
                sender = line.split('View All')[0].strip()
                break
        # Extract content: between the first and second 'Reply   Delete   Messages'
        marker = 'Reply   Delete   Messages'
        splits = body_text.split(marker)
        content = ''
        if len(splits) > 2:
            content = splits[1].strip()
        else:
            content = body_text
        return {'sender': sender, 'content': content}

    def reply_to_message(self, reply_content):
        if not self.logged_in:
            self.login()
        time.sleep(2)
        # Click the Reply button (assuming the first visible Reply button is for the open message)
        reply_buttons = self.driver.find_elements("css selector", "a.btn.btn-primary")
        for btn in reply_buttons:
            if 'Reply' in btn.text:
                btn.click()
                break
        time.sleep(2)
        # Find the textarea or input for the reply message
        textarea = None
        possible_selectors = ['textarea', 'input[type="text"]', 'input[type="search"]']
        for selector in possible_selectors:
            elements = self.driver.find_elements("css selector", selector)
            if elements:
                textarea = elements[0]
                break
        if textarea:
            textarea.clear()
            textarea.send_keys(reply_content)
            time.sleep(10)
            # Fill subject if empty
            try:
                subject_input = self.driver.find_element("id", "mesSubject")
                subject_value = subject_input.get_attribute("value")
                if not subject_value:
                    subject_input.clear()
                    subject_input.send_keys("AI Response")
            except Exception as e:
                print('Subject input not found or could not be filled:', e)
            # Check the required checkbox before sending
            # try:
            #     checkbox = self.driver.find_element("id", 'doTransferCredit')
            #     if not checkbox.is_selected():
            #         checkbox.click()
            #         time.sleep(1)
            # except Exception as e:
            #     print('Checkbox not found or could not be clicked:', e)
            # Find and click the send/submit button
            try:
                try:
                    send_button = self.driver.find_element("name", "btnSubmit")
                except Exception:
                    send_button = self.driver.find_element("xpath", "//input[@type='submit' and @name='btnSubmit' and @value='Send This Message Now']")
                send_button.click()
                time.sleep(2)
                # Handle alert after clicking send
                try:
                    alert = self.driver.switch_to.alert
                    print(f"Alert Text: {alert.text}")
                    alert.accept()
                    print("Alert accepted.")
                except Exception as alert_e:
                    print(f"No alert to accept or error handling alert: {alert_e}")
            except Exception as e:
                print('Send button not found or could not be clicked:', e)
            time.sleep(2)
        else:
            print('Reply textarea/input not found.')
