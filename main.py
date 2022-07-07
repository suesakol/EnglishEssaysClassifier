import os
import re
import pandas as pd
import spacy


# After importing spacy, create an instance of Language class, named "nlp" by convention

nlp = spacy.load("en_core_web_md")

# Create a regex pattern to extract info from file names
# ?P<...> create named groups for help with retrieval

file_pattern = re.compile(r"^(.*?)_(?P<L1>.*?)_(?P<Topic>.*?)_(?P<ID>.*?)_(?P<Level>.*?).txt$")

file_paths = []
file_names = []
first_lang = []
topic = []
subj_id = []
level = []

essays = []


# The first file in ./Data is empty thus skipped
# Here, os.walk() method generates file names (as strings) in the file index tree
# The method outputs a three-item tuple (root info, directories, and all files); hence, root, dirs, files

for root, dirs, files in os.walk("./Data/"):
    for name in files:
        if name == ".DS_Store":
            pass
        else:
            fpath = os.path.join(root, name)
            file_names.append(name)
            file_paths.append(fpath)

            pattern = re.match(file_pattern, name)

            first_lang.append(pattern.group("L1"))
            topic.append(pattern.group("Topic"))
            subj_id.append(pattern.group("ID"))
            level.append(pattern.group("Level"))


# Read content of each file and append it to a list
# Each text begins with "\ufeff" which is an encoding format
# Provide Python with the right encoding to remove it

file_num = 0

for file in file_paths:
    with open(file=f"{file}", encoding="utf-8-sig") as text:
        txt = text.read()
        raw_txt = txt.strip()
        essays.append(raw_txt)
        file_num += 1
print(f"Total files read: {file_num}")


# Create a data frame

df = pd.DataFrame(
    {
        'file_name': file_names,
        'subject_id': subj_id,
        'topic': topic,
        'levels_key': level,
        'first_lang': first_lang,
        'essay': essays,
    }
)


# NLP pipeline: tokenization, pos-tagging, syntactic analysis

docs = list(nlp.pipe(df.essay))


# Append to the data frame

df = pd.concat([
    df,
    pd.DataFrame(
        {
            'token': [[token.text for token in doc] for doc in docs],
            'pos': [[token.pos_ for token in doc] for doc in docs],
            'token_pos': [[(token.text, token.pos_) for token in doc] for doc in docs],
            'dep': [[token.dep_ for token in doc] for doc in docs],
            'token_dep': [[(token.text, token.dep_) for token in doc] for doc in docs],
            'sentence': [[s.text for s in doc.sents] for doc in docs],
            'word_length': [len([token.is_alpha for token in doc if token.is_alpha]) for doc in docs],
            'sentence_length': [len([s.text for s in doc.sents]) for doc in docs],
        }
    )], axis=1
)


# Save the data frame to a csv file

df.to_csv("Essays.csv", index=False)


# Iterate through a data frame and select columns into a dict
# nato_dict = {row.letter: row.code for (index, row) in df.iterrows()}