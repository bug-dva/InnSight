file_list = []
fh = open("filelist.txt", "r")
for line in fh.readlines():
    line = line.strip()
    line_url = 's3n://airbnbdataset/allcsvfile/'+str(line)
    file_list.append(line_url)
print(file_list)
