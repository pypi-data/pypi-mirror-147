import os

class making_directory:
    """
    Pass the parameters
    """
    def __init__(self, location, chunks_list_first,dictionary):
        self.location = location
        self.chunks_list_first = chunks_list_first
        self.dictionary = dictionary

    def making_directory(location, chunks_list_first,dictionary):
        for items in chunks_list_first:
            path = os.path.join(location,items)
            os.mkdir(path)
            for key in dictionary:
                if items == key:
                    for values in dictionary[key]:
                        os.makedirs(os.path.join(path,values))
                        