import urllib.request
import time
import match_data

#refresh

def pageloadandclose():
  page = urllib.request.urlopen('http://192.168.1.22:5000/refresh')
  page.close()

#main process

while True:

    task = input("what you wanna do?\n1.refresh match\n")

    if task == "1":
        task1 = input("would you like to set a timer to automatically reload user data?\ny = yes\nn = no\n")
        #task1 settings
        if task1 == "n":
            print("refreshing match\n")
            pageloadandclose()
            print("match refreshed\n")
        elif task1 == "y":
            print(f"alright will refresh every {len(match_data.users) * 2 + 1} seconds")
            while True:
                time.sleep(int(len(match_data.users) * 2 + 1))
                pageloadandclose()
                print("match refreshed\n")
        else:
            print("POOOP")
    
    else:
        pass

'''while True:
    time.sleep(5)
    pageloadandclose()
    print("info refreshed")'''
