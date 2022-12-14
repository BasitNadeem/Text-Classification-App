#Import Libraries
import numpy as np, pandas as pd, re
import fasttext

#Training Data Prep.
train_data = pd.read_csv("train_data.txt", sep=" :::", header=None, engine="python")
train_data.columns = ['Id', 'Title', 'Genre', 'Desc.']
train_data.drop(['Id', 'Desc.'], axis=1, inplace=True)

#Test Data Prep.
test_data = pd.read_csv("test_data_solution.txt", sep=" :::", header=None, names=['Id', 'Title', 'Genre', 'Desc.'], engine="python")
test_data.drop(['Id', 'Desc.'], axis=1, inplace=True)

#Function for Data Preprocessing
def Preprocess_Data(train, test):
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

        train['Title'] = train.Title.apply(process_title)
        test['Title'] = test.Title.apply(process_title)

        train["Genre"] = train["Genre"].apply(process_title)
        test["Genre"] = test["Genre"].apply(process_title)
        
        train.iloc[:, 1] = train.iloc[:, 1].apply(lambda x: '__label__' + x)
        test.iloc[:, 1] = test.iloc[:, 1].apply(lambda x: '__label__' + x)

        return train, test

#Fucntion for creating processed data files 
def Create_Datafile(training_file, test_file):
        training_file[['Genre', 'Title']].to_csv('train.txt', 
                                                index = False, 
                                                sep = ' ',
                                                header = None, 
                                                escapechar = " ")


        test_file[['Genre','Title']].to_csv('test.txt', 
                                        index = False, 
                                        sep = ' ',
                                        header = None, 
                                        escapechar = " ")
        
        return training_file, test_file

#Function for Training & Saving Model
def Classification_Model():
        model = fasttext.train_supervised('train.txt', lr=1.0, epoch=25, wordNgrams=2, bucket=200000, dim=50, loss='hs')
        model.test('test.txt')
        model.save_model('model.bin')
        return model


Preprocess_Data(train_data, test_data)
Create_Datafile(train_data, test_data)
Classification_Model()



