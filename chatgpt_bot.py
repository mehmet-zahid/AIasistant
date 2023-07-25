from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ChatgptBot:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        # keep the user logged in
        options.add_argument('--user-data-dir=chrome-data')

        self.driver = uc.Chrome(options=options)
        self.navigate_to_chatgpt()
        self.find_prompt_box()
        self.prompt_number = 1
        
    def navigate_to_chatgpt(self):
        """Navigate to the chatgpt website."""
        url = "https://chat.openai.com/"
        self.driver.get(url)

        # wait for the login in manually
        WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located((By.TAG_NAME, "textarea"))
        )
    
    def find_prompt_box(self):
        """Find the prompt box on the chatgpt website."""
        input_element = self.driver.find_element(By.TAG_NAME, "form")
        print(input_element)
        self.textarea = input_element.find_element(By.TAG_NAME, "textarea")
        print(self.textarea)
        self.button = input_element.find_element(By.TAG_NAME, "button")
        print(self.button)

    def get_response(self, child_number):
        chat_screen_output_prompt = self.driver.find_element(
            By.CSS_SELECTOR, f'#__next > div.overflow-hidden.w-full.h-full.relative.flex.z-0 > div.relative.flex.h-full.max-w-full.flex-1.overflow-hidden > div > main > div.flex-1.overflow-hidden > div > div > div > div:nth-child({child_number})'
            )
        return chat_screen_output_prompt.text

    def enter_prompt(self, prompt):
        """Enter the prompt into the prompt box and return the response."""
        
        self.textarea.send_keys(prompt)
        self.button.send_keys(Keys.ENTER)
        time.sleep(2)

        # wait for the response to be generated
        while True:
            try:
                # retreive buttons, check it has a text 'Regenerate response'
                buttons = self.driver.find_elements(By.TAG_NAME, 'button')
                for button in buttons:
                    
                    if button.text == 'Continue generating':
                        button.click()
                        continue
                    if button.text == 'Regenerate response':
                        response = self.get_response(self.prompt_number + 1)
                        raise Exception('Response generated')
                        
            # Stalement exception is thrown if the button is not visible
            except Exception as e:
                break
            time.sleep(2)
        self.prompt_number += 2
        return response

        
        
    def close(self):
        self.driver.quit()

    def start(self):
        """Run the bot."""
        while True:
            try:
                prompt = input("Enter a prompt: ")
                response = self.enter_prompt(prompt)
                print(response)
            except KeyboardInterrupt:
                self.close()
                break

    
