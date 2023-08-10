import requests
import time, random

messageId = 1
try:
    while True:
            print(messageId)
            url = f"http://127.0.0.1:8000/message?message=message {messageId}"
            print(url)
            response = requests.request("POST", url)
            print(f"URL hit : {messageId}")
            time.sleep(random.randint(0,2))
            messageId +=1
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")    
