input_file = open('./input.txt','r')

parsed_file = input_file.readline()


# part 1

layers = []
i = 0
layer_size = 25*6
while i < len(parsed_file)-1:
    layers.append([int(x) for x in parsed_file[i: i+layer_size]])
    i += layer_size

layers = layers[:-1]

from collections import Counter
import numpy as np
np.set_printoptions(formatter={'all':lambda x: ' ' if x==0 else 'x'})

counts = [Counter(layer) for layer in layers]
max_zeroes = np.argmin([x[0] for x in counts])
print(counts[max_zeroes][1] * counts[max_zeroes][2])

# part 2
final_layer = np.empty(layer_size)
final_layer[:] = 2
for layer in layers:
    temp_layer = [int(x) for x in list(layer)]
    final_layer = np.where(final_layer == 2, temp_layer, final_layer)

x = np.reshape(final_layer, (25, 6)).T
print(x)
