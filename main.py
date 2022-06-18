import os
import re
import pandas as pd


# Create a regex pattern to extract info from file names
# ?P<...> create named groups for help with retrieval

file_pattern = re.compile(r"^(.*?)_(?P<L1>.*?)_(?P<Topic>.*?)_(?P<ID>.*?)_(?P<Level>.*?).txt$")


file_paths = []
first_lang = []
topic = []
subj_id = []
level = []

essays = []


# The first file in ./Data is empty thus skipped
# Here, os.walk() method generates the file names (as strings) in the file index tree
# The method outputs a three-item tuple (root info, directories, and all files); hence, root, dirs, files

for root, dirs, files in os.walk("./Data/"):
    for name in files[1:]:
        fpath = os.path.join(root, name)
        file_paths.append(fpath)

        pattern = re.match(file_pattern, name)

        first_lang.append(pattern.group("L1"))
        topic.append(pattern.group("Topic"))
        subj_id.append(pattern.group("ID"))
        level.append(pattern.group("Level"))


# Read content of each file and append it to a list

for file in file_paths:
    with open(file=f"{file}", encoding="utf8") as text:
        raw_txt = text.read()
        essays.append(raw_txt)


df = pd.DataFrame(
    {
    'Subject_id': subj_id,
    'Topics': topic,
    'Levels_key': level,
    'L1s': first_lang,
    'Essays': essays,
    }
)

df.to_csv("Essays.csv", index=False)

# TODO: 1) Remove \ufeff at the beginning of each text (it's a space?)

