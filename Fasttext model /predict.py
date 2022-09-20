import fasttext

try:
    # silences warnings as the package does not properly use the python 'warnings' package
    # see https://github.com/facebookresearch/fastText/issues/1056
    fasttext.FastText.eprint = lambda *args,**kwargs: None
except:
    pass

#Loading trained model 
model = fasttext.load_model("model.bin")

#Function for prediction
def predict(title):
    print(model.predict(title))
    return 

#title1 = input("Please Enter movie name: ")
#predict(title1)

predict("Oscar  et  la  dame  rose")

