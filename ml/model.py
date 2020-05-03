# Most of this code is from https://www.datatechnotes.com/2019/06/text-classification-example-with-keras.html, modified by me.
# I give most of the credit for this to whoever wrote that tutorial. 
#
#Team 25 YouthVSCovid API - model.py - machine learning model for non-covid news
#Copyright (C) 2020 arthomnix
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published
#by the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, load_model
from keras import layers
from sklearn.model_selection import train_test_split
import pandas as pd

# read data.csv
df = pd.read_csv('data.csv')
df.columns = ["label","text"]
x = df['text'].values
y = df['label'].values
tokenizer = Tokenizer(num_words=500)
tokenizer.fit_on_texts(x)

maxlen = 10

def trainModel(epochs=5, maxlen=maxlen):
    """ Train model using datset from data.csv"""


    # split data into training / testing datasets
    x_train, x_test, y_train, y_test = \
     train_test_split(x, y, test_size=0.1, random_state=123)

    # Convert data into token vectors - ML models can't understand words!
    xtrain= tokenizer.texts_to_sequences(x_train)
    xtest= tokenizer.texts_to_sequences(x_test)
    xtrain=pad_sequences(xtrain,padding='post', maxlen=maxlen)
    xtest=pad_sequences(xtest,padding='post', maxlen=maxlen)
    # Define the model
    embedding_dim=50
    vocab_size=500
    model=Sequential()
    model.add(layers.Embedding(input_dim=vocab_size,
          output_dim=embedding_dim,
          input_length=maxlen))
    model.add(layers.LSTM(units=50,return_sequences=True))
    model.add(layers.LSTM(units=10))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(8))
    model.add(layers.Dense(1, activation="sigmoid"))
    model.compile(optimizer="adam", loss="binary_crossentropy", 
         metrics=['accuracy'])

    # Actually train the model
    model.fit(xtrain,y_train, epochs=epochs, batch_size=16, verbose=False)
    # Save the model to disk so we don't have to train every time
    model.save('model.h5')
    del model

def predictCoronaArticle(text, maxlen=maxlen):
    model = load_model('model.h5')
    textt = pad_sequences(tokenizer.texts_to_sequences([text]), padding='post', maxlen=maxlen)
    ypred = model.predict(textt)
    ypred[ypred>0.25]=1
    ypred[ypred<=0.25]=0
    return int(ypred[0])


