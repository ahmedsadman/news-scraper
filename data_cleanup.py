import os
import re
import string
import csv

def cleanup(content, seperator=" "):
    # remove emails or website links
    # content = re.sub(r'^https?:\/\/.*[\r\n]*', '', content, flags=re.MULTILINE)
    content = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', content)
    content = re.sub(r'\S+@\S+', '', content, flags=re.MULTILINE)

    # remove english
    filtered = filter(lambda x: x == " " or x in string.punctuation or x not in string.printable, content)
    joined = "".join(list(filtered))

    # remove multiple whitespace
    splitted = joined.split()
    return seperator.join(splitted)

def get_cleaned_data(file):
    '''return the cleaned up data as csv rows'''
    with open(file, "r", encoding="utf-8", newline="\n") as fstream:
        csv_reader = csv.reader(fstream, delimiter=",")
        line_count = 0
        rows = []
        for row in csv_reader:
            if line_count == 0:
                rows.append(["title", "content", "tags"])
                line_count += 1
                continue

            row[0] = cleanup(row[0]) # title
            row[1] = cleanup(row[1]) # content
            row[2] = cleanup(row[2], ",") # tags

            rows.append([row[0], row[1], row[2]])
        return rows

def write_clean_data(file, rows):
    '''write the clean data in csv file'''
    with open(file, "w", encoding="utf-8", newline="\n") as fstream:
        csv_writer = csv.writer(fstream, delimiter=",")
        csv_writer.writerows(rows)

def batch_data_cleanup():
    files = os.listdir('.')
    
    for file in files:
        if not ".csv" in file:
            continue
        rows = get_cleaned_data(file)
        write_clean_data(file, rows)
        

if __name__ == "__main__":
    batch_data_cleanup()
    print("-- CLEANUP COMPLETE --")