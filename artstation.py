import re
import json
import requests
import math
import os
from multiprocessing import Pool

requests.packages.urllib3.disable_warnings()

#artist to download from
username="lownine"



class Artstation():
    def __init__(self):
        self.urlbase="https://www.artstation.com/users/{0}/likes.json?page=".format(username)
	#makes a download folder
        if not os.path.exists('Downloads'):
            os.mkdir('Downloads')
        self.get_project_url()
            
    def get_project_url(self):
        self.randombase="https://www.artstation.com/users/{0}/random_projects.json?project_id={1}"
        self.sess = requests.Session()
	#prepare headers
        #set this to your cookies
        cookies={}
        self.sess.headers.update(cookies)
        self.sess.headers.update({'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"})
            
        request = self.sess.get(self.urlbase, verify=False)
        data = request.json()
		#obtains the number of likes from the json 
        number_likes=data['total_count']
        number_on_page=len(data['data'])
        number_pages_to_parse=math.ceil(number_likes/number_on_page)
        
	#go through all the likes and obtain the image urls
        for pages in range(number_pages_to_parse):
            page_request_data=self.sess.get(self.urlbase+str(pages), verify=False).json()['data']
            for like in page_request_data:
                artwork_link=like['permalink']
                images = self.sess.get((artwork_link), verify=False).text
                images=re.findall("(?<=\"image_url\\\\.:\\\\\").*?\.jpg", images)
				#if there are multiple images download them simultaneously
                if len(images)>0:
                    p=Pool(len(images))
                    p.map(self.download, images)
                    p.terminate()
                    p.join()
                
    #downloads obtained images and saves them to the Downloads folder
    def download(self, image):
        filename=image.split("/")[-1]
        if not os.path.exists(os.path.join('Downloads', filename)):
            image_download=self.sess.get(image, verify=False)
            with open(os.path.join('Downloads', filename),"wb") as filename:
                filename.write(image_download.content)
if __name__ == '__main__':
    art=Artstation()
    
