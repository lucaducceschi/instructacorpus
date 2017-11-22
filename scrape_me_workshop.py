## This bit of code extracts texts from the "workshop" section of instructables.
## it is still very rough, but it serves the purpouse. I will update it if I will need some new data in the future.
## So take this tool with a grain of salt, for the moment....

# This creates all the offests (i.e: the identifier of the urls that we want) for the workshop section of Instructables
#
# at present there are 59 pages in the section. 

and_counting=59
instructs_urls_offsets= []

# the number 33689, can be found in the url of last page of the workshop section.
# NB: the more pages the bigger the number: keep it under control from time to time
# Yes, the best way to do this is to create a bot that checks the number every week and updates the db. Lo faccio domani :-)
from bs4 import BeautifulSoup
import requests

while and_counting <33689:
    instructs_urls_offsets.append(and_counting)
    and_counting+= 59
    
# This creates all the urls 

a = "http://www.instructables.com/explore/category/workshop/?offset="
all_the_urls = [a+str(i) for i in instructs_urls_offsets]
all_the_urls.append("http://www.instructables.com/explore/category/workshop/")


# This extracts the links from all the pages listed in the a section.
# The links are not complete urls, but by adding the string "http://www.instructables.com"
# we are going to get exactly what we need 

def extract_links_from_urls(list_of_links):
    links_bucket = []
    for i in list_of_links:
        raw_soup = BeautifulSoup(requests.get(i).text, "lxml")
        links_bucket.append(list(set([str(i["href"]) for i in raw_soup.find_all("a") if "/id/" in str(i)])))
        print("number of links in the bucket: " , len(links_bucket))
    return links_bucket                        

# This is going to take some time 
all_the_links = extract_links_from_urls(all_the_urls)

# This processes the raw html and get rid unwanted http links
# it doesn't take care of www links
def get_the_juice(url):
    req = requests.Session().get("http://www.instructables.com"+url)
    soup = BeautifulSoup(req.content, "lxml")
    #OLD: return [item.get_text() for item in soup.select("p")]
    # Questa espressione regolare aggiunta al vecchio comando (vedi sopra) elimina anche le url che vengono usate come testo degli oggetti >a>
    return [re.sub(r'https?:\/\/.*[\n\r\s]?','',item.get_text()) for item in soup.select("p")] 


