import time
import random

print("Running Randint Service..")
while True:
    time.sleep(1)
    f = open("randint-service.txt", "r")
    command = f.read()
    if command == "run":
        print("Random number generated and stored in communication pipeline.")
        time.sleep(.5)
        randint = random.randint(1, 100)
        print(f"Random Number Generated: {randint}")
        f = open("randint-service.txt", "w")
        f.write(str(randint))
        f.close()
