import requests
from util import log
import os
from time import sleep

class PyBridge:
    def __init__(self, domain=None) -> None:
        self.chunk = 1048576

        self.directory = "projects"
        self.username = "darkstartech"
        self.token = '2bf3a19829dede7c15ddc19b9fd2ad511fe328fe'

        self.directory = "hospital"
        self.username = "darksideapp"
        self.token = '7590f4acab3c6ff9bf5f3a57c3030ebf993e3bb8'


        if not domain:
            self.domain = f"{self.username}.pythonanywhere.com"
        else:
            self.domain = domain

        self.url = f"https://www.pythonanywhere.com/api/v0/user/{self.username}/files/path/home/{self.username}/{self.directory}/"
        self.base_url = f"https://www.pythonanywhere.com/api/v0/user/{self.username}/files/path/home/{self.username}/{self.directory}/"

        self.headers = {'Authorization': f'Token {self.token}'}
        
        self.ignore_file = [".pyc", "__pycache__", "admin"]

    def __webapps(self, opr="reload"):
        url = f"https://www.pythonanywhere.com/api/v0/user/{self.username}/webapps/{self.domain}/{opr}/"

        response = requests.post(url=url, headers=self.headers)
        if response.status_code == 200:
            return True
        
        log(f"Error Occured: status_ccode is {response.status_code}")
        return False

    def reload(self):
        status = self.__webapps()
        if status:
            log("---> Webapp reloaded")

    
    def disable(self):
        status = self.__webapps(opr="disable")
        if status:
            log("---> Webapp disabled")
    
    def enable(self):
        status = self.__webapps(opr="enable")
        if status:
            log("---> Webapp enabled")

    def save_file(self, path, response):
        with open(path, "wb") as tf:
            for chunk in response.iter_content(self.chunk):

                if chunk: # filter out keep-alive new chunks
                    tf.write(chunk)

            tf.close()
            log(f"File Downloaded : {os.path.basename(path)}")


    def get_response(self, url, json=True, check_status=200):
        response = requests.get(url, headers = self.headers)
        if response.status_code == check_status:
            if json:
                try:
                    return response.json()
                except:
                    return False
                
            return response
        
        return False
            

    def __download_url(self, url, save_path):
        json_data = self.get_response(url)
        if not json_data:
            log(f"ErrorInResponse..")
            return False
        
        for file in json_data:
            one_file = json_data[file]

            if one_file['type'] == 'file':
                if os.path.splitext(file)[1] in self.ignore_file:
                    continue

                url = one_file['url']

                response = self.get_response(url, json=False)
                path = f"{save_path}/{file}"
                self.save_file(path, response)


            elif one_file['type'] == 'directory':
                if file in self.ignore_file:
                    continue

                url = one_file['url']
                new_path = f"{save_path}/{file}"

                if not os.path.exists(new_path):
                    try:
                        os.mkdir(new_path)
                        log(f"**** Folder Created : {file} ****")

                    except:
                        log(f"Error in making file : {new_path}")
                        continue

                self.__download_url(url, new_path)

            else:
                print(f"Unkown File found : {file} : {one_file[file]}")

    
    def download(self, save_path, from_down_path = ''):
        # url = f"{self.url}{from_down_path}"
        if not os.path.exists(save_path):
            log(f"Invalid Path : {save_path}")
            return False
        
        self.__download_url(url, save_path)


    def post_file(self, url, path):
        # log(f"URl==> {url}")
        #open file to send....
        with open(path, "rb") as ff:
            response = requests.post(url, headers= self.headers, files= {'content': ff})
        
        if response.status_code == 201:
            log(f"FileCreated : {os.path.basename(path)}")

        elif response.status_code == 200:
            log(f"FileUpdated : {os.path.basename(path)}")

        elif response.status_code == 429:
            log(f"Rate Limit reached, waiting for one minute..")
            sleep(30)
            self.post_file(url, path)

        else :
            log(f"ErrorInUploading :- status : {response.status_code}")

    def __upload(self, project_path, base_path):
        #list files
        for file in os.listdir(project_path):
            path = f"{project_path}{file}"

            if os.path.isdir(path):
                if file in self.ignore_file:
                    continue

                self.upload(f"{path}/", f"{base_path}{file}/")

            elif os.path.isfile(path):

                if os.path.splitext(file)[1] in self.ignore_file:
                    continue

                url = f"{self.base_url}{base_path}{file}"
                self.post_file(url, path)
            
            else:
                log("Error: KnownFileTypeFound")



    def upload(self, project_path, base_path = None):
        if not os.path.exists(project_path):
            log(f"FileNotFoundError")
            return False
        
        if not base_path:
            base_path = ""
        
        self.__upload(project_path, base_path)
        

        

if __name__ == "__main__":
    git = PyBridge()

    # path = "c:/Users/darkw/Downloads/Project/"
    path = "C:/Users/darkw/OneDrive/Documents/mcare/"

    # git.download(path)
    git.upload(path)
    # git.enable()
    git.reload()

       
