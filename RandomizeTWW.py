import random
import csv
import numpy as np
import pickle

# Sample data
list1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,   0.105,1.4,0.105,0.105, 3.605,0.105,0.105,0.105,    0.105,0,0.105,0,    0,0,0.105,0,   0,0,0.105,0.105,    0,0,0,0.315,   0,0,0,0,    0,0,0.105,0,    0,0,0.105,0,  0,0,0.105,0,    0,0,0,0,     0.105,0.105,0.105,0,   0.105,0,0,0,    0,0,0.735,0,   3.605,0,0.105,0,    0,0,0,0, 0,0,0,0]
list3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,   25,40,25,25,           10,25,25,25,                25,0,25,0,          0,0,10,0,      0,0,25,25,          0,0,0,10,      0,0,0,0,    0,0,25,0,       0,0,25,0,     0,0,25,0,       0,0,0,0,     25,40,40,0,            25,0,0,0,       0,0,10,0,      10, 0, 25,0,        0,0,0,0, 0,0,0,0]
list2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,   25,40,25,25,           40,25,25,25,                25,0,25,0,          0,0,40,0,      0,0,25,25,          0,0,0,55,      0,0,0,0,    0,0,25,0,       0,0,25,0,     0,0,25,0,       0,0,0,0,     25,40,40,0,            25,0,0,0,       0,0,55,0,      40,0,10,0,          0,0,0,0, 0,0,0,0]
list4 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,   0.2,2.67,0.2,0.2,      6.87,0.2,0.2,0.2,         0.2,0,0.2,0,           0,0,0.2,0,    0,0,0.2,0.2,        0,0,0,3,       0,0,0,0,    0,0,0.2,0,        0,0,0.2,0,      0,0,0.2,0,        0,0,0,0,     0.2,0.13,0.13,0, 0.2,0,0,0,        0,0,0.93,0,       6.87,0,0.2,0,  0,0,0,0, 0,0,0,0]

#list2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,40,40,25,40,25,55,0,25,25,25,0,40,25,55,40,0,0]Tp
#list3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,40,10,25,10,25,10,0,25,25,25,0,40,25,10,10,0,0]Tm

print(sum(list1))
print(len(list2))
print(len(list3))
print(len(list4))

# Create a list of tuples where each tuple contains the corresponding elements from each list
original_data = list(zip(list1, list2, list3, list4))

# Keep the first 6 elements of each list fixed and shuffle the rest of the elements
fixed_data = list(zip(list1[:24], list2[:24], list3[:24], list4[:24]))
remaining_data = list(zip(list1[24:], list2[24:], list3[24:], list4[24:]))


# Create 12 different outcomes
for i in range(8):
    # Shuffle the remaining elements
    random.shuffle(remaining_data)

    # Combine the fixed and shuffled data to create the new data
    new_data = fixed_data + remaining_data

    with open(f"input_data/Medoid/TWW/outcome_{i + 1}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(new_data)


   # Print the new data
#    print(f"input_data/Medoid/TWW/Outcome {i + 1}: {new_data}")


#listTWWPower= [0,0,0,0,0,0,0,1.715,3.815,0.21,0.105,0.21,0.315,0,0.105,0.105,0.105,0,0.315,0.105,0.735,3.705,0,0,]

#delteTheta= [0,0,0,0,0,0,0,40,30,25,30,25,55,0,25,25,25,0,40,25,45,30,0,0]

#Tmin = [0,0,0,0,0,0,0,40,10,25,10,25,10,0,25,5,25,0,40,25,10,10,0,0]

#f = [0,0,0,0,0,0,0,15,16,6,9,6,4,0,3,3,3,0,9,3,4,10,0,0]


