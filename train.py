import numpy as np, pandas as pd, re
import fasttext

train_data = pd.read_csv("train_data.txt", sep=" :::", header=None, engine="python")
train_data.columns = ['Id', 'Title', 'Genre', 'Desc.']
train_data.drop(['Id', 'Desc.'], axis=1, inplace=True)
#train_data.head()

test_data = pd.read_csv("test_data_solution.txt", sep=" :::", header=None, names=['Id', 'Title', 'Genre', 'Desc.'], engine="python")
test_data.drop(['Id', 'Desc.'], axis=1, inplace=True)
#test_data.head()

def process_title(title):
     """
     function that extracts characters and numbers
     from strings.

     input:
             title: string value

     output:
             title: cleaned string value
     """
     punc = '''!()-[]{};:'"\,<>./?@#$%^&*_“.|"'''

     for ele in punc:
         if ele in title:
             title = title.replace(ele, "")
     # strip away numbers and parenthesis
     title = (
         title.replace("(", "")
         .replace(")", "")
         .replace("/", "")
         .replace("_", "")
         .replace("-", "")
         .replace("&", "")
         .replace(":", "")
         .replace("@", "")
     )
     title = re.sub(r"\d+", "", title)
     title = title.replace("?", "")
     # strip away "part" word
     title = re.sub(r"[Pp]art", "", title)
     # strip II and III and IV
     title = title.replace("II", "").replace("III", "").replace("IV", "")
     title = title.strip()
     title = re.sub(" +", " ", title)

     return title

train_data['Title'] = train_data.Title.apply(process_title)

train_data["Genre"] = train_data["Genre"].apply(process_title)
test_data["Genre"] = test_data["Genre"].apply(process_title)

train_data.iloc[:, 1] = train_data.iloc[:, 1].apply(lambda x: '__label__' + x)

test_data.iloc[:, 1] = test_data.iloc[:, 1].apply(lambda x: '__label__' + x)


train_data[['Genre', 'Title']].to_csv('train.txt', 
                                          index = False, 
                                          sep = ' ',
                                          header = None, 
                                          #quoting = csv.QUOTE_NONE, 
                                          #quotechar = "", 
                                          escapechar = " ")


test_data[['Genre','Title']].to_csv('test.txt', 
                                     index = False, 
                                     sep = ' ',
                                     header = None, 
                                     #quoting = csv.QUOTE_NONE, 
                                     #quotechar = "", 
                                     escapechar = " ")

model = fasttext.train_supervised('train.txt', autotuneValidationFile= 'test.txt')

model.test('test.txt') 

model.save_model('model.bin')
