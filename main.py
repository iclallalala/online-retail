import pandas as pd
import re

# Read in the data
data = pd.read_csv('data.tsv', sep='\t',encoding='latin-1')

# Define a function to clean the text
def clean_text(text):
    text = text.lower() # convert to lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text) # remove punctuation
    return text

# Apply the cleaning function to the text column
data['pathology_report_text'] = data['pathology_report_text'].apply(lambda x: clean_text(x))

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

# Define the maximum number of words to keep
num_words = 10000

# Create the tokenizer and fit on the text data
tokenizer = Tokenizer(num_words=num_words)
tokenizer.fit_on_texts(data['pathology_report_text'])

# Convert the text data to sequences
sequences = tokenizer.texts_to_sequences(data['pathology_report_text'])

# Pad the sequences to the same length
padded_sequences = pad_sequences(sequences)


from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense

# Read in the training data
train = pd.read_csv('train.csv')

# Define the model
model = Sequential()
model.add(Embedding(input_dim=num_words, output_dim=100, input_length=padded_sequences.shape[1]))
model.add(LSTM(units=100, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(4, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(padded_sequences, train[['G1', 'G2', 'G3', 'G4']])


# Read in the test data
test = pd.read_csv('test.csv')

# merge test data with the data containing the pathology_report_text
test = pd.merge(test, data, on='pateint_id')

# Convert the test data to sequences
test_sequences = tokenizer.texts_to_sequences(test['pathology_report_text'])

# Pad the test sequences
test_padded_sequences = pad_sequences(test_sequences)

# Predict the Fuhrman grades for the test set
test_predictions = model.predict(test_padded_sequences)

# Create a dataframe with the patient_id and predictions
submission = pd.DataFrame({'pateint_id': test['pateint_id'],
                           'likelihood_G1': test_predictions[:, 0],
                           'likelihood_G2': test_predictions[:, 1],
                           'likelihood_G3': test_predictions[:, 2],
                           'likelihood_G4': test_predictions[:, 3]})

# Save the submission dataframe to a csv file
submission.to_csv('submission.csv', index=False)
