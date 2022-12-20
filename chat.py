import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

class Generator():
  def __init__(self, api_key):
    self.api_key = api_key

class OpenAIGenerator(Generator):
  def generate(self, model="text-davinci-003", **kwargs):
    response = requests.post(
      "https://api.openai.com/v1/completions",
      headers={"Authorization": f"Bearer {self.api_key}"},
      json={"model": model, **kwargs},
    )
    r = response.json()
    try:
      return r["choices"][0]["text"]
    except:
      print(r)
      
driver = webdriver.Firefox()
driver.get("https://www.omegle.com")

def get_chatlog():
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  items = soup.find_all("div", class_="logitem")
  return "\n".join([item.text for item in items][2:])
  
def send(message):
  try:
    driver.find_element(By.CLASS_NAME, "chatmsg").send_keys(message)
    driver.find_element(By.CLASS_NAME, "sendbtn").click()
  except:
    pass

def disconnect():
  disconnectbtn = driver.find_element(By.CLASS_NAME, "disconnectbtn")
  try:
    disconnectbtn.click()
    disconnectbtn.click()
    disconnectbtn.click()
  except:
    pass

with open("api_key.txt", "r") as f:
  api_key = f.read()
  
gpt3 = OpenAIGenerator(api_key)

if __name__ == "__main__":

  with open("interests.txt", "r") as f:
    interests = f.read()
  print(interests.strip().replace("\n",","))


  done = False
  while not done:
    m = input(">")
    
    if not m:
      chatlog = get_chatlog()
      prompt = "Write a conversation from an online chat:\n" + chatlog + "\nYou:"
      
      response = gpt3.generate(model="text-davinci-003", prompt=prompt, temperature=1.3, max_tokens=128,stop="\n", frequency_penalty=0.5)
      
      send(response)
      
    elif m == "q":
      done = True
      
    elif m == "r":
      disconnect()
      
    else:
      send(m)
      
  driver.quit()
