import os
import csv

class generate_log_raw_petak:
    """
    This is a function to generate new report that consist by 9 photos per shape, please pass the params to execute the function
    """
    def __init__(self,location,chunk_shape_dictionary):
        self.location = location
        self.chunk_shape_dictionary = chunk_shape_dictionary

    def generate_log_raw_petak(path_ekspor,chunk_shape_dictionary):
        path_new = []
        for key in chunk_shape_dictionary:
            path_new_append = str(path_ekspor) + "/" + str(key) 
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

        new_csv = []
        for l in list_b:
            get_csv = l.split("/")
            new_csv.append(get_csv[len(get_csv)-3:len(get_csv)])

        foldernames = os.listdir(path_ekspor)
        substring = "prioritas_ketiga"
        rows_csv_merge = []
        for i in foldernames:
            if i.find(substring) != -1:
                csv_reader = csv.reader(open(os.path.join(path_ekspor,i)))
                header = next(csv_reader)

                for row in csv_reader:
                    rows_csv_merge.append(row)
            
        with open(path_ekspor + "\\" + "Log Raw Petak.csv","w",newline="") as fp:
            a = csv.writer(fp,delimiter=",")
            fields=["Chunk Name","Keyid","Camera Name","Longitude","Latitude","Altitude","Longitude Accuracy", "Latitude Accuracy","Altitude Accuracy"]
            a.writerow(fields)

            for n in new_csv:
                chunk_new = n[0]
                shape_new = n[1]
                photo_new = n[2]
                for r in rows_csv_merge:
                    chunk_old = r[0]
                    shape_old = r[1]
                    photo_old = r[2]
                    long_old = r[3]
                    lat_old = r[4]
                    alt_old = r[5]
                    long_acc = r[6]
                    lat_acc = r[7]
                    alt_acc = r[8]
                    if chunk_new == chunk_old and shape_new == shape_old and (photo_new == (photo_old + ".jpg") or photo_new == (photo_old + ".JPG")):
                        a.writerow([chunk_old,shape_old,photo_old,long_old,lat_old,alt_old,long_acc,lat_acc,alt_acc])
    