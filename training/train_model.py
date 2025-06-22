from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import csv
import numpy as np

x_train = []
y_train = []

def dataCollect(filename, label):
    with open(filename, newline='') as csvfile:
        feuilledata = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in feuilledata:
            data = ', '.join(row)
            data = data.split(',')
            dataFloat = []
            for d in data:
                dataFloat.append(float(d))
            #print(dataFloat)
            x_train.append(dataFloat)
            y_train.append(label)

dataCollect('data/feuille_data.csv','feuille')
dataCollect('data/pierre_data.csv','pierre')
dataCollect('data/ciseau_data.csv','ciseau')

label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(y_train)

x_train, x_test, y_train, y_test = train_test_split(
    x_train, y_train, test_size=0.2, random_state=42, stratify=y_train
)

x_train = np.array(x_train)
y_train = np.array(y_train)
x_test = np.array(x_test)
y_test = np.array(y_test)

model = keras.Sequential([
    layers.Dense(1024, activation='relu', input_shape=[63]),
    layers.Dropout(0.3),
    layers.BatchNormalization(),
    layers.Dense(1024, activation='relu'),
    layers.Dropout(0.3),
    layers.BatchNormalization(),
    layers.Dense(1024, activation='relu'),
    layers.Dropout(0.3),
    layers.BatchNormalization(),
    layers.Dense(3, activation='softmax'),
])
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',  # ← adaptée à des labels entiers (0,1,2)
    metrics=['accuracy']                     # ← pour afficher l'accuracy
)
history = model.fit(
    x_train, y_train,
    #batch_size=256,
    epochs=100,
    verbose=1,
    validation_data=(x_test, y_test)
)

# Évaluation sur les données de test
loss, accuracy = model.evaluate(x_test, y_test)
print(f"✅ Test accuracy: {accuracy:.2%}")