import os
import csv
import shutil

class copy_selected_foto:
    """
    This is testing
    """
    def __init__(self, location, substring, src_raw_foto, chunks_list_first):
        self.location = location
        self.substring = substring
        self.src_raw_foto = src_raw_foto
        self.chunks_list_first = chunks_list_first

    def copy_selected_foto(location, substring, src_raw_foto, chunks_list_first):
        rows_csv_merge = []
        for i in os.listdir(location):
            if i.find(substring) != -1:
                csv_reader = csv.reader(open(os.path.join(location,i)))
                header = next(csv_reader)

                for row in csv_reader:
                    rows_csv_merge.append(row)

        for i in range(len(src_raw_foto)):
            chunk_name_raw = (str(src_raw_foto[i].split("-")[0]))
            src_path_raw = (str(src_raw_foto[i].split("-")[1]))

            for chunk in chunks_list_first:
                    if chunk_name_raw == str(chunk):
                        for file_name in os.listdir(src_path_raw):
                            source = src_path_raw + "/" + file_name
                            for file in rows_csv_merge:
                                destination = location + "/" + file[0] + "/" + file[1] + "/" + file_name
                                if os.path.isfile(source) and (file_name == file[2] + ".jpg" or file_name == file[2] + ".JPG"):
                                    shutil.copy(source,destination)
                                    print("copied",file_name)