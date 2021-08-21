import urllib.request
import time

#refresh

def pageloadandclose():
  page = urllib.request.urlopen('http://192.168.1.4:5000/refresh')
  page.close()

#main process

while True:

    task = input("what you wanna do?\n1.refresh match\n")

    if task == "1":
        print("refreshing match\n")
        pageloadandclose()
        print("match refreshed\n")
    else:
        pass

'''while True:
    time.sleep(5)
    pageloadandclose()
    print("info refreshed")'''