import os
import csv
import shutil

class process_foto:
    """
    This is a function to generating 9 photos per each folder, please pass the params to process the function"""
    def __init__(self, location,chunk_shape_dictionary):
        self.location = location
        self.chunk_shape_dictionary = chunk_shape_dictionary

    def process_foto(location, chunk_shape_dictionary):
        path_new = []
        for key in chunk_shape_dictionary:
            path_new_append = str(location) + "/" + str(key) 
            path_new.append(path_new_append)
        
        path_new_2 = []
        for path in path_new:
            foldernames_2 = os.listdir(path)
            for folder in foldernames_2:
                path_new_2.append(str(path) + "/" + str(folder))
        
        arranged_dict = {}
        for path_foto in path_new_2:
            path_foto_arrange = []
            foldernames_3 = os.listdir(path_foto)
            if len(foldernames_3) > 0:
                folder_names_4 = foldernames_3[0:9]
                for file in folder_names_4:
                    path_foto_arrange.append(str(file))
                arranged_dict[path_foto] = path_foto_arrange
        
        path_raw = []
        list_b = []

        for folder, files in arranged_dict.items():
            path_raw.append(folder)
            for file in files:
                list_b.append(str(folder) + "/" + str(file))
        
        list_a = []
        for file in path_raw:
            for photo in os.listdir(file):
                list_a.append(str(file) + "/" + str(photo))
        
        def non_match_elements(list_a, list_b):
            non_match = []
            for i in list_a:
                if i not in list_b:
                    non_match.append(i)
            return non_match

        non_match = non_match_elements(list_a,list_b)

        for deleted in non_match:
            os.remove(deleted)
            print("Deleting File ", non_match)
        for (root,dirs,files) in os.walk(location):
            print(root)
