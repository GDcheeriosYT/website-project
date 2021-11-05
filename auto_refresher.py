import requests
import bs4
import dpkt

def hit_site(url):
    print(url)
    r = requests.get(url,stream = True)
    print(r.headers)
    print(r.encoding)
    print(r.status_code)
    print(r.json())
    print(requests.get(url,stream=True))
    print(r.request.headers)
    print(r.response.headers)
    for line in r.iter_lines():
        print(line)
    data = r.text
    soup = BeautifulSoup(data)
    return soup

hit_site("http://osu.ppy.sh")