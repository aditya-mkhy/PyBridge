import json
import time
import os
from util import log

class DB:
    def __init__(self, file) -> None:
        self.file = file
        if not os.path.exists(self.file):
            self.__init_file__()
        
        self.load()
        

    def __read(self) -> dict:
        with open(self.file, "r") as ff:
            dump_data = ff.read()

        try:
            return json.loads(dump_data)
        
        except Exception as e:
            log(f"ErrorInLoding : {e}")
            return False
        

    def load(self) -> dict:
        self.data = self.__read()
        
        if self.data == False:
            log("File is initialised as data is not loded due to some error")
            self.__init_file__()
            self.data = {}
            return False
        
        #data is loaded successfully......
        return True
      
    def get_data(self):
        return self.__read()


    def __write(self, data):
        with open(self.file, "w") as tf:
            tf.write(data)
            
        return True

    def commit(self):
        self.__write( json.dumps(self.data) )

    def __init_file__(self):
        # data = {
        #     "file" : {
        #         "modified" : time.time(),
        #         "updated" : time.time(),
        #         "size" : time.time(),
        #     }
        # }
        jason_data = json.dumps({})
        self.__write(jason_data)
        return True


if __name__ == "__main__":
    file = "./db.if"
    database = DB(file)
    print(database.data)
