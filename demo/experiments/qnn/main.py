import os
import numpy as np
import random

from qiskit_algorithms.optimizers import COBYLA
from qiskit.circuit.library import RealAmplitudes
from qiskit.primitives import Sampler
from qiskit_algorithms.utils import algorithm_globals

from qiskit_machine_learning.algorithms.classifiers import VQC

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

algorithm_globals.random_seed = 42
sampler1 = Sampler()
sampler2 = Sampler()

size_sample = 40
size_train = 30
size_test = size_sample - size_train
num_feature = 3

subarrays = []
for _ in range(size_sample):
    subarray_length = random.randint(num_feature, num_feature)
    subarray_values = np.random.randint(0, 100, subarray_length)
    subarrays.append(subarray_values)

features = np.array(subarrays)

labels = np.zeros_like(features)
max_values = np.max(features, axis=1)
max_indices = np.argmax(features, axis=1)

labels[np.arange(features.shape[0]), max_indices] = 1

features = MinMaxScaler().fit_transform(features)

train_features, test_features, train_labels, test_labels = train_test_split(
    features,
    labels,
    train_size=size_train,
    shuffle=False,
    random_state=algorithm_globals.random_seed,
)

train_flattened_features = train_features.flatten()
train_flattened_labels = train_labels.flatten()

test_flattened_features = test_features.flatten()
test_flattened_labels = test_labels.flatten()

maxiter = 20
objective_values = []

original_optimizer = COBYLA(maxiter=maxiter)

ansatz = RealAmplitudes(num_feature)
initial_point = np.asarray([0.5] * ansatz.num_parameters)

original_classifier = VQC(
    ansatz=ansatz,
    optimizer=original_optimizer,
    sampler=sampler1,
)

original_classifier.fit(train_features, train_labels)

print("Train score", original_classifier.score(train_features, train_labels))
print("Test score ", original_classifier.score(test_features, test_labels))

res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

original_classifier.save(os.path.join(res_path, "vqc_classifier.model"))

loaded_classifier = VQC.load(os.path.join(res_path, "vqc_classifier.model"))
loaded_classifier.warm_start = True
loaded_classifier.neural_network.sampler = sampler2
loaded_classifier.optimizer = COBYLA(maxiter=80)

loaded_classifier.fit(train_features, train_labels)

print("Train score", loaded_classifier.score(train_features, train_labels))
print("Test score", loaded_classifier.score(test_features, test_labels))

train_predicts = loaded_classifier.predict(train_features)
test_predicts = loaded_classifier.predict(test_features)

train_flattened_predicts = train_predicts.flatten()
test_flattened_predicts = test_predicts.flatten()

count_train = 0
count_test = 0
for train_predict, train_label, train_feat in zip(
    train_flattened_predicts, train_flattened_labels, train_flattened_features
):
    if not np.all(train_predict == train_label):
        index = np.where(train_flattened_features == train_feat)
        count_train += 1

for test_predict, test_label, test_feat in zip(
    test_flattened_predicts, test_flattened_labels, test_flattened_features
):
    if not np.all(test_predict == test_label):
        index = np.where(test_flattened_features == test_feat)
        count_test += 1

print("Error on train values : ", count_train)
print("Error on test values : ", count_test)
