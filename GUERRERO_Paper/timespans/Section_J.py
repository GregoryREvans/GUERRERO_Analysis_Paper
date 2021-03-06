import abjad
import itertools
import os
import pathlib
import time
import abjadext.rmakers
from MusicMaker import MusicMaker
from AttachmentHandler import AttachmentHandler
from random import random
from random import seed
from evans.abjad_functions.talea_timespan.timespan_functions import make_showable_list as make_showable_list

print('Interpreting file ...')

# Define the time signatures we would like to apply against the timespan structure.

time_signatures = [
    abjad.TimeSignature(pair) for pair in [
        (4, 4), (4, 4), (4, 4), (4, 4), (4, 4),
        (4, 4), (9, 8),
        # (4, 4), (4, 4), (4, 4),
        # (4, 4), (4, 4), (4, 4), (4, 4), (4, 4),
        # (4, 4), (4, 4), (4, 4), (4, 4), (4, 4),
        # (4, 4), (4, 4), (4, 4), (4, 4), (4, 4),
    ]
]

bounds = abjad.mathtools.cumulative_sums([_.duration for _ in time_signatures])

#Define Pitch Material

def cyc(lst):
    count = 0
    while True:
        yield lst[count%len(lst)]
        count += 1

def grouper(lst1, lst2):
    def cyc(lst):
        c = 0
        while True:
            yield lst[c%len(lst)]
            c += 1
    lst1 = cyc(lst1)
    return [next(lst1) if i == 1 else [next(lst1) for _ in range(i)] for i in lst2]

def reduceMod(list_length, rw):
    return [(x % list_length) for x in rw]


sopranino_note = [27, 17, 8, 0, 11, ]
soprano_1_note = [22, 16, 13, ]
soprano_2_note = [16, 13, 14, 13, ]
soprano_3_note = [13, 12, 13, 16, 26 ]
alto_1_note = [20, 12, 23, ]
alto_2_note = [12, 1, 12, 23, ]
alto_3_note = [1, 23, 1, 12, ]
alto_4_note = [20, 12, 20, 23, ]
alto_5_note = [12, 20, 1, 23, ]
alto_6_note = [1, 20, 12, ]
tenor_1_note = [17, -1, 25, 6,]
tenor_2_note = [6, 25, 17,]
tenor_3_note = [-1, 6, 17, 25, ]
tenor_4_note = [17, -1, 6, ]
tenor_5_note = [6, 25, 17, ]
baritone_1_note = [13, 24, 13, 6, ]
baritone_2_note = [6, 24, 13, 4, ]
baritone_3_note = [4, 13, 6, 24, ]
bass_1_note = [9, 11, 11, 9, 11, ]
bass_2_note = [11, 9, 9, 11, 9, ]
contrabass_note = [-2, 2, 7, -2, 2, 7, 2, -2, ]


# -3 at bottom of chord for completion
sopranino_chord = [17, 27, 11, 0, 8,]
soprano_1_chord = [22, [13.25, 16, 26.25, ], 16, [13.25, 16, 26.25, ], 13, [13.25, 16, 26.25, ], ]
soprano_2_chord = [16, [13, 14.75, 26.25, ], 13, [13, 14.75, 26.25, ], 14, [13, 14.75, 26.25, ], 13, [13, 14.75, 26.25, ], ] #maybe it's 13.25?
soprano_3_chord = [13, [12.75, 15.5, 26, ], 13, 12, [12.75, 15.5, 26, ], 16, [12.75, 15.5, 26, ], 26 ]
alto_1_chord = [20, [12.5, 19, 27.75, 34, ], 12, [12.5, 19, 27.75, 34, ], 23, ]
alto_2_chord = [12, [12.5, 15.25, 25.5, ], 1, [12.5, 15.25, 25.5, ], 12, [12.5, 15.25, 25.5, ], 23, ]
alto_3_chord = [1, [1.75, 13.5, 22.25, 27, 30, ], 23, [1.75, 13.5, 22.25, 27, 30, ], 1, [1.75, 13.5, 22.25, 27, 30, ], 12, [1.75, 13.5, 22.25, 27, 30, ], ]
alto_4_chord = [20, [12.5, 15.25, 25.5, ], 12, [12.5, 15.25, 25.5, ], 20, [12.5, 15.25, 25.5, ], 23, ]
alto_5_chord = [12, [1.75, 13.5, 22.25, 27, 30, ], 20, 1, [1.75, 13.5, 22.25, 27, 30, ], 23, [1.75, 13.5, 22.25, 27, 30, ], ]
alto_6_chord = [1, [12.5, 19, 27.75, 34, ], 20, 12, [12.5, 19, 27.75, 34, ], ]
tenor_1_chord = [17, [6, 17.5, ], -1, 25, [6, 17.5, ], 6, [6, 17.5, ],]
tenor_2_chord = [6, [6, 17.5, 25.5, 30, ], 25, [6, 17.5, 25.5, 30, ], 17,]
tenor_3_chord = [-1, [6, 17.5, 25.5, 30.75, ], 6, [6, 17.5, 25.5, 30.75, ], 17, [6, 17.5, 25.5, 30.75, ], 25, [6, 17.5, 25.5, 30.75, ], ]
tenor_4_chord = [17, [6, 17.5, ], -1, [6, 17.5, ], 6, [6, 17.5, ],]
tenor_5_chord = [6, [6, 17.5, 25.5, 30.75, ], 25, [6, 17.5, 25.5, 30.75, ], 17, [6, 17.5, 25.5, 30.75, ], ]
baritone_1_chord = [13, [13.25, 27.5, 33.75, ], 24, [13.25, 27.5, 33.75, ], 13, [13.25, 27.5, 33.75, ], 6, [13.25, 27.5, 33.75, ],]
baritone_2_chord = [6, [4, 16.5, 23.5, ], 24, 13, [4, 16.5, 23.5, ], 4, ]
baritone_3_chord = [4, [7.75, 17.75, 25.5, 34, ], 13, [7.75, 17.75, 25.5, 34, ], 6, [7.75, 17.75, 25.5, 34, ], 24, [7.75, 17.75, 25.5, 34, ], ]
bass_1_chord = [11, 18, 9, 11, 0, ]
bass_2_chord = [9, 11, 0, 11, 9, 18, ]
contrabass_chord = [-2, 7, 2, 16, 7, 18, 16, 25, 16, ]

def reduceMod(x, rw):
    return [(y % x) for y in rw]

seed(22)
sopranino_random_walk = []
sopranino_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = sopranino_random_walk[i-1] + movement
    sopranino_random_walk.append(value)
    sopranino_walk_chord = [18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, ]
l = len(sopranino_walk_chord)
sopranino_random_walk_notes = [sopranino_walk_chord[x] for x in reduceMod(l, sopranino_random_walk)]

seed(23)
soprano_1_random_walk = []
soprano_1_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = soprano_1_random_walk[i-1] + movement
    soprano_1_random_walk.append(value)
soprano_1_walk_chord = [17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, ]
l = len(soprano_1_walk_chord)
soprano_1_random_walk_notes = [soprano_1_walk_chord[x] for x in reduceMod(l, soprano_1_random_walk)]

seed(24)
soprano_2_random_walk = []
soprano_2_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = soprano_2_random_walk[i-1] + movement
    soprano_2_random_walk.append(value)
soprano_2_random_walk.append(value)
soprano_2_walk_chord = [16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, ]
l = len(soprano_2_walk_chord)
soprano_2_random_walk_notes = [soprano_2_walk_chord[x] for x in reduceMod(l, soprano_2_random_walk)]

seed(25)
soprano_3_random_walk = []
soprano_3_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = soprano_3_random_walk[i-1] + movement
    soprano_3_random_walk.append(value)
soprano_3_random_walk.append(value)
soprano_3_walk_chord = [15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, ]
l = len(soprano_3_walk_chord)
soprano_3_random_walk_notes = [soprano_3_walk_chord[x] for x in reduceMod(l, soprano_3_random_walk)]

seed(26)
alto_1_random_walk = []
alto_1_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = alto_1_random_walk[i-1] + movement
    alto_1_random_walk.append(value)
alto_1_walk_chord = [14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, ]
l = len(alto_1_walk_chord)
alto_1_random_walk_notes = [alto_1_walk_chord[x] for x in reduceMod(l, alto_1_random_walk)]

seed(27)
alto_2_random_walk = []
alto_2_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = alto_2_random_walk[i-1] + movement
    alto_2_random_walk.append(value)
alto_2_walk_chord = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, ]
l = len(alto_2_walk_chord)
alto_2_random_walk_notes = [alto_2_walk_chord[x] for x in reduceMod(l, alto_2_random_walk)]

seed(28)
alto_3_random_walk = []
alto_3_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = alto_3_random_walk[i-1] + movement
    alto_3_random_walk.append(value)
alto_3_walk_chord = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, ]
l = len(alto_3_walk_chord)
alto_3_random_walk_notes = [alto_3_walk_chord[x] for x in reduceMod(l, alto_3_random_walk)]

seed(29)
alto_4_random_walk = []
alto_4_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = alto_4_random_walk[i-1] + movement
    alto_4_random_walk.append(value)
alto_4_walk_chord = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ]
l = len(alto_4_walk_chord)
alto_4_random_walk_notes = [alto_4_walk_chord[x] for x in reduceMod(l, alto_4_random_walk)]

seed(30)
alto_5_random_walk = []
alto_5_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = alto_5_random_walk[i-1] + movement
    alto_5_random_walk.append(value)
alto_5_walk_chord = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ]
l = len(alto_5_walk_chord)
alto_5_random_walk_notes = [alto_5_walk_chord[x] for x in reduceMod(l, alto_5_random_walk)]

seed(31)
alto_6_random_walk = []
alto_6_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = alto_6_random_walk[i-1] + movement
    alto_6_random_walk.append(value)
alto_6_walk_chord = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, ]
l = len(alto_6_walk_chord)
alto_6_random_walk_notes = [alto_6_walk_chord[x] for x in reduceMod(l, alto_6_random_walk)]

seed(32)
tenor_1_random_walk = []
tenor_1_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = tenor_1_random_walk[i-1] + movement
    tenor_1_random_walk.append(value)
tenor_1_walk_chord = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, ]
l = len(tenor_1_walk_chord)
tenor_1_random_walk_notes = [tenor_1_walk_chord[x] for x in reduceMod(l, tenor_1_random_walk)]

seed(33)
tenor_2_random_walk = []
tenor_2_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = tenor_2_random_walk[i-1] + movement
    tenor_2_random_walk.append(value)
tenor_2_walk_chord = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, 3, 4, 5, 6, ]
l = len(tenor_2_walk_chord)
tenor_2_random_walk_notes = [tenor_2_walk_chord[x] for x in reduceMod(l, tenor_2_random_walk)]

seed(34)
tenor_3_random_walk = []
tenor_3_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = tenor_3_random_walk[i-1] + movement
    tenor_3_random_walk.append(value)
tenor_3_walk_chord = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, 3, 4, 5, ]
l = len(tenor_3_walk_chord)
tenor_3_random_walk_notes = [tenor_3_walk_chord[x] for x in reduceMod(l, tenor_3_random_walk)]

seed(35)
tenor_4_random_walk = []
tenor_4_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = tenor_4_random_walk[i-1] + movement
    tenor_4_random_walk.append(value)
tenor_4_walk_chord = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, 3, 4, ]
l = len(tenor_4_walk_chord)
tenor_4_random_walk_notes = [tenor_4_walk_chord[x] for x in reduceMod(l, tenor_4_random_walk)]

seed(36)
tenor_5_random_walk = []
tenor_5_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = tenor_5_random_walk[i-1] + movement
    tenor_5_random_walk.append(value)
tenor_5_walk_chord = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, 3, ]
l = len(tenor_5_walk_chord)
tenor_5_random_walk_notes = [tenor_5_walk_chord[x] for x in reduceMod(l, tenor_5_random_walk)]

seed(37)
baritone_1_random_walk = []
baritone_1_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = baritone_1_random_walk[i-1] + movement
    baritone_1_random_walk.append(value)
baritone_1_walk_chord = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, 2, ]
l = len(baritone_1_walk_chord)
baritone_1_random_walk_notes = [baritone_1_walk_chord[x] for x in reduceMod(l, baritone_1_random_walk)]

seed(38)
baritone_2_random_walk = []
baritone_2_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = baritone_2_random_walk[i-1] + movement
    baritone_2_random_walk.append(value)
baritone_2_walk_chord = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, 1, ]
l = len(baritone_2_walk_chord)
baritone_2_random_walk_notes = [baritone_2_walk_chord[x] for x in reduceMod(l, baritone_2_random_walk)]

seed(39)
baritone_3_random_walk = []
baritone_3_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = baritone_3_random_walk[i-1] + movement
    baritone_3_random_walk.append(value)
baritone_3_walk_chord = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, 0, ]
l = len(baritone_3_walk_chord)
baritone_3_random_walk_notes = [baritone_3_walk_chord[x] for x in reduceMod(l, baritone_3_random_walk)]

seed(40)
bass_1_random_walk = []
bass_1_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = bass_1_random_walk[i-1] + movement
    bass_1_random_walk.append(value)
bass_1_walk_chord = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -1, ]
l = len(bass_1_walk_chord)
bass_1_random_walk_notes = [bass_1_walk_chord[x] for x in reduceMod(l, bass_1_random_walk)]

seed(41)
bass_2_random_walk = []
bass_2_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = bass_2_random_walk[i-1] + movement
    bass_2_random_walk.append(value)
bass_2_walk_chord = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, ]
l = len(bass_2_walk_chord)
bass_2_random_walk_notes = [bass_2_walk_chord[x] for x in reduceMod(l, bass_2_random_walk)]

seed(42)
contrabass_random_walk = []
contrabass_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = contrabass_random_walk[i-1] + movement
    contrabass_random_walk.append(value)
contrabass_walk_chord = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, ]
l = len(contrabass_walk_chord)
contrabass_random_walk_notes = [contrabass_walk_chord[x] for x in reduceMod(l, contrabass_random_walk)]

# Define rhythm-makers: two to be sued by the MusicMaker, one for silence.

rmaker_one = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(
        counts=[3, 2, 5, 2, 3, 1, 3, 2, 3, 1, 2, ],
        denominator=8,
        ),
    beam_specifier=abjadext.rmakers.BeamSpecifier(
        beam_divisions_together=True,
        beam_rests=False,
        ),
    extra_counts_per_division=[1, 0, -1, 1, -1, 0, 1, ],
    logical_tie_masks=[
        abjadext.rmakers.silence([3], 4),
        ],
    # division_masks=[
    #     abjadext.rmakers.SilenceMask(
    #         pattern=abjad.index([1], 5),
    #         ),
    #     ],
    tuplet_specifier=abjadext.rmakers.TupletSpecifier(
        trivialize=True,
        extract_trivial=True,
        rewrite_rest_filled=True,
        rewrite_sustained=True,
        ),
    )

rmaker_two = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(
        counts=[1, 1, 3, 1, 5, 5, 3, 1, 1, 3, 1, 3, 3, 1, 3, 7, 1, 6, 1, 3, ],
        denominator=8,
        ),
    beam_specifier=abjadext.rmakers.BeamSpecifier(
        beam_divisions_together=True,
        beam_rests=False,
        ),
    extra_counts_per_division=[-1, 0, 1, -1, 1, 0, ],
    logical_tie_masks=[
        abjadext.rmakers.silence([4, 8, ], 9),
        ],
    # division_masks=[
    #     abjadext.rmakers.SilenceMask(
    #         pattern=abjad.index([0], 7),
    #         ),
    #     ],
    tuplet_specifier=abjadext.rmakers.TupletSpecifier(
        trivialize=True,
        extract_trivial=True,
        rewrite_rest_filled=True,
        rewrite_sustained=True,
        ),
    )

# Initialize AttachmentHandler

attachment_handler_one = AttachmentHandler(
    starting_dynamic='f',
    ending_dynamic='ff',
    hairpin='<',
    # articulation_list=['accent', '', 'tenuto', '', '', 'portato', '', '', '', ],
)

attachment_handler_two = AttachmentHandler(
    starting_dynamic='p',
    ending_dynamic='mp',
    hairpin='<',
    articulation_list=['flageolet', 'flageolet', 'flageolet', 'flageolet', 'flageolet', 'halfopen', 'halfopen', 'halfopen', 'flageolet', 'stopped', 'stopped', 'stopped', 'stopped', 'halfopen', 'flageolet', 'halfopen', 'halfopen', 'halfopen', 'stopped', 'stopped', 'stopped', ],
)

attachment_handler_three = AttachmentHandler(
    starting_dynamic='mf',
    ending_dynamic='mp',
    hairpin='>',
    # articulation_list=['espressivo'],
)

# Initialize MusicMakers with the rhythm-makers.
#####sopranino#####
sopranino_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=sopranino_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
sopranino_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=sopranino_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
sopranino_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=sopranino_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####soprano_one#####
soprano_one_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_1_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
soprano_one_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_1_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
soprano_one_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_1_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####soprano_two#####
soprano_two_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_2_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
soprano_two_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_2_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
soprano_two_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_2_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####soprano_three#####
soprano_three_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_3_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
soprano_three_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_3_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
soprano_three_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_3_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####alto_one#####
alto_one_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_1_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_one_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_1_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
alto_one_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_1_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####alto_two#####
alto_two_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_2_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_two_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_2_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
alto_two_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_2_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####alto_three#####
alto_three_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_3_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_three_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_3_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
alto_three_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_3_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####alto_four#####
alto_four_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_4_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_four_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_4_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
alto_four_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_4_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####alto_five#####
alto_five_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_5_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_five_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_5_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
alto_five_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_5_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####alto_six#####
alto_six_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_6_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_six_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_6_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
alto_six_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_6_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####tenor_one#####
tenor_one_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_1_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
tenor_one_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_1_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
tenor_one_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_1_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####tenor_two#####
tenor_two_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_2_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
tenor_two_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_2_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
tenor_two_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_2_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####tenor_three#####
tenor_three_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_3_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
tenor_three_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_3_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
tenor_three_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_3_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####tenor_four#####
tenor_four_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_4_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
tenor_four_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_4_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
tenor_four_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_4_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####tenor_five#####
tenor_five_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_5_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
tenor_five_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_5_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
tenor_five_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_5_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####baritone_one#####
baritone_one_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=baritone_1_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
baritone_one_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=baritone_1_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
baritone_one_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=baritone_1_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####baritone_two#####
baritone_two_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=baritone_2_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
baritone_two_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=baritone_2_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
baritone_two_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=baritone_2_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####baritone_three#####
baritone_three_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=baritone_3_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
baritone_three_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=baritone_3_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
baritone_three_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=baritone_3_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####bass_one#####
bass_one_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=bass_1_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
bass_one_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=bass_1_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
bass_one_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=bass_1_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####bass_two#####
bass_two_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=bass_2_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
bass_two_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=bass_2_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
bass_two_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=bass_2_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####contrabass#####
contrabass_musicmaker_one = MusicMaker(
    rmaker=rmaker_two,
    pitches=contrabass_chord,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
contrabass_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=contrabass_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
contrabass_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=contrabass_note,
    continuous=True,
    attachment_handler=attachment_handler_three,
)

silence_maker = abjadext.rmakers.NoteRhythmMaker(
    division_masks=[
        abjadext.rmakers.SilenceMask(
            pattern=abjad.index([0], 1),
            ),
        ],
    )

# Define a small class so that we can annotate timespans with additional
# information:


class MusicSpecifier:

    def __init__(self, music_maker, voice_name):
        self.music_maker = music_maker
        self.voice_name = voice_name

# Define an initial timespan structure, annotated with music specifiers. This
# structure has not been split along meter boundaries. This structure does not
# contain timespans explicitly representing silence. Here I make four, one
# for each voice, using Python's list comprehension syntax to save some
# space.

print('Collecting timespans and rmakers ...')

voice_1_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 1',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), sopranino_musicmaker_two],
        [(2, 8), (4, 8), sopranino_musicmaker_one],
        [(4, 8), (6, 8), sopranino_musicmaker_two],
        [(6, 8), (8, 8), sopranino_musicmaker_two],

        [(10, 8), (12, 8), sopranino_musicmaker_two],
        [(12, 8), (14, 8), sopranino_musicmaker_two],
        [(14, 8), (16, 8), sopranino_musicmaker_two],
        [(16, 8), (18, 8), sopranino_musicmaker_one],
        [(18, 8), (20, 8), sopranino_musicmaker_two],
        [(20, 8), (22, 8), sopranino_musicmaker_two],
        [(22, 8), (24, 8), sopranino_musicmaker_two],

        [(26, 8), (28, 8), sopranino_musicmaker_one],
        [(28, 8), (30, 8), sopranino_musicmaker_two],
        [(30, 8), (32, 8), sopranino_musicmaker_two],
        [(32, 8), (34, 8), sopranino_musicmaker_two],
        [(34, 8), (36, 8), sopranino_musicmaker_three],
        [(36, 8), (38, 8), sopranino_musicmaker_three],
        [(38, 8), (40, 8), sopranino_musicmaker_one],
        [(40, 8), (42, 8), sopranino_musicmaker_two],
        [(42, 8), (44, 8), sopranino_musicmaker_two],
        [(44, 8), (46, 8), sopranino_musicmaker_two],
        [(46, 8), (48, 8), sopranino_musicmaker_one],
        [(48, 8), (50, 8), sopranino_musicmaker_three],

        [(52, 8), (54, 8), sopranino_musicmaker_two],
        [(54, 8), (56, 8), sopranino_musicmaker_two],
        [(56, 8), (57, 8), silence_maker],
        # [(56, 8), (58, 8), sopranino_musicmaker_one],
        # [(58, 8), (60, 8), sopranino_musicmaker_one],
        # [(60, 8), (62, 8), sopranino_musicmaker_three],
        # [(62, 8), (64, 8), sopranino_musicmaker_two],
        # [(64, 8), (66, 8), sopranino_musicmaker_two],
        # [(66, 8), (68, 8), sopranino_musicmaker_one],
        # [(68, 8), (70, 8), sopranino_musicmaker_three],
        # [(70, 8), (72, 8), sopranino_musicmaker_two],
        # [(72, 8), (74, 8), sopranino_musicmaker_one],
        #
        # [(76, 8), (78, 8), sopranino_musicmaker_two],
        # [(78, 8), (80, 8), sopranino_musicmaker_one],
        # [(80, 8), (82, 8), sopranino_musicmaker_one],
        # [(82, 8), (84, 8), sopranino_musicmaker_one],
        # [(84, 8), (86, 8), sopranino_musicmaker_three],
        # [(86, 8), (88, 8), sopranino_musicmaker_two],
        # [(88, 8), (90, 8), sopranino_musicmaker_two],
        # [(90, 8), (92, 8), sopranino_musicmaker_three],
        # [(92, 8), (94, 8), sopranino_musicmaker_three],
        # [(94, 8), (96, 8), sopranino_musicmaker_two],
        # [(96, 8), (98, 8), sopranino_musicmaker_one],
        # [(98, 8), (100, 8), sopranino_musicmaker_one],
        # [(100, 8), (102, 8), sopranino_musicmaker_one],
        # [(102, 8), (104, 8), sopranino_musicmaker_two],
        # [(104, 8), (106, 8), sopranino_musicmaker_two],
        # [(106, 8), (108, 8), sopranino_musicmaker_two],
        # [(108, 8), (110, 8), sopranino_musicmaker_one],
        # [(110, 8), (112, 8), sopranino_musicmaker_two],
        # [(112, 8), (114, 8), sopranino_musicmaker_two],
        # [(114, 8), (116, 8), sopranino_musicmaker_one],
        # [(116, 8), (118, 8), sopranino_musicmaker_one],
        # [(118, 8), (120, 8), sopranino_musicmaker_one],
        #
        # [(122, 8), (124, 8), sopranino_musicmaker_two],
        # [(124, 8), (126, 8), sopranino_musicmaker_two],
        # [(126, 8), (128, 8), sopranino_musicmaker_two],
        # [(128, 8), (130, 8), sopranino_musicmaker_three],
        # [(130, 8), (132, 8), sopranino_musicmaker_two],
        # [(132, 8), (134, 8), sopranino_musicmaker_two],
        # [(134, 8), (136, 8), sopranino_musicmaker_one],
        # [(136, 8), (138, 8), sopranino_musicmaker_one],
        # [(138, 8), (140, 8), sopranino_musicmaker_three],
        # [(140, 8), (142, 8), sopranino_musicmaker_three],
        # [(142, 8), (144, 8), sopranino_musicmaker_one],
        # [(144, 8), (146, 8), sopranino_musicmaker_two],
        #
        # [(150, 8), (152, 8), sopranino_musicmaker_three],
        # [(152, 8), (154, 8), sopranino_musicmaker_two],
        # [(154, 8), (156, 8), sopranino_musicmaker_one],
        #
        # [(158, 8), (160, 8), sopranino_musicmaker_one],
        # [(160, 8), (162, 8), sopranino_musicmaker_two],
        # [(162, 8), (164, 8), sopranino_musicmaker_two],
        # [(164, 8), (166, 8), sopranino_musicmaker_two],
        # [(166, 8), (168, 8), sopranino_musicmaker_one],
        # [(168, 8), (170, 8), sopranino_musicmaker_two],
        # [(170, 8), (172, 8), sopranino_musicmaker_three],
        # [(172, 8), (174, 8), sopranino_musicmaker_one],
        #
        # [(176, 8), (178, 8), sopranino_musicmaker_one],
        # [(178, 8), (180, 8), sopranino_musicmaker_one],
        # [(180, 8), (182, 8), sopranino_musicmaker_three],
        # [(182, 8), (184, 8), sopranino_musicmaker_one],
        # [(184, 8), (186, 8), sopranino_musicmaker_two],
        # [(186, 8), (188, 8), sopranino_musicmaker_three],
        # [(188, 8), (190, 8), sopranino_musicmaker_two],
        # [(190, 8), (192, 8), sopranino_musicmaker_two],
        #
        # [(194, 8), (196, 8), sopranino_musicmaker_one],
        # [(196, 8), (198, 8), sopranino_musicmaker_one],
        # [(198, 8), (199, 8), sopranino_musicmaker_one],
        # [(199, 8), (200, 8), silence_maker],
    ]
])

voice_2_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 2',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), soprano_one_musicmaker_two],
        [(2, 8), (4, 8), soprano_one_musicmaker_three],
        [(4, 8), (6, 8), soprano_one_musicmaker_two],

        [(8, 8), (10, 8), soprano_one_musicmaker_three],
        [(10, 8), (12, 8), soprano_one_musicmaker_two],
        [(12, 8), (14, 8), soprano_one_musicmaker_two],
        [(14, 8), (16, 8), soprano_one_musicmaker_one],
        [(16, 8), (18, 8), soprano_one_musicmaker_three],
        [(18, 8), (20, 8), soprano_one_musicmaker_one],

        [(22, 8), (24, 8), soprano_one_musicmaker_one],
        [(24, 8), (26, 8), soprano_one_musicmaker_one],
        [(26, 8), (28, 8), soprano_one_musicmaker_three],
        [(28, 8), (30, 8), soprano_one_musicmaker_two],
        [(30, 8), (32, 8), soprano_one_musicmaker_two],
        [(32, 8), (34, 8), soprano_one_musicmaker_two],
        [(34, 8), (36, 8), soprano_one_musicmaker_two],
        [(36, 8), (38, 8), soprano_one_musicmaker_three],

        [(40, 8), (42, 8), soprano_one_musicmaker_one],
        [(42, 8), (44, 8), soprano_one_musicmaker_one],

        [(46, 8), (48, 8), soprano_one_musicmaker_one],
        [(48, 8), (50, 8), soprano_one_musicmaker_two],
        [(50, 8), (52, 8), soprano_one_musicmaker_three],
        [(52, 8), (54, 8), soprano_one_musicmaker_two],
        [(54, 8), (56, 8), soprano_one_musicmaker_one],
        # [(56, 8), (58, 8), soprano_one_musicmaker_one],
        # [(58, 8), (60, 8), soprano_one_musicmaker_one],
        # [(60, 8), (62, 8), soprano_one_musicmaker_two],
        # [(62, 8), (64, 8), soprano_one_musicmaker_one],
        # [(64, 8), (66, 8), soprano_one_musicmaker_three],
        # [(66, 8), (68, 8), soprano_one_musicmaker_two],
        # [(68, 8), (70, 8), soprano_one_musicmaker_two],
        #
        # [(72, 8), (74, 8), soprano_one_musicmaker_two],
        # [(74, 8), (76, 8), soprano_one_musicmaker_two],
        # [(76, 8), (78, 8), soprano_one_musicmaker_one],
        # [(78, 8), (80, 8), soprano_one_musicmaker_one],
        # [(80, 8), (82, 8), soprano_one_musicmaker_three],
        # [(82, 8), (84, 8), soprano_one_musicmaker_one],
        # [(84, 8), (86, 8), soprano_one_musicmaker_one],
        #
        # [(88, 8), (90, 8), soprano_one_musicmaker_two],
        # [(90, 8), (92, 8), soprano_one_musicmaker_two],
        # [(92, 8), (94, 8), soprano_one_musicmaker_two],
        # [(94, 8), (96, 8), soprano_one_musicmaker_two],
        # [(96, 8), (98, 8), soprano_one_musicmaker_one],
        # [(98, 8), (100, 8), soprano_one_musicmaker_three],
        # [(100, 8), (102, 8), soprano_one_musicmaker_one],
        # [(102, 8), (104, 8), soprano_one_musicmaker_one],
        #
        # [(106, 8), (108, 8), soprano_one_musicmaker_two],
        # [(108, 8), (110, 8), soprano_one_musicmaker_one],
        # [(110, 8), (112, 8), soprano_one_musicmaker_one],
        #
        # [(114, 8), (116, 8), soprano_one_musicmaker_two],
        # [(116, 8), (118, 8), soprano_one_musicmaker_two],
        # [(118, 8), (120, 8), soprano_one_musicmaker_three],
        # [(120, 8), (122, 8), soprano_one_musicmaker_one],
        # [(122, 8), (124, 8), soprano_one_musicmaker_one],
        # [(124, 8), (126, 8), soprano_one_musicmaker_two],
        # [(126, 8), (128, 8), soprano_one_musicmaker_two],
        # [(128, 8), (130, 8), soprano_one_musicmaker_two],
        #
        # [(134, 8), (136, 8), soprano_one_musicmaker_one],
        # [(136, 8), (138, 8), soprano_one_musicmaker_one],
        # [(138, 8), (140, 8), soprano_one_musicmaker_one],
        # [(140, 8), (142, 8), soprano_one_musicmaker_three],
        # [(142, 8), (144, 8), soprano_one_musicmaker_one],
        # [(144, 8), (146, 8), soprano_one_musicmaker_two],
        # [(146, 8), (148, 8), soprano_one_musicmaker_two],
        # [(148, 8), (150, 8), soprano_one_musicmaker_two],
        # [(150, 8), (152, 8), soprano_one_musicmaker_two],
        # [(152, 8), (154, 8), soprano_one_musicmaker_two],
        #
        # [(156, 8), (158, 8), soprano_one_musicmaker_two],
        # [(158, 8), (160, 8), soprano_one_musicmaker_one],
        # [(160, 8), (162, 8), soprano_one_musicmaker_one],
        # [(162, 8), (164, 8), soprano_one_musicmaker_one],
        # [(164, 8), (166, 8), soprano_one_musicmaker_three],
        # [(166, 8), (168, 8), soprano_one_musicmaker_one],
        # [(168, 8), (170, 8), soprano_one_musicmaker_one],
        # [(170, 8), (172, 8), soprano_one_musicmaker_one],
        # [(172, 8), (174, 8), soprano_one_musicmaker_two],
        # [(174, 8), (176, 8), soprano_one_musicmaker_two],
        # [(176, 8), (178, 8), soprano_one_musicmaker_two],
        # [(178, 8), (180, 8), soprano_one_musicmaker_three],
        # [(180, 8), (182, 8), soprano_one_musicmaker_two],
        # [(182, 8), (184, 8), soprano_one_musicmaker_two],
        # [(184, 8), (186, 8), soprano_one_musicmaker_one],
        #
        # [(188, 8), (190, 8), soprano_one_musicmaker_one],
        # [(190, 8), (192, 8), soprano_one_musicmaker_three],
        # [(192, 8), (194, 8), soprano_one_musicmaker_one],
        # [(194, 8), (196, 8), soprano_one_musicmaker_one],
        # [(196, 8), (198, 8), soprano_one_musicmaker_one],
        # [(198, 8), (199, 8), soprano_one_musicmaker_one],
    ]
])

voice_3_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 3',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), soprano_two_musicmaker_one],
        [(2, 8), (4, 8), soprano_two_musicmaker_one],
        [(4, 8), (6, 8), soprano_two_musicmaker_one],
        [(6, 8), (8, 8), soprano_two_musicmaker_one],
        [(8, 8), (10, 8), soprano_two_musicmaker_one],
        [(10, 8), (12, 8), soprano_two_musicmaker_three],
        [(12, 8), (14, 8), soprano_two_musicmaker_one],
        [(14, 8), (16, 8), soprano_two_musicmaker_one],
        [(16, 8), (18, 8), soprano_two_musicmaker_two],

        [(20, 8), (22, 8), soprano_two_musicmaker_two],
        [(22, 8), (24, 8), soprano_two_musicmaker_three],
        [(24, 8), (26, 8), soprano_two_musicmaker_two],
        [(26, 8), (28, 8), soprano_two_musicmaker_two],
        [(28, 8), (30, 8), soprano_two_musicmaker_two],
        [(30, 8), (32, 8), soprano_two_musicmaker_one],
        [(32, 8), (34, 8), soprano_two_musicmaker_one],
        [(34, 8), (36, 8), soprano_two_musicmaker_one],
        [(36, 8), (38, 8), soprano_two_musicmaker_three],
        [(38, 8), (40, 8), soprano_two_musicmaker_one],
        [(40, 8), (42, 8), soprano_two_musicmaker_one],
        [(42, 8), (44, 8), soprano_two_musicmaker_two],
        [(44, 8), (46, 8), soprano_two_musicmaker_three],
        [(46, 8), (48, 8), soprano_two_musicmaker_two],
        [(48, 8), (50, 8), soprano_two_musicmaker_two],
        [(50, 8), (52, 8), soprano_two_musicmaker_one],

        # [(54, 8), (56, 8), soprano_two_musicmaker_one],
        # [(56, 8), (58, 8), soprano_two_musicmaker_one],
        # [(58, 8), (60, 8), soprano_two_musicmaker_two],
        # [(60, 8), (62, 8), soprano_two_musicmaker_two],
        # [(62, 8), (64, 8), soprano_two_musicmaker_two],
        # [(64, 8), (66, 8), soprano_two_musicmaker_three],
        # [(66, 8), (68, 8), soprano_two_musicmaker_one],
        # [(68, 8), (70, 8), soprano_two_musicmaker_two],
        # [(70, 8), (72, 8), soprano_two_musicmaker_one],
        # [(72, 8), (74, 8), soprano_two_musicmaker_two],
        # [(74, 8), (76, 8), soprano_two_musicmaker_two],
        # [(76, 8), (78, 8), soprano_two_musicmaker_one],
        # [(78, 8), (80, 8), soprano_two_musicmaker_one],
        # [(80, 8), (82, 8), soprano_two_musicmaker_one],
        # [(82, 8), (84, 8), soprano_two_musicmaker_three],
        # [(84, 8), (86, 8), soprano_two_musicmaker_two],
        # [(86, 8), (88, 8), soprano_two_musicmaker_two],
        # [(88, 8), (90, 8), soprano_two_musicmaker_two],
        # [(90, 8), (92, 8), soprano_two_musicmaker_one],
        # [(92, 8), (94, 8), soprano_two_musicmaker_one],
        # [(94, 8), (96, 8), soprano_two_musicmaker_one],
        # [(96, 8), (98, 8), soprano_two_musicmaker_one],
        # [(98, 8), (100, 8), soprano_two_musicmaker_three],
        # [(100, 8), (102, 8), soprano_two_musicmaker_two],
        # [(102, 8), (104, 8), soprano_two_musicmaker_two],
        # [(104, 8), (106, 8), soprano_two_musicmaker_two],
        #
        # [(108, 8), (110, 8), soprano_two_musicmaker_one],
        # [(110, 8), (112, 8), soprano_two_musicmaker_one],
        # [(112, 8), (114, 8), soprano_two_musicmaker_three],
        # [(114, 8), (116, 8), soprano_two_musicmaker_one],
        # [(116, 8), (118, 8), soprano_two_musicmaker_one],
        # [(118, 8), (120, 8), soprano_two_musicmaker_one],
        # [(120, 8), (122, 8), soprano_two_musicmaker_two],
        # [(122, 8), (124, 8), soprano_two_musicmaker_two],
        # [(124, 8), (126, 8), soprano_two_musicmaker_three],
        # [(126, 8), (128, 8), soprano_two_musicmaker_two],
        # [(128, 8), (130, 8), soprano_two_musicmaker_two],
        # [(130, 8), (132, 8), soprano_two_musicmaker_two],
        # [(132, 8), (134, 8), soprano_two_musicmaker_two],
        # [(134, 8), (136, 8), soprano_two_musicmaker_three],
        # [(136, 8), (138, 8), soprano_two_musicmaker_one],
        # [(138, 8), (140, 8), soprano_two_musicmaker_one],
        # [(140, 8), (142, 8), soprano_two_musicmaker_one],
        # [(142, 8), (144, 8), soprano_two_musicmaker_three],
        # [(144, 8), (146, 8), soprano_two_musicmaker_one],
        # [(146, 8), (148, 8), soprano_two_musicmaker_one],
        # [(148, 8), (150, 8), soprano_two_musicmaker_three],
        # [(150, 8), (152, 8), soprano_two_musicmaker_two],
        # [(152, 8), (154, 8), soprano_two_musicmaker_three],
        # [(154, 8), (156, 8), soprano_two_musicmaker_three],
        # [(156, 8), (158, 8), soprano_two_musicmaker_one],
        #
        # [(162, 8), (164, 8), soprano_two_musicmaker_one],
        # [(164, 8), (166, 8), soprano_two_musicmaker_one],
        # [(166, 8), (168, 8), soprano_two_musicmaker_two],
        # [(168, 8), (170, 8), soprano_two_musicmaker_three],
        # [(170, 8), (172, 8), soprano_two_musicmaker_two],
        #
        # [(174, 8), (176, 8), soprano_two_musicmaker_two],
        # [(176, 8), (178, 8), soprano_two_musicmaker_two],
        # [(178, 8), (180, 8), soprano_two_musicmaker_three],
        # [(180, 8), (182, 8), soprano_two_musicmaker_one],
        #
        # [(184, 8), (186, 8), soprano_two_musicmaker_two],
        # [(186, 8), (188, 8), soprano_two_musicmaker_two],
        # [(188, 8), (190, 8), soprano_two_musicmaker_two],
        # [(190, 8), (192, 8), soprano_two_musicmaker_three],
        # [(192, 8), (194, 8), soprano_two_musicmaker_one],
        #
        # [(196, 8), (198, 8), soprano_two_musicmaker_one],
        # [(198, 8), (199, 8), soprano_two_musicmaker_one],
    ]
])

voice_4_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 4',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), soprano_three_musicmaker_two],
        [(2, 8), (4, 8), soprano_three_musicmaker_two],
        [(4, 8), (6, 8), soprano_three_musicmaker_two],
        [(6, 8), (8, 8), soprano_three_musicmaker_three],
        [(8, 8), (10, 8), soprano_three_musicmaker_one],
        [(10, 8), (12, 8), soprano_three_musicmaker_one],
        [(12, 8), (14, 8), soprano_three_musicmaker_one],
        [(14, 8), (16, 8), soprano_three_musicmaker_three],
        [(16, 8), (18, 8), soprano_three_musicmaker_two],

        [(20, 8), (22, 8), soprano_three_musicmaker_two],
        [(22, 8), (24, 8), soprano_three_musicmaker_three],
        [(24, 8), (26, 8), soprano_three_musicmaker_two],
        [(26, 8), (28, 8), soprano_three_musicmaker_two],
        [(28, 8), (30, 8), soprano_three_musicmaker_two],
        [(30, 8), (32, 8), soprano_three_musicmaker_three],
        [(32, 8), (34, 8), soprano_three_musicmaker_one],
        [(34, 8), (36, 8), soprano_three_musicmaker_one],
        [(36, 8), (38, 8), soprano_three_musicmaker_one],
        [(39, 8), (40, 8), soprano_three_musicmaker_three],

        [(42, 8), (44, 8), soprano_three_musicmaker_one],
        [(44, 8), (46, 8), soprano_three_musicmaker_two],
        [(46, 8), (48, 8), soprano_three_musicmaker_three],
        [(48, 8), (50, 8), soprano_three_musicmaker_two],
        [(50, 8), (52, 8), soprano_three_musicmaker_two],
        [(52, 8), (54, 8), soprano_three_musicmaker_two],
        [(54, 8), (56, 8), soprano_three_musicmaker_three],
        # [(56, 8), (58, 8), soprano_three_musicmaker_two],
        # [(58, 8), (60, 8), soprano_three_musicmaker_one],
        # [(60, 8), (62, 8), soprano_three_musicmaker_one],
        # [(62, 8), (64, 8), soprano_three_musicmaker_three],
        # [(64, 8), (66, 8), soprano_three_musicmaker_one],
        # [(66, 8), (68, 8), soprano_three_musicmaker_one],
        # [(68, 8), (70, 8), soprano_three_musicmaker_one],
        # [(70, 8), (72, 8), soprano_three_musicmaker_three],
        # [(72, 8), (74, 8), soprano_three_musicmaker_two],
        #
        # [(76, 8), (78, 8), soprano_three_musicmaker_two],
        # [(78, 8), (80, 8), soprano_three_musicmaker_three],
        # [(80, 8), (82, 8), soprano_three_musicmaker_two],
        # [(82, 8), (84, 8), soprano_three_musicmaker_two],
        # [(84, 8), (86, 8), soprano_three_musicmaker_two],
        # [(86, 8), (88, 8), soprano_three_musicmaker_three],
        # [(88, 8), (90, 8), soprano_three_musicmaker_one],
        # [(90, 8), (92, 8), soprano_three_musicmaker_one],
        # [(92, 8), (94, 8), soprano_three_musicmaker_one],
        # [(94, 8), (96, 8), soprano_three_musicmaker_three],
        # [(96, 8), (98, 8), soprano_three_musicmaker_one],
        # [(98, 8), (100, 8), soprano_three_musicmaker_one],
        # [(100, 8), (102, 8), soprano_three_musicmaker_two],
        # [(102, 8), (104, 8), soprano_three_musicmaker_three],
        # [(104, 8), (106, 8), soprano_three_musicmaker_two],
        # [(106, 8), (108, 8), soprano_three_musicmaker_two],
        # [(108, 8), (110, 8), soprano_three_musicmaker_two],
        # [(110, 8), (112, 8), soprano_three_musicmaker_three],
        # [(112, 8), (114, 8), soprano_three_musicmaker_two],
        # [(114, 8), (116, 8), soprano_three_musicmaker_one],
        # [(116, 8), (118, 8), soprano_three_musicmaker_one],
        # [(118, 8), (120, 8), soprano_three_musicmaker_three],
        # [(120, 8), (122, 8), soprano_three_musicmaker_one],
        #
        # [(124, 8), (126, 8), soprano_three_musicmaker_one],
        # [(126, 8), (128, 8), soprano_three_musicmaker_three],
        # [(128, 8), (130, 8), soprano_three_musicmaker_two],
        # [(130, 8), (132, 8), soprano_three_musicmaker_two],
        # [(132, 8), (134, 8), soprano_three_musicmaker_two],
        #
        # [(136, 8), (138, 8), soprano_three_musicmaker_two],
        # [(138, 8), (140, 8), soprano_three_musicmaker_two],
        # [(140, 8), (142, 8), soprano_three_musicmaker_two],
        # [(142, 8), (144, 8), soprano_three_musicmaker_three],
        # [(144, 8), (146, 8), soprano_three_musicmaker_one],
        # [(146, 8), (148, 8), soprano_three_musicmaker_one],
        # [(148, 8), (150, 8), soprano_three_musicmaker_one],
        # [(150, 8), (152, 8), soprano_three_musicmaker_three],
        # [(152, 8), (154, 8), soprano_three_musicmaker_one],
        # [(154, 8), (156, 8), soprano_three_musicmaker_one],
        # [(156, 8), (158, 8), soprano_three_musicmaker_two],
        # [(158, 8), (160, 8), soprano_three_musicmaker_three],
        # [(160, 8), (162, 8), soprano_three_musicmaker_two],
        # [(162, 8), (164, 8), soprano_three_musicmaker_two],
        #
        # [(168, 8), (170, 8), soprano_three_musicmaker_two],
        # [(170, 8), (172, 8), soprano_three_musicmaker_one],
        # [(172, 8), (174, 8), soprano_three_musicmaker_one],
        # [(174, 8), (176, 8), soprano_three_musicmaker_three],
        #
        # [(180, 8), (182, 8), soprano_three_musicmaker_one],
        # [(182, 8), (184, 8), soprano_three_musicmaker_three],
        # [(184, 8), (186, 8), soprano_three_musicmaker_two],
        # [(186, 8), (188, 8), soprano_three_musicmaker_two],
        # [(188, 8), (190, 8), soprano_three_musicmaker_one],
        #
        # [(192, 8), (194, 8), soprano_three_musicmaker_one],
        # [(194, 8), (196, 8), soprano_three_musicmaker_one],
        # [(196, 8), (198, 8), soprano_three_musicmaker_one],
        # [(198, 8), (199, 8), soprano_three_musicmaker_one],
    ]
])

voice_5_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 5',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), alto_one_musicmaker_one],
        [(2, 8), (4, 8), alto_one_musicmaker_one],
        [(4, 8), (6, 8), alto_one_musicmaker_two],
        [(6, 8), (8, 8), alto_one_musicmaker_two],
        [(8, 8), (10, 8), alto_one_musicmaker_three],

        [(12, 8), (14, 8), alto_one_musicmaker_two],
        [(14, 8), (16, 8), alto_one_musicmaker_one],
        [(16, 8), (18, 8), alto_one_musicmaker_one],
        [(18, 8), (20, 8), alto_one_musicmaker_three],

        [(22, 8), (24, 8), alto_one_musicmaker_one],
        [(24, 8), (26, 8), alto_one_musicmaker_two],
        [(26, 8), (28, 8), alto_one_musicmaker_two],
        [(28, 8), (30, 8), alto_one_musicmaker_three],
        [(30, 8), (32, 8), alto_one_musicmaker_two],
        [(32, 8), (34, 8), alto_one_musicmaker_two],
        [(34, 8), (36, 8), alto_one_musicmaker_one],

        [(38, 8), (40, 8), alto_one_musicmaker_three],
        [(40, 8), (42, 8), alto_one_musicmaker_one],
        [(42, 8), (44, 8), alto_one_musicmaker_one],
        [(44, 8), (46, 8), alto_one_musicmaker_two],
        [(46, 8), (48, 8), alto_one_musicmaker_two],
        [(48, 8), (50, 8), alto_one_musicmaker_three],
        [(50, 8), (52, 8), alto_one_musicmaker_two],

        [(54, 8), (56, 8), alto_one_musicmaker_one],
        # [(56, 8), (58, 8), alto_one_musicmaker_one],
        # [(58, 8), (60, 8), alto_one_musicmaker_three],
        # [(60, 8), (62, 8), alto_one_musicmaker_one],
        # [(62, 8), (64, 8), alto_one_musicmaker_one],
        # [(64, 8), (66, 8), alto_one_musicmaker_two],
        # [(66, 8), (68, 8), alto_one_musicmaker_two],
        # [(68, 8), (70, 8), alto_one_musicmaker_three],
        # [(70, 8), (72, 8), alto_one_musicmaker_two],
        # [(72, 8), (74, 8), alto_one_musicmaker_two],
        #
        # [(76, 8), (78, 8), alto_one_musicmaker_one],
        # [(78, 8), (80, 8), alto_one_musicmaker_three],
        # [(80, 8), (82, 8), alto_one_musicmaker_one],
        # [(82, 8), (84, 8), alto_one_musicmaker_one],
        # [(84, 8), (86, 8), alto_one_musicmaker_two],
        # [(86, 8), (88, 8), alto_one_musicmaker_two],
        # [(88, 8), (90, 8), alto_one_musicmaker_three],
        # [(90, 8), (92, 8), alto_one_musicmaker_two],
        #
        # [(94, 8), (96, 8), alto_one_musicmaker_one],
        # [(96, 8), (98, 8), alto_one_musicmaker_one],
        # [(98, 8), (100, 8), alto_one_musicmaker_three],
        # [(100, 8), (102, 8), alto_one_musicmaker_one],
        # [(102, 8), (104, 8), alto_one_musicmaker_one],
        # [(104, 8), (106, 8), alto_one_musicmaker_two],
        # [(106, 8), (108, 8), alto_one_musicmaker_two],
        # [(108, 8), (110, 8), alto_one_musicmaker_three],
        # [(110, 8), (112, 8), alto_one_musicmaker_two],
        #
        # [(114, 8), (116, 8), alto_one_musicmaker_one],
        # [(116, 8), (118, 8), alto_one_musicmaker_one],
        # [(118, 8), (120, 8), alto_one_musicmaker_three],
        # [(120, 8), (122, 8), alto_one_musicmaker_one],
        # [(122, 8), (124, 8), alto_one_musicmaker_one],
        # [(124, 8), (126, 8), alto_one_musicmaker_two],
        # [(126, 8), (128, 8), alto_one_musicmaker_two],
        # [(128, 8), (130, 8), alto_one_musicmaker_three],
        # [(130, 8), (132, 8), alto_one_musicmaker_two],
        # [(132, 8), (134, 8), alto_one_musicmaker_two],
        # [(134, 8), (136, 8), alto_one_musicmaker_one],
        #
        # [(138, 8), (140, 8), alto_one_musicmaker_three],
        # [(140, 8), (142, 8), alto_one_musicmaker_one],
        # [(142, 8), (144, 8), alto_one_musicmaker_one],
        # [(144, 8), (146, 8), alto_one_musicmaker_two],
        # [(146, 8), (148, 8), alto_one_musicmaker_two],
        # [(148, 8), (150, 8), alto_one_musicmaker_three],
        # [(150, 8), (152, 8), alto_one_musicmaker_two],
        # [(152, 8), (154, 8), alto_one_musicmaker_two],
        #
        # [(158, 8), (160, 8), alto_one_musicmaker_three],
        # [(160, 8), (162, 8), alto_one_musicmaker_one],
        # [(162, 8), (164, 8), alto_one_musicmaker_one],
        # [(164, 8), (166, 8), alto_one_musicmaker_two],
        # [(166, 8), (168, 8), alto_one_musicmaker_two],
        #
        # [(170, 8), (172, 8), alto_one_musicmaker_two],
        # [(172, 8), (174, 8), alto_one_musicmaker_two],
        # [(174, 8), (176, 8), alto_one_musicmaker_one],
        # [(176, 8), (178, 8), alto_one_musicmaker_one],
        # [(178, 8), (180, 8), alto_one_musicmaker_three],
        # [(180, 8), (182, 8), alto_one_musicmaker_one],
        # [(182, 8), (184, 8), alto_one_musicmaker_one],
        # [(184, 8), (186, 8), alto_one_musicmaker_two],
        #
        # [(188, 8), (190, 8), alto_one_musicmaker_three],
        # [(190, 8), (192, 8), alto_one_musicmaker_one],
        # [(192, 8), (194, 8), alto_one_musicmaker_one],
        #
        # [(196, 8), (198, 8), alto_one_musicmaker_one],
        # [(198, 8), (199, 8), alto_one_musicmaker_one],
    ]
])

voice_6_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 6',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), alto_two_musicmaker_one],
        [(2, 8), (4, 8), alto_two_musicmaker_one],
        [(4, 8), (6, 8), alto_two_musicmaker_one],
        [(6, 8), (8, 8), alto_two_musicmaker_one],
        [(8, 8), (10, 8), alto_two_musicmaker_two],
        [(10, 8), (12, 8), alto_two_musicmaker_three],

        [(14, 8), (16, 8), alto_two_musicmaker_two],
        [(16, 8), (18, 8), alto_two_musicmaker_two],
        [(18, 8), (20, 8), alto_two_musicmaker_two],
        [(20, 8), (22, 8), alto_two_musicmaker_one],
        [(22, 8), (24, 8), alto_two_musicmaker_three],
        [(24, 8), (26, 8), alto_two_musicmaker_one],

        [(28, 8), (30, 8), alto_two_musicmaker_one],
        [(30, 8), (32, 8), alto_two_musicmaker_two],
        [(32, 8), (34, 8), alto_two_musicmaker_two],
        [(34, 8), (36, 8), alto_two_musicmaker_three],
        [(36, 8), (38, 8), alto_two_musicmaker_two],
        [(38, 8), (40, 8), alto_two_musicmaker_one],
        [(40, 8), (42, 8), alto_two_musicmaker_one],
        [(42, 8), (44, 8), alto_two_musicmaker_one],
        [(44, 8), (46, 8), alto_two_musicmaker_two],
        [(46, 8), (48, 8), alto_two_musicmaker_three],
        [(48, 8), (50, 8), alto_two_musicmaker_one],
        [(50, 8), (52, 8), alto_two_musicmaker_two],
        [(52, 8), (54, 8), alto_two_musicmaker_one],

        # [(56, 8), (58, 8), alto_two_musicmaker_two],
        # [(58, 8), (60, 8), alto_two_musicmaker_three],
        # [(60, 8), (62, 8), alto_two_musicmaker_one],
        # [(62, 8), (64, 8), alto_two_musicmaker_two],
        # [(64, 8), (66, 8), alto_two_musicmaker_two],
        # [(66, 8), (68, 8), alto_two_musicmaker_two],
        # [(68, 8), (70, 8), alto_two_musicmaker_one],
        # [(70, 8), (72, 8), alto_two_musicmaker_three],
        # [(72, 8), (74, 8), alto_two_musicmaker_one],
        # [(74, 8), (76, 8), alto_two_musicmaker_two],
        #
        # [(78, 8), (80, 8), alto_two_musicmaker_two],
        # [(80, 8), (82, 8), alto_two_musicmaker_two],
        # [(82, 8), (84, 8), alto_two_musicmaker_three],
        # [(84, 8), (86, 8), alto_two_musicmaker_one],
        # [(86, 8), (88, 8), alto_two_musicmaker_one],
        # [(88, 8), (90, 8), alto_two_musicmaker_one],
        # [(90, 8), (92, 8), alto_two_musicmaker_two],
        #
        # [(96, 8), (98, 8), alto_two_musicmaker_two],
        # [(98, 8), (100, 8), alto_two_musicmaker_two],
        # [(100, 8), (102, 8), alto_two_musicmaker_one],
        # [(102, 8), (104, 8), alto_two_musicmaker_one],
        # [(104, 8), (106, 8), alto_two_musicmaker_one],
        # [(106, 8), (108, 8), alto_two_musicmaker_three],
        # [(108, 8), (110, 8), alto_two_musicmaker_one],
        # [(110, 8), (112, 8), alto_two_musicmaker_two],
        # [(112, 8), (114, 8), alto_two_musicmaker_two],
        #
        # [(116, 8), (118, 8), alto_two_musicmaker_two],
        # [(118, 8), (120, 8), alto_two_musicmaker_three],
        # [(120, 8), (122, 8), alto_two_musicmaker_two],
        # [(122, 8), (124, 8), alto_two_musicmaker_one],
        # [(124, 8), (126, 8), alto_two_musicmaker_one],
        # [(126, 8), (128, 8), alto_two_musicmaker_one],
        # [(128, 8), (130, 8), alto_two_musicmaker_one],
        #
        # [(132, 8), (134, 8), alto_two_musicmaker_one],
        # [(134, 8), (136, 8), alto_two_musicmaker_two],
        # [(136, 8), (138, 8), alto_two_musicmaker_two],
        # [(138, 8), (140, 8), alto_two_musicmaker_two],
        # [(140, 8), (142, 8), alto_two_musicmaker_two],
        # [(142, 8), (144, 8), alto_two_musicmaker_three],
        # [(144, 8), (146, 8), alto_two_musicmaker_two],
        #
        # [(148, 8), (150, 8), alto_two_musicmaker_one],
        # [(150, 8), (152, 8), alto_two_musicmaker_one],
        # [(152, 8), (154, 8), alto_two_musicmaker_one],
        # [(154, 8), (156, 8), alto_two_musicmaker_three],
        # [(156, 8), (158, 8), alto_two_musicmaker_one],
        # [(158, 8), (160, 8), alto_two_musicmaker_one],
        #
        # [(162, 8), (164, 8), alto_two_musicmaker_two],
        # [(164, 8), (166, 8), alto_two_musicmaker_two],
        # [(166, 8), (168, 8), alto_two_musicmaker_three],
        # [(168, 8), (170, 8), alto_two_musicmaker_two],
        # [(170, 8), (172, 8), alto_two_musicmaker_two],
        # [(172, 8), (174, 8), alto_two_musicmaker_two],
        # [(174, 8), (176, 8), alto_two_musicmaker_two],
        # [(176, 8), (178, 8), alto_two_musicmaker_two],
        # [(178, 8), (180, 8), alto_two_musicmaker_three],
        # [(180, 8), (182, 8), alto_two_musicmaker_one],
        # [(182, 8), (184, 8), alto_two_musicmaker_one],
        #
        # [(186, 8), (188, 8), alto_two_musicmaker_one],
        # [(188, 8), (190, 8), alto_two_musicmaker_one],
        #
        # [(192, 8), (194, 8), alto_two_musicmaker_one],
        # [(194, 8), (196, 8), alto_two_musicmaker_one],
        # [(196, 8), (198, 8), alto_two_musicmaker_one],
        # [(198, 8), (199, 8), alto_two_musicmaker_one],
    ]
])

voice_7_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 7',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), alto_three_musicmaker_two],

        [(4, 8), (6, 8), alto_three_musicmaker_two],
        [(6, 8), (8, 8), alto_three_musicmaker_two],
        [(8, 8), (10, 8), alto_three_musicmaker_two],

        [(12, 8), (14, 8), alto_three_musicmaker_two],
        [(14, 8), (16, 8), alto_three_musicmaker_one],
        [(16, 8), (18, 8), alto_three_musicmaker_three],
        [(18, 8), (20, 8), alto_three_musicmaker_one],

        [(22, 8), (24, 8), alto_three_musicmaker_two],
        [(24, 8), (26, 8), alto_three_musicmaker_two],
        [(26, 8), (28, 8), alto_three_musicmaker_two],

        [(32, 8), (34, 8), alto_three_musicmaker_one],
        [(34, 8), (36, 8), alto_three_musicmaker_three],
        [(36, 8), (38, 8), alto_three_musicmaker_one],
        [(38, 8), (40, 8), alto_three_musicmaker_one],
        [(40, 8), (42, 8), alto_three_musicmaker_one],

        [(44, 8), (46, 8), alto_three_musicmaker_two],
        [(46, 8), (48, 8), alto_three_musicmaker_two],
        [(48, 8), (50, 8), alto_three_musicmaker_two],
        [(50, 8), (52, 8), alto_three_musicmaker_two],
        [(52, 8), (54, 8), alto_three_musicmaker_three],

        # [(56, 8), (58, 8), alto_three_musicmaker_one],
        # [(58, 8), (60, 8), alto_three_musicmaker_one],
        # [(60, 8), (62, 8), alto_three_musicmaker_one],
        # [(62, 8), (64, 8), alto_three_musicmaker_one],
        # [(64, 8), (66, 8), alto_three_musicmaker_two],
        # [(66, 8), (68, 8), alto_three_musicmaker_two],
        # [(68, 8), (70, 8), alto_three_musicmaker_two],
        # [(70, 8), (72, 8), alto_three_musicmaker_three],
        # [(72, 8), (74, 8), alto_three_musicmaker_two],
        # [(74, 8), (76, 8), alto_three_musicmaker_one],
        #
        # [(80, 8), (82, 8), alto_three_musicmaker_one],
        # [(82, 8), (84, 8), alto_three_musicmaker_one],
        # [(84, 8), (86, 8), alto_three_musicmaker_one],
        # [(86, 8), (88, 8), alto_three_musicmaker_two],
        # [(88, 8), (90, 8), alto_three_musicmaker_three],
        # [(90, 8), (92, 8), alto_three_musicmaker_two],
        # [(92, 8), (94, 8), alto_three_musicmaker_two],
        # [(94, 8), (96, 8), alto_three_musicmaker_two],
        # [(96, 8), (98, 8), alto_three_musicmaker_two],
        # [(98, 8), (100, 8), alto_three_musicmaker_one],
        #
        # [(102, 8), (104, 8), alto_three_musicmaker_one],
        # [(104, 8), (106, 8), alto_three_musicmaker_two],
        # [(106, 8), (108, 8), alto_three_musicmaker_three],
        # [(108, 8), (110, 8), alto_three_musicmaker_two],
        # [(110, 8), (112, 8), alto_three_musicmaker_two],
        #
        # [(114, 8), (116, 8), alto_three_musicmaker_one],
        # [(116, 8), (118, 8), alto_three_musicmaker_one],
        # [(118, 8), (120, 8), alto_three_musicmaker_one],
        # [(120, 8), (122, 8), alto_three_musicmaker_one],
        # [(122, 8), (124, 8), alto_three_musicmaker_two],
        # [(124, 8), (126, 8), alto_three_musicmaker_three],
        # [(126, 8), (128, 8), alto_three_musicmaker_two],
        # [(128, 8), (130, 8), alto_three_musicmaker_two],
        # [(130, 8), (132, 8), alto_three_musicmaker_two],
        # [(132, 8), (134, 8), alto_three_musicmaker_two],
        # [(134, 8), (136, 8), alto_three_musicmaker_one],
        # [(136, 8), (138, 8), alto_three_musicmaker_one],
        #
        # [(140, 8), (142, 8), alto_three_musicmaker_one],
        # [(142, 8), (144, 8), alto_three_musicmaker_three],
        # [(144, 8), (146, 8), alto_three_musicmaker_one],
        # [(146, 8), (148, 8), alto_three_musicmaker_two],
        # [(148, 8), (150, 8), alto_three_musicmaker_two],
        # [(150, 8), (152, 8), alto_three_musicmaker_three],
        # [(152, 8), (154, 8), alto_three_musicmaker_two],
        # [(154, 8), (156, 8), alto_three_musicmaker_two],
        # [(156, 8), (158, 8), alto_three_musicmaker_two],
        # [(158, 8), (160, 8), alto_three_musicmaker_one],
        # [(160, 8), (162, 8), alto_three_musicmaker_three],
        # [(162, 8), (164, 8), alto_three_musicmaker_one],
        # [(164, 8), (166, 8), alto_three_musicmaker_one],
        # [(166, 8), (168, 8), alto_three_musicmaker_one],
        # [(168, 8), (170, 8), alto_three_musicmaker_one],
        # [(170, 8), (172, 8), alto_three_musicmaker_two],
        #
        # [(174, 8), (176, 8), alto_three_musicmaker_two],
        # [(176, 8), (178, 8), alto_three_musicmaker_two],
        # [(178, 8), (180, 8), alto_three_musicmaker_three],
        # [(180, 8), (182, 8), alto_three_musicmaker_one],
        # [(182, 8), (184, 8), alto_three_musicmaker_one],
        # [(184, 8), (186, 8), alto_three_musicmaker_one],
        #
        # [(188, 8), (190, 8), alto_three_musicmaker_one],
        # [(190, 8), (192, 8), alto_three_musicmaker_two],
        # [(192, 8), (194, 8), alto_three_musicmaker_one],
        # [(194, 8), (196, 8), alto_three_musicmaker_one],
        # [(196, 8), (198, 8), alto_three_musicmaker_one],
        # [(198, 8), (199, 8), alto_three_musicmaker_one],
    ]
])

voice_8_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 8',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), alto_four_musicmaker_two],
        [(2, 8), (4, 8), alto_four_musicmaker_two],
        [(4, 8), (6, 8), alto_four_musicmaker_two],
        [(6, 8), (8, 8), alto_four_musicmaker_one],
        [(8, 8), (10, 8), alto_four_musicmaker_one],
        [(10, 8), (12, 8), alto_four_musicmaker_one],
        [(12, 8), (14, 8), alto_four_musicmaker_two],

        [(16, 8), (18, 8), alto_four_musicmaker_two],
        [(18, 8), (20, 8), alto_four_musicmaker_one],
        [(20, 8), (22, 8), alto_four_musicmaker_three],
        [(22, 8), (24, 8), alto_four_musicmaker_one],
        [(24, 8), (26, 8), alto_four_musicmaker_one],
        [(26, 8), (28, 8), alto_four_musicmaker_two],
        [(28, 8), (30, 8), alto_four_musicmaker_two],

        [(32, 8), (34, 8), alto_four_musicmaker_two],
        [(34, 8), (36, 8), alto_four_musicmaker_one],
        [(36, 8), (38, 8), alto_four_musicmaker_one],
        [(38, 8), (39, 8), alto_four_musicmaker_one],
        [(40, 8), (42, 8), alto_four_musicmaker_one],
        [(42, 8), (44, 8), alto_four_musicmaker_three],
        [(44, 8), (46, 8), alto_four_musicmaker_two],

        [(48, 8), (50, 8), alto_four_musicmaker_two],
        [(50, 8), (52, 8), alto_four_musicmaker_two],
        [(52, 8), (54, 8), alto_four_musicmaker_two],
        [(54, 8), (56, 8), alto_four_musicmaker_one],
        # [(56, 8), (58, 8), alto_four_musicmaker_one],
        # [(58, 8), (60, 8), alto_four_musicmaker_one],
        #
        # [(62, 8), (64, 8), alto_four_musicmaker_one],
        # [(64, 8), (66, 8), alto_four_musicmaker_three],
        # [(66, 8), (68, 8), alto_four_musicmaker_two],
        # [(68, 8), (70, 8), alto_four_musicmaker_two],
        # [(70, 8), (72, 8), alto_four_musicmaker_two],
        # [(72, 8), (74, 8), alto_four_musicmaker_two],
        # [(74, 8), (76, 8), alto_four_musicmaker_three],
        #
        # [(78, 8), (80, 8), alto_four_musicmaker_one],
        # [(80, 8), (82, 8), alto_four_musicmaker_one],
        # [(82, 8), (84, 8), alto_four_musicmaker_one],
        # [(84, 8), (86, 8), alto_four_musicmaker_one],
        #
        # [(90, 8), (92, 8), alto_four_musicmaker_one],
        # [(92, 8), (94, 8), alto_four_musicmaker_two],
        # [(94, 8), (96, 8), alto_four_musicmaker_two],
        # [(96, 8), (98, 8), alto_four_musicmaker_two],
        # [(98, 8), (100, 8), alto_four_musicmaker_two],
        # [(100, 8), (102, 8), alto_four_musicmaker_two],
        # [(102, 8), (104, 8), alto_four_musicmaker_three],
        # [(104, 8), (106, 8), alto_four_musicmaker_two],
        # [(106, 8), (108, 8), alto_four_musicmaker_one],
        # [(108, 8), (110, 8), alto_four_musicmaker_three],
        #
        # [(112, 8), (114, 8), alto_four_musicmaker_one],
        # [(114, 8), (116, 8), alto_four_musicmaker_three],
        # [(116, 8), (118, 8), alto_four_musicmaker_one],
        # [(118, 8), (120, 8), alto_four_musicmaker_one],
        # [(120, 8), (122, 8), alto_four_musicmaker_one],
        # [(122, 8), (124, 8), alto_four_musicmaker_two],
        # [(124, 8), (126, 8), alto_four_musicmaker_two],
        #
        # [(130, 8), (132, 8), alto_four_musicmaker_three],
        # [(132, 8), (134, 8), alto_four_musicmaker_two],
        # [(134, 8), (136, 8), alto_four_musicmaker_two],
        # [(136, 8), (138, 8), alto_four_musicmaker_one],
        # [(138, 8), (140, 8), alto_four_musicmaker_one],
        # [(140, 8), (142, 8), alto_four_musicmaker_one],
        # [(142, 8), (144, 8), alto_four_musicmaker_one],
        # [(144, 8), (146, 8), alto_four_musicmaker_one],
        #
        # [(148, 8), (150, 8), alto_four_musicmaker_two],
        # [(150, 8), (152, 8), alto_four_musicmaker_two],
        # [(152, 8), (154, 8), alto_four_musicmaker_three],
        # [(154, 8), (156, 8), alto_four_musicmaker_two],
        # [(156, 8), (158, 8), alto_four_musicmaker_two],
        # [(158, 8), (160, 8), alto_four_musicmaker_one],
        # [(160, 8), (162, 8), alto_four_musicmaker_one],
        # [(162, 8), (164, 8), alto_four_musicmaker_one],
        # [(164, 8), (166, 8), alto_four_musicmaker_one],
        #
        # [(168, 8), (170, 8), alto_four_musicmaker_two],
        # [(170, 8), (172, 8), alto_four_musicmaker_two],
        # [(172, 8), (174, 8), alto_four_musicmaker_one],
        # [(174, 8), (176, 8), alto_four_musicmaker_three],
        # [(176, 8), (178, 8), alto_four_musicmaker_two],
        # [(178, 8), (180, 8), alto_four_musicmaker_one],
        # [(180, 8), (182, 8), alto_four_musicmaker_one],
        # [(182, 8), (184, 8), alto_four_musicmaker_one],
        # [(184, 8), (186, 8), alto_four_musicmaker_two],
        #
        # [(188, 8), (190, 8), alto_four_musicmaker_two],
        # [(190, 8), (192, 8), alto_four_musicmaker_two],
        # [(192, 8), (194, 8), alto_four_musicmaker_one],
        # [(194, 8), (196, 8), alto_four_musicmaker_one],
        # [(196, 8), (198, 8), alto_four_musicmaker_one],
        # [(198, 8), (199, 8), alto_four_musicmaker_one],
    ]
])

voice_9_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 9',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), alto_five_musicmaker_two],
        [(2, 8), (4, 8), alto_five_musicmaker_one],
        [(4, 8), (6, 8), alto_five_musicmaker_one],
        [(6, 8), (8, 8), alto_five_musicmaker_two],
        [(8, 8), (10, 8), alto_five_musicmaker_three],

        [(12, 8), (14, 8), alto_five_musicmaker_one],
        [(14, 8), (16, 8), alto_five_musicmaker_one],
        [(16, 8), (18, 8), alto_five_musicmaker_one],
        [(18, 8), (20, 8), alto_five_musicmaker_one],
        [(20, 8), (22, 8), alto_five_musicmaker_three],
        [(22, 8), (24, 8), alto_five_musicmaker_two],
        [(24, 8), (26, 8), alto_five_musicmaker_two],

        [(28, 8), (30, 8), alto_five_musicmaker_two],
        [(30, 8), (32, 8), alto_five_musicmaker_three],
        [(32, 8), (34, 8), alto_five_musicmaker_one],
        [(34, 8), (36, 8), alto_five_musicmaker_one],
        [(36, 8), (38, 8), alto_five_musicmaker_one],
        [(38, 8), (40, 8), alto_five_musicmaker_three],
        [(40, 8), (42, 8), alto_five_musicmaker_one],
        [(42, 8), (44, 8), alto_five_musicmaker_two],
        [(44, 8), (46, 8), alto_five_musicmaker_two],

        [(48, 8), (50, 8), alto_five_musicmaker_three],
        [(50, 8), (52, 8), alto_five_musicmaker_two],
        [(52, 8), (54, 8), alto_five_musicmaker_two],
        [(54, 8), (56, 8), alto_five_musicmaker_two],
        # [(56, 8), (58, 8), alto_five_musicmaker_one],
        # [(58, 8), (60, 8), alto_five_musicmaker_one],
        #
        # [(62, 8), (64, 8), alto_five_musicmaker_one],
        # [(64, 8), (66, 8), alto_five_musicmaker_one],
        # [(66, 8), (68, 8), alto_five_musicmaker_one],
        # [(68, 8), (70, 8), alto_five_musicmaker_one],
        # [(70, 8), (72, 8), alto_five_musicmaker_three],
        # [(72, 8), (74, 8), alto_five_musicmaker_two],
        # [(74, 8), (76, 8), alto_five_musicmaker_two],
        # [(76, 8), (78, 8), alto_five_musicmaker_two],
        # [(78, 8), (80, 8), alto_five_musicmaker_three],
        # [(80, 8), (82, 8), alto_five_musicmaker_two],
        # [(82, 8), (84, 8), alto_five_musicmaker_two],
        # [(84, 8), (86, 8), alto_five_musicmaker_two],
        #
        # [(88, 8), (90, 8), alto_five_musicmaker_three],
        # [(90, 8), (92, 8), alto_five_musicmaker_one],
        # [(92, 8), (94, 8), alto_five_musicmaker_one],
        # [(94, 8), (96, 8), alto_five_musicmaker_one],
        # [(96, 8), (98, 8), alto_five_musicmaker_one],
        # [(98, 8), (100, 8), alto_five_musicmaker_one],
        # [(100, 8), (102, 8), alto_five_musicmaker_three],
        # [(102, 8), (104, 8), alto_five_musicmaker_two],
        # [(104, 8), (106, 8), alto_five_musicmaker_two],
        # [(106, 8), (108, 8), alto_five_musicmaker_two],
        # [(108, 8), (110, 8), alto_five_musicmaker_two],
        # [(110, 8), (112, 8), alto_five_musicmaker_three],
        #
        # [(114, 8), (116, 8), alto_five_musicmaker_one],
        # [(116, 8), (118, 8), alto_five_musicmaker_one],
        # [(118, 8), (120, 8), alto_five_musicmaker_three],
        # [(120, 8), (122, 8), alto_five_musicmaker_one],
        # [(122, 8), (124, 8), alto_five_musicmaker_one],
        # [(124, 8), (126, 8), alto_five_musicmaker_two],
        # [(126, 8), (128, 8), alto_five_musicmaker_three],
        # [(128, 8), (130, 8), alto_five_musicmaker_two],
        # [(130, 8), (132, 8), alto_five_musicmaker_two],
        # [(132, 8), (134, 8), alto_five_musicmaker_one],
        # [(134, 8), (136, 8), alto_five_musicmaker_one],
        # [(136, 8), (138, 8), alto_five_musicmaker_three],
        # [(138, 8), (140, 8), alto_five_musicmaker_two],
        # [(140, 8), (142, 8), alto_five_musicmaker_two],
        # [(142, 8), (144, 8), alto_five_musicmaker_one],
        # [(144, 8), (146, 8), alto_five_musicmaker_two],
        # [(146, 8), (148, 8), alto_five_musicmaker_two],
        # [(148, 8), (150, 8), alto_five_musicmaker_three],
        #
        # [(152, 8), (154, 8), alto_five_musicmaker_two],
        # [(154, 8), (156, 8), alto_five_musicmaker_two],
        # [(156, 8), (158, 8), alto_five_musicmaker_three],
        # [(158, 8), (160, 8), alto_five_musicmaker_one],
        # [(160, 8), (162, 8), alto_five_musicmaker_one],
        # [(162, 8), (164, 8), alto_five_musicmaker_one],
        # [(164, 8), (166, 8), alto_five_musicmaker_one],
        #
        # [(168, 8), (170, 8), alto_five_musicmaker_one],
        # [(170, 8), (172, 8), alto_five_musicmaker_one],
        # [(172, 8), (174, 8), alto_five_musicmaker_two],
        # [(174, 8), (176, 8), alto_five_musicmaker_two],
        # [(176, 8), (178, 8), alto_five_musicmaker_two],
        # [(178, 8), (180, 8), alto_five_musicmaker_three],
        # [(180, 8), (182, 8), alto_five_musicmaker_two],
        # [(182, 8), (184, 8), alto_five_musicmaker_two],
        # [(184, 8), (186, 8), alto_five_musicmaker_one],
        # [(186, 8), (188, 8), alto_five_musicmaker_one],
        # [(188, 8), (190, 8), alto_five_musicmaker_three],
        # [(190, 8), (192, 8), alto_five_musicmaker_one],
        # [(192, 8), (194, 8), alto_five_musicmaker_one],
        # [(194, 8), (196, 8), alto_five_musicmaker_one],
        # [(196, 8), (198, 8), alto_five_musicmaker_one],
        # [(198, 8), (199, 8), alto_five_musicmaker_one],
    ]
])

voice_10_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 10',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), alto_six_musicmaker_one],

        [(4, 8), (6, 8), alto_six_musicmaker_three],
        [(6, 8), (8, 8), alto_six_musicmaker_one],
        [(8, 8), (10, 8), alto_six_musicmaker_two],
        [(10, 8), (12, 8), alto_six_musicmaker_three],
        [(12, 8), (14, 8), alto_six_musicmaker_two],
        [(14, 8), (16, 8), alto_six_musicmaker_two],
        [(16, 8), (18, 8), alto_six_musicmaker_one],

        [(20, 8), (22, 8), alto_six_musicmaker_one],
        [(22, 8), (24, 8), alto_six_musicmaker_one],
        [(24, 8), (26, 8), alto_six_musicmaker_one],
        [(26, 8), (28, 8), alto_six_musicmaker_three],
        [(28, 8), (30, 8), alto_six_musicmaker_two],
        [(30, 8), (32, 8), alto_six_musicmaker_two],
        [(32, 8), (34, 8), alto_six_musicmaker_two],
        [(34, 8), (36, 8), alto_six_musicmaker_two],
        [(36, 8), (38, 8), alto_six_musicmaker_three],
        [(38, 8), (40, 8), alto_six_musicmaker_one],
        [(40, 8), (42, 8), alto_six_musicmaker_one],
        [(42, 8), (44, 8), alto_six_musicmaker_one],
        [(44, 8), (46, 8), alto_six_musicmaker_one],
        [(46, 8), (48, 8), alto_six_musicmaker_three],
        [(48, 8), (50, 8), alto_six_musicmaker_one],

        [(52, 8), (54, 8), alto_six_musicmaker_two],
        [(54, 8), (56, 8), alto_six_musicmaker_two],
        # [(56, 8), (58, 8), alto_six_musicmaker_two],
        # [(58, 8), (60, 8), alto_six_musicmaker_three],
        # [(60, 8), (62, 8), alto_six_musicmaker_two],
        # [(62, 8), (64, 8), alto_six_musicmaker_two],
        # [(64, 8), (66, 8), alto_six_musicmaker_two],
        # [(66, 8), (68, 8), alto_six_musicmaker_one],
        # [(68, 8), (70, 8), alto_six_musicmaker_one],
        # [(70, 8), (72, 8), alto_six_musicmaker_three],
        # [(72, 8), (74, 8), alto_six_musicmaker_one],
        # [(74, 8), (76, 8), alto_six_musicmaker_one],
        # [(76, 8), (78, 8), alto_six_musicmaker_one],
        # [(78, 8), (80, 8), alto_six_musicmaker_two],
        # [(80, 8), (82, 8), alto_six_musicmaker_two],
        # [(82, 8), (84, 8), alto_six_musicmaker_two],
        # [(84, 8), (86, 8), alto_six_musicmaker_three],
        # [(86, 8), (88, 8), alto_six_musicmaker_two],
        # [(88, 8), (90, 8), alto_six_musicmaker_one],
        # [(90, 8), (92, 8), alto_six_musicmaker_one],
        #
        # [(94, 8), (96, 8), alto_six_musicmaker_one],
        # [(96, 8), (98, 8), alto_six_musicmaker_two],
        # [(98, 8), (100, 8), alto_six_musicmaker_three],
        # [(100, 8), (102, 8), alto_six_musicmaker_two],
        # [(102, 8), (104, 8), alto_six_musicmaker_one],
        # [(104, 8), (106, 8), alto_six_musicmaker_one],
        # [(106, 8), (108, 8), alto_six_musicmaker_one],
        # [(108, 8), (110, 8), alto_six_musicmaker_two],
        #
        # [(112, 8), (114, 8), alto_six_musicmaker_one],
        # [(114, 8), (116, 8), alto_six_musicmaker_one],
        # [(116, 8), (118, 8), alto_six_musicmaker_two],
        # [(118, 8), (120, 8), alto_six_musicmaker_two],
        # [(120, 8), (122, 8), alto_six_musicmaker_two],
        # [(122, 8), (124, 8), alto_six_musicmaker_three],
        # [(124, 8), (126, 8), alto_six_musicmaker_two],
        # [(126, 8), (128, 8), alto_six_musicmaker_one],
        #
        # [(130, 8), (132, 8), alto_six_musicmaker_one],
        # [(132, 8), (134, 8), alto_six_musicmaker_three],
        # [(134, 8), (136, 8), alto_six_musicmaker_one],
        # [(136, 8), (138, 8), alto_six_musicmaker_two],
        # [(138, 8), (140, 8), alto_six_musicmaker_two],
        # [(140, 8), (142, 8), alto_six_musicmaker_two],
        # [(142, 8), (144, 8), alto_six_musicmaker_three],
        #
        # [(148, 8), (150, 8), alto_six_musicmaker_two],
        # [(150, 8), (152, 8), alto_six_musicmaker_three],
        # [(152, 8), (154, 8), alto_six_musicmaker_one],
        # [(154, 8), (156, 8), alto_six_musicmaker_one],
        # [(156, 8), (158, 8), alto_six_musicmaker_one],
        # [(158, 8), (160, 8), alto_six_musicmaker_three],
        # [(160, 8), (162, 8), alto_six_musicmaker_two],
        # [(162, 8), (164, 8), alto_six_musicmaker_two],
        # [(164, 8), (166, 8), alto_six_musicmaker_three],
        #
        # [(168, 8), (170, 8), alto_six_musicmaker_two],
        # [(170, 8), (172, 8), alto_six_musicmaker_three],
        # [(172, 8), (174, 8), alto_six_musicmaker_one],
        # [(174, 8), (176, 8), alto_six_musicmaker_three],
        # [(176, 8), (178, 8), alto_six_musicmaker_one],
        # [(178, 8), (180, 8), alto_six_musicmaker_three],
        #
        # [(182, 8), (184, 8), alto_six_musicmaker_two],
        # [(184, 8), (186, 8), alto_six_musicmaker_two],
        # [(186, 8), (188, 8), alto_six_musicmaker_two],
        # [(188, 8), (190, 8), alto_six_musicmaker_one],
        # [(190, 8), (192, 8), alto_six_musicmaker_one],
        # [(192, 8), (194, 8), alto_six_musicmaker_one],
        # [(194, 8), (196, 8), alto_six_musicmaker_one],
        #
        # [(198, 8), (199, 8), alto_six_musicmaker_one],
    ]
])

voice_11_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 11',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), tenor_one_musicmaker_one],
        [(2, 8), (4, 8), tenor_one_musicmaker_one],
        [(4, 8), (6, 8), tenor_one_musicmaker_two],
        [(6, 8), (8, 8), tenor_one_musicmaker_two],
        [(8, 8), (10, 8), tenor_one_musicmaker_three],
        [(10, 8), (12, 8), tenor_one_musicmaker_one],
        [(12, 8), (14, 8), tenor_one_musicmaker_one],

        [(16, 8), (18, 8), tenor_one_musicmaker_one],
        [(18, 8), (20, 8), tenor_one_musicmaker_two],
        [(20, 8), (22, 8), tenor_one_musicmaker_two],
        [(22, 8), (24, 8), tenor_one_musicmaker_three],
        [(24, 8), (26, 8), tenor_one_musicmaker_two],
        [(26, 8), (28, 8), tenor_one_musicmaker_one],
        [(28, 8), (30, 8), tenor_one_musicmaker_one],
        [(30, 8), (32, 8), tenor_one_musicmaker_one],
        [(32, 8), (34, 8), tenor_one_musicmaker_one],
        [(34, 8), (36, 8), tenor_one_musicmaker_one],
        [(36, 8), (38, 8), tenor_one_musicmaker_two],

        [(40, 8), (42, 8), tenor_one_musicmaker_three],
        [(42, 8), (44, 8), tenor_one_musicmaker_two],
        [(44, 8), (46, 8), tenor_one_musicmaker_one],
        [(46, 8), (48, 8), tenor_one_musicmaker_one],
        [(48, 8), (50, 8), tenor_one_musicmaker_one],
        [(50, 8), (52, 8), tenor_one_musicmaker_one],
        [(52, 8), (54, 8), tenor_one_musicmaker_two],
        [(54, 8), (56, 8), tenor_one_musicmaker_two],
        # [(56, 8), (58, 8), tenor_one_musicmaker_three],
        # [(58, 8), (60, 8), tenor_one_musicmaker_one],
        # [(60, 8), (62, 8), tenor_one_musicmaker_one],
        # [(62, 8), (64, 8), tenor_one_musicmaker_one],
        # [(64, 8), (66, 8), tenor_one_musicmaker_two],
        # [(66, 8), (68, 8), tenor_one_musicmaker_two],
        #
        # [(70, 8), (72, 8), tenor_one_musicmaker_two],
        # [(72, 8), (74, 8), tenor_one_musicmaker_two],
        # [(74, 8), (76, 8), tenor_one_musicmaker_two],
        # [(76, 8), (78, 8), tenor_one_musicmaker_one],
        #
        # [(80, 8), (82, 8), tenor_one_musicmaker_one],
        # [(82, 8), (84, 8), tenor_one_musicmaker_one],
        # [(84, 8), (86, 8), tenor_one_musicmaker_two],
        # [(86, 8), (88, 8), tenor_one_musicmaker_two],
        # [(88, 8), (90, 8), tenor_one_musicmaker_three],
        # [(90, 8), (92, 8), tenor_one_musicmaker_two],
        # [(92, 8), (94, 8), tenor_one_musicmaker_two],
        # [(94, 8), (96, 8), tenor_one_musicmaker_two],
        # [(96, 8), (98, 8), tenor_one_musicmaker_two],
        # [(98, 8), (100, 8), tenor_one_musicmaker_one],
        # [(100, 8), (102, 8), tenor_one_musicmaker_one],
        # [(102, 8), (104, 8), tenor_one_musicmaker_two],
        # [(104, 8), (106, 8), tenor_one_musicmaker_one],
        # [(106, 8), (108, 8), tenor_one_musicmaker_one],
        # [(108, 8), (110, 8), tenor_one_musicmaker_one],
        # [(110, 8), (112, 8), tenor_one_musicmaker_one],
        # [(112, 8), (114, 8), tenor_one_musicmaker_two],
        # [(114, 8), (116, 8), tenor_one_musicmaker_two],
        # [(116, 8), (118, 8), tenor_one_musicmaker_three],
        #
        # [(120, 8), (122, 8), tenor_one_musicmaker_two],
        # [(122, 8), (124, 8), tenor_one_musicmaker_one],
        # [(124, 8), (126, 8), tenor_one_musicmaker_one],
        # [(126, 8), (128, 8), tenor_one_musicmaker_one],
        # [(128, 8), (130, 8), tenor_one_musicmaker_one],
        # [(130, 8), (132, 8), tenor_one_musicmaker_one],
        # [(132, 8), (134, 8), tenor_one_musicmaker_two],
        # [(134, 8), (136, 8), tenor_one_musicmaker_two],
        # [(136, 8), (138, 8), tenor_one_musicmaker_two],
        # [(138, 8), (140, 8), tenor_one_musicmaker_three],
        # [(140, 8), (142, 8), tenor_one_musicmaker_two],
        # [(142, 8), (144, 8), tenor_one_musicmaker_two],
        # [(144, 8), (146, 8), tenor_one_musicmaker_two],
        # [(146, 8), (148, 8), tenor_one_musicmaker_two],
        # [(148, 8), (150, 8), tenor_one_musicmaker_one],
        # [(150, 8), (152, 8), tenor_one_musicmaker_one],
        # [(152, 8), (154, 8), tenor_one_musicmaker_one],
        #
        # [(156, 8), (158, 8), tenor_one_musicmaker_two],
        # [(158, 8), (160, 8), tenor_one_musicmaker_two],
        # [(160, 8), (162, 8), tenor_one_musicmaker_three],
        # [(162, 8), (164, 8), tenor_one_musicmaker_two],
        # [(164, 8), (166, 8), tenor_one_musicmaker_one],
        # [(166, 8), (168, 8), tenor_one_musicmaker_one],
        #
        # [(170, 8), (172, 8), tenor_one_musicmaker_one],
        # [(172, 8), (174, 8), tenor_one_musicmaker_one],
        # [(174, 8), (176, 8), tenor_one_musicmaker_two],
        # [(176, 8), (178, 8), tenor_one_musicmaker_two],
        # [(178, 8), (180, 8), tenor_one_musicmaker_three],
        # [(180, 8), (182, 8), tenor_one_musicmaker_two],
        # [(182, 8), (184, 8), tenor_one_musicmaker_two],
        # [(184, 8), (186, 8), tenor_one_musicmaker_two],
        # [(186, 8), (188, 8), tenor_one_musicmaker_two],
        # [(188, 8), (190, 8), tenor_one_musicmaker_one],
        # [(190, 8), (192, 8), tenor_one_musicmaker_one],
        # [(192, 8), (194, 8), tenor_one_musicmaker_one],
        # [(194, 8), (196, 8), tenor_one_musicmaker_one],
        # [(196, 8), (198, 8), tenor_one_musicmaker_one],
        # [(198, 8), (199, 8), tenor_one_musicmaker_one],
    ]
])

voice_12_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 12',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), tenor_two_musicmaker_two],
        [(2, 8), (4, 8), tenor_two_musicmaker_one],
        [(4, 8), (6, 8), tenor_two_musicmaker_one],
        [(6, 8), (8, 8), tenor_two_musicmaker_one],
        [(8, 8), (10, 8), tenor_two_musicmaker_two],
        [(10, 8), (12, 8), tenor_two_musicmaker_one],
        [(12, 8), (14, 8), tenor_two_musicmaker_one],
        [(14, 8), (16, 8), tenor_two_musicmaker_two],
        [(16, 8), (18, 8), tenor_two_musicmaker_three],
        [(18, 8), (20, 8), tenor_two_musicmaker_two],

        [(22, 8), (24, 8), tenor_two_musicmaker_two],
        [(24, 8), (26, 8), tenor_two_musicmaker_two],
        [(26, 8), (28, 8), tenor_two_musicmaker_two],
        [(28, 8), (30, 8), tenor_two_musicmaker_one],
        [(30, 8), (32, 8), tenor_two_musicmaker_one],
        [(32, 8), (34, 8), tenor_two_musicmaker_three],
        [(34, 8), (36, 8), tenor_two_musicmaker_one],
        [(36, 8), (38, 8), tenor_two_musicmaker_one],
        [(38, 8), (39, 8), tenor_two_musicmaker_one],
        [(40, 8), (42, 8), tenor_two_musicmaker_one],
        [(42, 8), (44, 8), tenor_two_musicmaker_two],

        [(46, 8), (48, 8), tenor_two_musicmaker_two],
        [(48, 8), (50, 8), tenor_two_musicmaker_one],
        [(51, 8), (52, 8), tenor_two_musicmaker_one],
        [(52, 8), (54, 8), tenor_two_musicmaker_three],
        [(54, 8), (56, 8), tenor_two_musicmaker_two],
        # [(56, 8), (58, 8), tenor_two_musicmaker_two],
        # [(58, 8), (60, 8), tenor_two_musicmaker_two],
        # [(60, 8), (62, 8), tenor_two_musicmaker_two],
        # [(62, 8), (64, 8), tenor_two_musicmaker_one],
        # [(64, 8), (66, 8), tenor_two_musicmaker_one],
        # [(66, 8), (68, 8), tenor_two_musicmaker_three],
        # [(68, 8), (70, 8), tenor_two_musicmaker_one],
        #
        # [(72, 8), (74, 8), tenor_two_musicmaker_two],
        # [(74, 8), (76, 8), tenor_two_musicmaker_two],
        # [(76, 8), (78, 8), tenor_two_musicmaker_two],
        # [(78, 8), (80, 8), tenor_two_musicmaker_two],
        # [(80, 8), (82, 8), tenor_two_musicmaker_two],
        # [(82, 8), (84, 8), tenor_two_musicmaker_one],
        # [(84, 8), (86, 8), tenor_two_musicmaker_two],
        # [(86, 8), (88, 8), tenor_two_musicmaker_one],
        # [(88, 8), (90, 8), tenor_two_musicmaker_one],
        # [(90, 8), (92, 8), tenor_two_musicmaker_three],
        # [(92, 8), (94, 8), tenor_two_musicmaker_one],
        # [(94, 8), (96, 8), tenor_two_musicmaker_one],
        # [(96, 8), (98, 8), tenor_two_musicmaker_one],
        #
        # [(100, 8), (102, 8), tenor_two_musicmaker_two],
        # [(102, 8), (104, 8), tenor_two_musicmaker_two],
        # [(104, 8), (106, 8), tenor_two_musicmaker_two],
        # [(106, 8), (108, 8), tenor_two_musicmaker_one],
        # [(108, 8), (110, 8), tenor_two_musicmaker_one],
        # [(110, 8), (112, 8), tenor_two_musicmaker_three],
        # [(112, 8), (114, 8), tenor_two_musicmaker_one],
        # [(114, 8), (116, 8), tenor_two_musicmaker_two],
        # [(116, 8), (118, 8), tenor_two_musicmaker_two],
        # [(118, 8), (120, 8), tenor_two_musicmaker_two],
        #
        # [(122, 8), (124, 8), tenor_two_musicmaker_one],
        # [(124, 8), (126, 8), tenor_two_musicmaker_three],
        # [(126, 8), (128, 8), tenor_two_musicmaker_one],
        # [(128, 8), (130, 8), tenor_two_musicmaker_two],
        # [(130, 8), (132, 8), tenor_two_musicmaker_two],
        # [(132, 8), (134, 8), tenor_two_musicmaker_three],
        # [(134, 8), (136, 8), tenor_two_musicmaker_two],
        # [(136, 8), (138, 8), tenor_two_musicmaker_two],
        # [(138, 8), (140, 8), tenor_two_musicmaker_two],
        # [(140, 8), (142, 8), tenor_two_musicmaker_two],
        # [(142, 8), (144, 8), tenor_two_musicmaker_one],
        # [(144, 8), (146, 8), tenor_two_musicmaker_one],
        # [(146, 8), (148, 8), tenor_two_musicmaker_three],
        # [(148, 8), (150, 8), tenor_two_musicmaker_one],
        #
        # [(152, 8), (154, 8), tenor_two_musicmaker_one],
        # [(154, 8), (156, 8), tenor_two_musicmaker_two],
        # [(156, 8), (158, 8), tenor_two_musicmaker_two],
        # [(158, 8), (160, 8), tenor_two_musicmaker_two],
        # [(160, 8), (162, 8), tenor_two_musicmaker_two],
        # [(162, 8), (164, 8), tenor_two_musicmaker_one],
        # [(164, 8), (166, 8), tenor_two_musicmaker_one],
        # [(166, 8), (168, 8), tenor_two_musicmaker_three],
        # [(168, 8), (170, 8), tenor_two_musicmaker_one],
        # [(170, 8), (172, 8), tenor_two_musicmaker_one],
        # [(172, 8), (174, 8), tenor_two_musicmaker_one],
        # [(174, 8), (176, 8), tenor_two_musicmaker_two],
        # [(176, 8), (178, 8), tenor_two_musicmaker_two],
        # [(178, 8), (180, 8), tenor_two_musicmaker_two],
        #
        # [(182, 8), (184, 8), tenor_two_musicmaker_one],
        # [(184, 8), (186, 8), tenor_two_musicmaker_three],
        # [(186, 8), (188, 8), tenor_two_musicmaker_two],
        # [(188, 8), (190, 8), tenor_two_musicmaker_two],
        # [(190, 8), (192, 8), tenor_two_musicmaker_two],
        # [(192, 8), (194, 8), tenor_two_musicmaker_one],
        # [(194, 8), (196, 8), tenor_two_musicmaker_one],
        # [(196, 8), (198, 8), tenor_two_musicmaker_one],
        # [(198, 8), (199, 8), tenor_two_musicmaker_one],
    ]
])

voice_13_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 13',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), tenor_three_musicmaker_three],
        [(2, 8), (4, 8), tenor_three_musicmaker_one],
        [(4, 8), (6, 8), tenor_three_musicmaker_three],
        [(6, 8), (8, 8), tenor_three_musicmaker_one],
        [(8, 8), (10, 8), tenor_three_musicmaker_one],
        [(10, 8), (12, 8), tenor_three_musicmaker_three],
        [(12, 8), (14, 8), tenor_three_musicmaker_two],
        [(14, 8), (16, 8), tenor_three_musicmaker_two],

        [(18, 8), (20, 8), tenor_three_musicmaker_three],
        [(20, 8), (22, 8), tenor_three_musicmaker_two],
        [(22, 8), (24, 8), tenor_three_musicmaker_two],
        [(24, 8), (26, 8), tenor_three_musicmaker_one],
        [(26, 8), (28, 8), tenor_three_musicmaker_one],
        [(28, 8), (30, 8), tenor_three_musicmaker_three],
        [(30, 8), (32, 8), tenor_three_musicmaker_two],
        [(32, 8), (34, 8), tenor_three_musicmaker_two],
        [(34, 8), (36, 8), tenor_three_musicmaker_two],

        [(38, 8), (40, 8), tenor_three_musicmaker_one],
        [(40, 8), (42, 8), tenor_three_musicmaker_three],
        [(42, 8), (44, 8), tenor_three_musicmaker_one],
        [(44, 8), (46, 8), tenor_three_musicmaker_one],
        [(46, 8), (48, 8), tenor_three_musicmaker_one],

        [(50, 8), (52, 8), tenor_three_musicmaker_three],
        [(52, 8), (54, 8), tenor_three_musicmaker_two],
        [(54, 8), (56, 8), tenor_three_musicmaker_two],
        # [(56, 8), (58, 8), tenor_three_musicmaker_two],
        # [(58, 8), (60, 8), tenor_three_musicmaker_three],
        # [(60, 8), (62, 8), tenor_three_musicmaker_two],
        # [(62, 8), (64, 8), tenor_three_musicmaker_one],
        # [(64, 8), (66, 8), tenor_three_musicmaker_three],
        #
        # [(68, 8), (70, 8), tenor_three_musicmaker_three],
        # [(70, 8), (72, 8), tenor_three_musicmaker_three],
        # [(72, 8), (74, 8), tenor_three_musicmaker_two],
        # [(74, 8), (76, 8), tenor_three_musicmaker_two],
        # [(76, 8), (78, 8), tenor_three_musicmaker_three],
        # [(78, 8), (80, 8), tenor_three_musicmaker_two],
        # [(80, 8), (82, 8), tenor_three_musicmaker_two],
        # [(82, 8), (84, 8), tenor_three_musicmaker_two],
        # [(84, 8), (86, 8), tenor_three_musicmaker_three],
        # [(86, 8), (88, 8), tenor_three_musicmaker_one],
        # [(88, 8), (90, 8), tenor_three_musicmaker_one],
        # [(90, 8), (92, 8), tenor_three_musicmaker_one],
        #
        # [(94, 8), (96, 8), tenor_three_musicmaker_three],
        # [(96, 8), (98, 8), tenor_three_musicmaker_two],
        # [(98, 8), (100, 8), tenor_three_musicmaker_two],
        # [(100, 8), (102, 8), tenor_three_musicmaker_two],
        # [(102, 8), (104, 8), tenor_three_musicmaker_two],
        # [(104, 8), (106, 8), tenor_three_musicmaker_one],
        # [(106, 8), (108, 8), tenor_three_musicmaker_three],
        # [(108, 8), (110, 8), tenor_three_musicmaker_one],
        #
        # [(112, 8), (114, 8), tenor_three_musicmaker_two],
        # [(114, 8), (116, 8), tenor_three_musicmaker_two],
        # [(116, 8), (118, 8), tenor_three_musicmaker_two],
        # [(118, 8), (120, 8), tenor_three_musicmaker_two],
        # [(120, 8), (122, 8), tenor_three_musicmaker_three],
        # [(122, 8), (124, 8), tenor_three_musicmaker_two],
        # [(124, 8), (126, 8), tenor_three_musicmaker_one],
        # [(126, 8), (128, 8), tenor_three_musicmaker_one],
        # [(128, 8), (130, 8), tenor_three_musicmaker_one],
        #
        # [(132, 8), (134, 8), tenor_three_musicmaker_three],
        # [(134, 8), (136, 8), tenor_three_musicmaker_one],
        # [(136, 8), (138, 8), tenor_three_musicmaker_one],
        # [(138, 8), (140, 8), tenor_three_musicmaker_two],
        # [(140, 8), (142, 8), tenor_three_musicmaker_two],
        # [(142, 8), (144, 8), tenor_three_musicmaker_three],
        # [(144, 8), (146, 8), tenor_three_musicmaker_two],
        # [(146, 8), (148, 8), tenor_three_musicmaker_one],
        # [(148, 8), (150, 8), tenor_three_musicmaker_two],
        #
        # [(152, 8), (154, 8), tenor_three_musicmaker_two],
        # [(154, 8), (156, 8), tenor_three_musicmaker_one],
        # [(156, 8), (158, 8), tenor_three_musicmaker_three],
        # [(158, 8), (160, 8), tenor_three_musicmaker_two],
        # [(160, 8), (162, 8), tenor_three_musicmaker_three],
        # [(162, 8), (164, 8), tenor_three_musicmaker_two],
        # [(164, 8), (166, 8), tenor_three_musicmaker_two],
        # [(166, 8), (168, 8), tenor_three_musicmaker_one],
        # [(168, 8), (170, 8), tenor_three_musicmaker_one],
        # [(170, 8), (172, 8), tenor_three_musicmaker_three],
        #
        # [(174, 8), (176, 8), tenor_three_musicmaker_one],
        # [(176, 8), (178, 8), tenor_three_musicmaker_two],
        # [(178, 8), (180, 8), tenor_three_musicmaker_two],
        # [(180, 8), (182, 8), tenor_three_musicmaker_two],
        # [(182, 8), (184, 8), tenor_three_musicmaker_one],
        # [(184, 8), (186, 8), tenor_three_musicmaker_one],
        # [(186, 8), (188, 8), tenor_three_musicmaker_three],
        # [(188, 8), (190, 8), tenor_three_musicmaker_one],
        # [(190, 8), (192, 8), tenor_three_musicmaker_two],
        #
        # [(194, 8), (196, 8), tenor_three_musicmaker_one],
        # [(196, 8), (198, 8), tenor_three_musicmaker_one],
        # [(198, 8), (199, 8), tenor_three_musicmaker_one],
    ]
])

voice_14_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 14',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), tenor_four_musicmaker_two],
        [(2, 8), (4, 8), tenor_four_musicmaker_two],
        [(4, 8), (6, 8), tenor_four_musicmaker_two],
        [(6, 8), (8, 8), tenor_four_musicmaker_two],
        [(8, 8), (10, 8), tenor_four_musicmaker_two],
        [(10, 8), (12, 8), tenor_four_musicmaker_one],
        [(12, 8), (14, 8), tenor_four_musicmaker_two],
        [(14, 8), (16, 8), tenor_four_musicmaker_two],
        [(16, 8), (18, 8), tenor_four_musicmaker_one],

        [(22, 8), (24, 8), tenor_four_musicmaker_one],
        [(24, 8), (26, 8), tenor_four_musicmaker_three],
        [(26, 8), (28, 8), tenor_four_musicmaker_one],
        [(28, 8), (30, 8), tenor_four_musicmaker_one],
        [(30, 8), (32, 8), tenor_four_musicmaker_one],
        [(32, 8), (34, 8), tenor_four_musicmaker_two],
        [(34, 8), (36, 8), tenor_four_musicmaker_two],
        [(36, 8), (38, 8), tenor_four_musicmaker_two],
        [(38, 8), (40, 8), tenor_four_musicmaker_three],
        [(40, 8), (42, 8), tenor_four_musicmaker_two],

        [(46, 8), (48, 8), tenor_four_musicmaker_two],
        [(48, 8), (50, 8), tenor_four_musicmaker_one],
        [(50, 8), (52, 8), tenor_four_musicmaker_three],
        [(52, 8), (54, 8), tenor_four_musicmaker_one],
        [(54, 8), (56, 8), tenor_four_musicmaker_one],
        # [(56, 8), (58, 8), tenor_four_musicmaker_one],
        # [(58, 8), (60, 8), tenor_four_musicmaker_one],
        # [(60, 8), (62, 8), tenor_four_musicmaker_one],
        # [(62, 8), (64, 8), tenor_four_musicmaker_two],
        # [(64, 8), (66, 8), tenor_four_musicmaker_two],
        # [(66, 8), (68, 8), tenor_four_musicmaker_one],
        # [(68, 8), (70, 8), tenor_four_musicmaker_two],
        #
        # [(72, 8), (74, 8), tenor_four_musicmaker_two],
        # [(74, 8), (76, 8), tenor_four_musicmaker_one],
        # [(76, 8), (78, 8), tenor_four_musicmaker_three],
        # [(78, 8), (80, 8), tenor_four_musicmaker_one],
        # [(80, 8), (82, 8), tenor_four_musicmaker_one],
        # [(82, 8), (84, 8), tenor_four_musicmaker_one],
        #
        # [(88, 8), (90, 8), tenor_four_musicmaker_two],
        # [(90, 8), (92, 8), tenor_four_musicmaker_two],
        # [(92, 8), (94, 8), tenor_four_musicmaker_one],
        # [(94, 8), (96, 8), tenor_four_musicmaker_three],
        # [(96, 8), (98, 8), tenor_four_musicmaker_one],
        # [(98, 8), (100, 8), tenor_four_musicmaker_two],
        # [(100, 8), (102, 8), tenor_four_musicmaker_two],
        # [(102, 8), (104, 8), tenor_four_musicmaker_one],
        # [(104, 8), (106, 8), tenor_four_musicmaker_two],
        # [(106, 8), (108, 8), tenor_four_musicmaker_one],
        #
        # [(110, 8), (112, 8), tenor_four_musicmaker_two],
        # [(112, 8), (114, 8), tenor_four_musicmaker_two],
        # [(114, 8), (116, 8), tenor_four_musicmaker_two],
        # [(116, 8), (118, 8), tenor_four_musicmaker_one],
        # [(118, 8), (120, 8), tenor_four_musicmaker_three],
        # [(120, 8), (122, 8), tenor_four_musicmaker_one],
        # [(122, 8), (124, 8), tenor_four_musicmaker_one],
        # [(124, 8), (126, 8), tenor_four_musicmaker_two],
        #
        # [(128, 8), (130, 8), tenor_four_musicmaker_two],
        # [(130, 8), (132, 8), tenor_four_musicmaker_two],
        # [(132, 8), (134, 8), tenor_four_musicmaker_two],
        # [(134, 8), (136, 8), tenor_four_musicmaker_one],
        # [(136, 8), (138, 8), tenor_four_musicmaker_three],
        # [(138, 8), (140, 8), tenor_four_musicmaker_one],
        # [(140, 8), (142, 8), tenor_four_musicmaker_one],
        # [(142, 8), (144, 8), tenor_four_musicmaker_one],
        # [(144, 8), (146, 8), tenor_four_musicmaker_one],
        # [(146, 8), (148, 8), tenor_four_musicmaker_two],
        #
        # [(150, 8), (152, 8), tenor_four_musicmaker_one],
        # [(152, 8), (154, 8), tenor_four_musicmaker_two],
        # [(154, 8), (156, 8), tenor_four_musicmaker_two],
        # [(156, 8), (158, 8), tenor_four_musicmaker_two],
        # [(158, 8), (160, 8), tenor_four_musicmaker_two],
        # [(160, 8), (162, 8), tenor_four_musicmaker_one],
        # [(162, 8), (164, 8), tenor_four_musicmaker_three],
        # [(164, 8), (166, 8), tenor_four_musicmaker_one],
        # [(166, 8), (168, 8), tenor_four_musicmaker_one],
        #
        # [(170, 8), (172, 8), tenor_four_musicmaker_one],
        # [(172, 8), (174, 8), tenor_four_musicmaker_one],
        #
        # [(178, 8), (180, 8), tenor_four_musicmaker_two],
        # [(180, 8), (182, 8), tenor_four_musicmaker_two],
        # [(182, 8), (184, 8), tenor_four_musicmaker_two],
        # [(184, 8), (186, 8), tenor_four_musicmaker_two],
        # [(186, 8), (188, 8), tenor_four_musicmaker_two],
        # [(188, 8), (190, 8), tenor_four_musicmaker_three],
        # [(190, 8), (192, 8), tenor_four_musicmaker_two],
        # [(192, 8), (194, 8), tenor_four_musicmaker_one],
        # [(194, 8), (196, 8), tenor_four_musicmaker_one],
        # [(196, 8), (198, 8), tenor_four_musicmaker_one],
        # [(198, 8), (199, 8), tenor_four_musicmaker_one],
    ]
])

voice_15_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 15',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), tenor_five_musicmaker_two],
        [(2, 8), (4, 8), tenor_five_musicmaker_two],
        [(4, 8), (6, 8), tenor_five_musicmaker_two],
        [(6, 8), (8, 8), tenor_five_musicmaker_one],
        [(8, 8), (10, 8), tenor_five_musicmaker_three],
        [(10, 8), (12, 8), tenor_five_musicmaker_one],

        [(14, 8), (16, 8), tenor_five_musicmaker_two],
        [(16, 8), (18, 8), tenor_five_musicmaker_two],
        [(18, 8), (20, 8), tenor_five_musicmaker_three],
        [(20, 8), (22, 8), tenor_five_musicmaker_one],
        [(22, 8), (24, 8), tenor_five_musicmaker_one],
        [(24, 8), (26, 8), tenor_five_musicmaker_one],
        [(26, 8), (28, 8), tenor_five_musicmaker_one],
        [(28, 8), (30, 8), tenor_five_musicmaker_three],

        [(32, 8), (34, 8), tenor_five_musicmaker_two],
        [(34, 8), (36, 8), tenor_five_musicmaker_one],
        [(36, 8), (38, 8), tenor_five_musicmaker_one],
        [(38, 8), (40, 8), tenor_five_musicmaker_three],
        [(40, 8), (42, 8), tenor_five_musicmaker_one],
        [(42, 8), (44, 8), tenor_five_musicmaker_two],
        [(44, 8), (46, 8), tenor_five_musicmaker_two],

        [(50, 8), (52, 8), tenor_five_musicmaker_one],
        [(52, 8), (54, 8), tenor_five_musicmaker_one],
        [(54, 8), (56, 8), tenor_five_musicmaker_one],
        # [(56, 8), (58, 8), tenor_five_musicmaker_one],
        # [(58, 8), (60, 8), tenor_five_musicmaker_three],
        # [(60, 8), (62, 8), tenor_five_musicmaker_one],
        # [(62, 8), (64, 8), tenor_five_musicmaker_one],
        # [(64, 8), (66, 8), tenor_five_musicmaker_one],
        # [(66, 8), (68, 8), tenor_five_musicmaker_one],
        #
        # [(70, 8), (72, 8), tenor_five_musicmaker_one],
        # [(72, 8), (74, 8), tenor_five_musicmaker_one],
        # [(74, 8), (76, 8), tenor_five_musicmaker_two],
        # [(76, 8), (78, 8), tenor_five_musicmaker_two],
        # [(78, 8), (80, 8), tenor_five_musicmaker_three],
        # [(80, 8), (82, 8), tenor_five_musicmaker_two],
        # [(82, 8), (84, 8), tenor_five_musicmaker_two],
        # [(84, 8), (86, 8), tenor_five_musicmaker_two],
        # [(86, 8), (88, 8), tenor_five_musicmaker_two],
        # [(88, 8), (90, 8), tenor_five_musicmaker_three],
        #
        # [(92, 8), (94, 8), tenor_five_musicmaker_one],
        # [(94, 8), (96, 8), tenor_five_musicmaker_one],
        # [(96, 8), (98, 8), tenor_five_musicmaker_one],
        # [(98, 8), (100, 8), tenor_five_musicmaker_three],
        # [(100, 8), (102, 8), tenor_five_musicmaker_one],
        # [(102, 8), (104, 8), tenor_five_musicmaker_one],
        # [(104, 8), (106, 8), tenor_five_musicmaker_two],
        # [(106, 8), (108, 8), tenor_five_musicmaker_two],
        # [(108, 8), (110, 8), tenor_five_musicmaker_three],
        # [(110, 8), (112, 8), tenor_five_musicmaker_two],
        # [(112, 8), (114, 8), tenor_five_musicmaker_two],
        #
        # [(116, 8), (118, 8), tenor_five_musicmaker_two],
        # [(118, 8), (120, 8), tenor_five_musicmaker_three],
        # [(120, 8), (122, 8), tenor_five_musicmaker_one],
        # [(122, 8), (124, 8), tenor_five_musicmaker_one],
        # [(124, 8), (126, 8), tenor_five_musicmaker_one],
        # [(126, 8), (128, 8), tenor_five_musicmaker_one],
        # [(128, 8), (130, 8), tenor_five_musicmaker_three],
        # [(130, 8), (132, 8), tenor_five_musicmaker_one],
        #
        # [(134, 8), (136, 8), tenor_five_musicmaker_two],
        # [(136, 8), (138, 8), tenor_five_musicmaker_two],
        # [(138, 8), (140, 8), tenor_five_musicmaker_three],
        # [(140, 8), (142, 8), tenor_five_musicmaker_two],
        # [(142, 8), (144, 8), tenor_five_musicmaker_two],
        # [(144, 8), (146, 8), tenor_five_musicmaker_two],
        # [(146, 8), (148, 8), tenor_five_musicmaker_two],
        # [(148, 8), (150, 8), tenor_five_musicmaker_three],
        # [(150, 8), (152, 8), tenor_five_musicmaker_two],
        #
        # [(154, 8), (156, 8), tenor_five_musicmaker_one],
        # [(156, 8), (158, 8), tenor_five_musicmaker_one],
        # [(158, 8), (160, 8), tenor_five_musicmaker_three],
        # [(160, 8), (162, 8), tenor_five_musicmaker_two],
        # [(162, 8), (164, 8), tenor_five_musicmaker_two],
        # [(164, 8), (166, 8), tenor_five_musicmaker_one],
        # [(166, 8), (168, 8), tenor_five_musicmaker_one],
        # [(168, 8), (170, 8), tenor_five_musicmaker_three],
        # [(170, 8), (172, 8), tenor_five_musicmaker_two],
        #
        # [(174, 8), (176, 8), tenor_five_musicmaker_two],
        # [(176, 8), (178, 8), tenor_five_musicmaker_one],
        # [(178, 8), (180, 8), tenor_five_musicmaker_three],
        # [(180, 8), (182, 8), tenor_five_musicmaker_two],
        # [(182, 8), (184, 8), tenor_five_musicmaker_two],
        # [(184, 8), (186, 8), tenor_five_musicmaker_two],
        # [(186, 8), (188, 8), tenor_five_musicmaker_two],
        # [(188, 8), (190, 8), tenor_five_musicmaker_one],
        #
        # [(192, 8), (194, 8), tenor_five_musicmaker_one],
        # [(194, 8), (196, 8), tenor_five_musicmaker_one],
        # [(196, 8), (198, 8), tenor_five_musicmaker_one],
        # [(198, 8), (199, 8), tenor_five_musicmaker_one],
    ]
])

voice_16_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 16',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), baritone_one_musicmaker_two],
        [(2, 8), (4, 8), baritone_one_musicmaker_two],
        [(4, 8), (6, 8), baritone_one_musicmaker_two],

        [(8, 8), (10, 8), baritone_one_musicmaker_one],
        [(10, 8), (12, 8), baritone_one_musicmaker_three],
        [(12, 8), (14, 8), baritone_one_musicmaker_one],
        [(14, 8), (16, 8), baritone_one_musicmaker_two],

        [(18, 8), (20, 8), baritone_one_musicmaker_two],
        [(20, 8), (22, 8), baritone_one_musicmaker_two],
        [(22, 8), (24, 8), baritone_one_musicmaker_one],
        [(24, 8), (26, 8), baritone_one_musicmaker_one],

        [(28, 8), (30, 8), baritone_one_musicmaker_two],
        [(30, 8), (32, 8), baritone_one_musicmaker_two],
        [(32, 8), (34, 8), baritone_one_musicmaker_two],
        [(34, 8), (36, 8), baritone_one_musicmaker_two],
        [(36, 8), (38, 8), baritone_one_musicmaker_one],
        [(38, 8), (40, 8), baritone_one_musicmaker_three],
        [(40, 8), (42, 8), baritone_one_musicmaker_one],
        [(42, 8), (44, 8), baritone_one_musicmaker_two],

        [(46, 8), (48, 8), baritone_one_musicmaker_two],
        [(48, 8), (50, 8), baritone_one_musicmaker_two],
        [(50, 8), (52, 8), baritone_one_musicmaker_one],
        [(52, 8), (54, 8), baritone_one_musicmaker_one],
        [(54, 8), (56, 8), baritone_one_musicmaker_three],
        # [(56, 8), (58, 8), baritone_one_musicmaker_two],
        # [(58, 8), (60, 8), baritone_one_musicmaker_two],
        # [(60, 8), (62, 8), baritone_one_musicmaker_two],
        # [(62, 8), (64, 8), baritone_one_musicmaker_two],
        # [(64, 8), (66, 8), baritone_one_musicmaker_one],
        # [(66, 8), (68, 8), baritone_one_musicmaker_three],
        # [(68, 8), (70, 8), baritone_one_musicmaker_one],
        # [(70, 8), (72, 8), baritone_one_musicmaker_two],
        # [(72, 8), (74, 8), baritone_one_musicmaker_two],
        #
        # [(76, 8), (78, 8), baritone_one_musicmaker_two],
        # [(78, 8), (80, 8), baritone_one_musicmaker_one],
        # [(80, 8), (82, 8), baritone_one_musicmaker_one],
        # [(82, 8), (84, 8), baritone_one_musicmaker_three],
        # [(84, 8), (86, 8), baritone_one_musicmaker_two],
        #
        # [(88, 8), (90, 8), baritone_one_musicmaker_two],
        # [(90, 8), (92, 8), baritone_one_musicmaker_two],
        # [(92, 8), (94, 8), baritone_one_musicmaker_one],
        # [(94, 8), (96, 8), baritone_one_musicmaker_three],
        # [(96, 8), (98, 8), baritone_one_musicmaker_one],
        #
        # [(100, 8), (102, 8), baritone_one_musicmaker_two],
        # [(102, 8), (104, 8), baritone_one_musicmaker_two],
        # [(104, 8), (106, 8), baritone_one_musicmaker_two],
        #
        # [(108, 8), (110, 8), baritone_one_musicmaker_one],
        # [(110, 8), (112, 8), baritone_one_musicmaker_three],
        # [(112, 8), (114, 8), baritone_one_musicmaker_one],
        # [(114, 8), (116, 8), baritone_one_musicmaker_two],
        # [(116, 8), (118, 8), baritone_one_musicmaker_two],
        # [(118, 8), (120, 8), baritone_one_musicmaker_two],
        # [(120, 8), (122, 8), baritone_one_musicmaker_one],
        # [(122, 8), (124, 8), baritone_one_musicmaker_three],
        # [(124, 8), (126, 8), baritone_one_musicmaker_one],
        # [(126, 8), (128, 8), baritone_one_musicmaker_one],
        # [(128, 8), (130, 8), baritone_one_musicmaker_two],
        # [(130, 8), (132, 8), baritone_one_musicmaker_two],
        # [(132, 8), (134, 8), baritone_one_musicmaker_two],
        # [(134, 8), (136, 8), baritone_one_musicmaker_one],
        # [(136, 8), (138, 8), baritone_one_musicmaker_one],
        # [(138, 8), (140, 8), baritone_one_musicmaker_three],
        # [(140, 8), (142, 8), baritone_one_musicmaker_one],
        # [(142, 8), (144, 8), baritone_one_musicmaker_two],
        # [(144, 8), (146, 8), baritone_one_musicmaker_two],
        # [(146, 8), (148, 8), baritone_one_musicmaker_two],
        #
        # [(150, 8), (152, 8), baritone_one_musicmaker_three],
        # [(152, 8), (154, 8), baritone_one_musicmaker_one],
        #
        # [(156, 8), (158, 8), baritone_one_musicmaker_two],
        #
        # [(162, 8), (164, 8), baritone_one_musicmaker_one],
        # [(164, 8), (166, 8), baritone_one_musicmaker_one],
        # [(166, 8), (168, 8), baritone_one_musicmaker_three],
        # [(168, 8), (170, 8), baritone_one_musicmaker_one],
        # [(170, 8), (172, 8), baritone_one_musicmaker_two],
        # [(172, 8), (174, 8), baritone_one_musicmaker_two],
        # [(174, 8), (176, 8), baritone_one_musicmaker_two],
        #
        # [(178, 8), (180, 8), baritone_one_musicmaker_three],
        # [(180, 8), (182, 8), baritone_one_musicmaker_one],
        # [(182, 8), (184, 8), baritone_one_musicmaker_one],
        # [(184, 8), (186, 8), baritone_one_musicmaker_two],
        # [(186, 8), (188, 8), baritone_one_musicmaker_two],
        #
        # [(190, 8), (192, 8), baritone_one_musicmaker_one],
        # [(192, 8), (194, 8), baritone_one_musicmaker_one],
        # [(194, 8), (196, 8), baritone_one_musicmaker_one],
        # [(196, 8), (198, 8), baritone_one_musicmaker_one],
        # [(198, 8), (199, 8), baritone_one_musicmaker_one],
    ]
])

voice_17_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 17',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), baritone_two_musicmaker_one],
        [(2, 8), (4, 8), baritone_two_musicmaker_one],
        [(4, 8), (6, 8), baritone_two_musicmaker_two],
        [(6, 8), (8, 8), baritone_two_musicmaker_two],
        [(8, 8), (10, 8), baritone_two_musicmaker_two],
        [(10, 8), (12, 8), baritone_two_musicmaker_three],
        [(12, 8), (14, 8), baritone_two_musicmaker_one],
        [(14, 8), (16, 8), baritone_two_musicmaker_one],
        [(16, 8), (18, 8), baritone_two_musicmaker_one],

        [(22, 8), (24, 8), baritone_two_musicmaker_two],
        [(24, 8), (26, 8), baritone_two_musicmaker_two],
        [(26, 8), (28, 8), baritone_two_musicmaker_two],
        [(28, 8), (30, 8), baritone_two_musicmaker_three],
        [(30, 8), (32, 8), baritone_two_musicmaker_one],
        [(32, 8), (34, 8), baritone_two_musicmaker_one],

        [(36, 8), (38, 8), baritone_two_musicmaker_one],
        [(38, 8), (40, 8), baritone_two_musicmaker_one],
        [(40, 8), (42, 8), baritone_two_musicmaker_two],
        [(42, 8), (44, 8), baritone_two_musicmaker_two],
        [(44, 8), (46, 8), baritone_two_musicmaker_two],
        [(46, 8), (48, 8), baritone_two_musicmaker_one],
        [(48, 8), (50, 8), baritone_two_musicmaker_two],
        [(50, 8), (52, 8), baritone_two_musicmaker_two],
        [(52, 8), (54, 8), baritone_two_musicmaker_two],
        [(54, 8), (56, 8), baritone_two_musicmaker_three],
        # [(56, 8), (58, 8), baritone_two_musicmaker_one],
        #
        # [(60, 8), (62, 8), baritone_two_musicmaker_one],
        # [(62, 8), (64, 8), baritone_two_musicmaker_one],
        # [(64, 8), (66, 8), baritone_two_musicmaker_one],
        # [(66, 8), (68, 8), baritone_two_musicmaker_one],
        # [(68, 8), (70, 8), baritone_two_musicmaker_two],
        # [(70, 8), (72, 8), baritone_two_musicmaker_three],
        # [(72, 8), (74, 8), baritone_two_musicmaker_two],
        # [(74, 8), (76, 8), baritone_two_musicmaker_two],
        #
        # [(78, 8), (80, 8), baritone_two_musicmaker_two],
        # [(80, 8), (82, 8), baritone_two_musicmaker_two],
        # [(82, 8), (84, 8), baritone_two_musicmaker_three],
        # [(84, 8), (86, 8), baritone_two_musicmaker_one],
        # [(86, 8), (88, 8), baritone_two_musicmaker_one],
        # [(88, 8), (90, 8), baritone_two_musicmaker_one],
        # [(90, 8), (92, 8), baritone_two_musicmaker_one],
        # [(92, 8), (94, 8), baritone_two_musicmaker_one],
        # [(94, 8), (96, 8), baritone_two_musicmaker_one],
        #
        # [(98, 8), (100, 8), baritone_two_musicmaker_two],
        # [(100, 8), (102, 8), baritone_two_musicmaker_two],
        # [(102, 8), (104, 8), baritone_two_musicmaker_two],
        # [(104, 8), (106, 8), baritone_two_musicmaker_two],
        # [(106, 8), (108, 8), baritone_two_musicmaker_three],
        # [(108, 8), (110, 8), baritone_two_musicmaker_one],
        # [(110, 8), (112, 8), baritone_two_musicmaker_one],
        # [(112, 8), (114, 8), baritone_two_musicmaker_one],
        # [(114, 8), (116, 8), baritone_two_musicmaker_one],
        #
        # [(118, 8), (120, 8), baritone_two_musicmaker_two],
        # [(120, 8), (122, 8), baritone_two_musicmaker_two],
        # [(122, 8), (124, 8), baritone_two_musicmaker_two],
        # [(124, 8), (126, 8), baritone_two_musicmaker_two],
        # [(126, 8), (128, 8), baritone_two_musicmaker_three],
        # [(128, 8), (130, 8), baritone_two_musicmaker_one],
        # [(130, 8), (132, 8), baritone_two_musicmaker_one],
        # [(132, 8), (134, 8), baritone_two_musicmaker_two],
        # [(134, 8), (136, 8), baritone_two_musicmaker_one],
        # [(136, 8), (138, 8), baritone_two_musicmaker_two],
        # [(138, 8), (140, 8), baritone_two_musicmaker_two],
        #
        # [(144, 8), (146, 8), baritone_two_musicmaker_two],
        # [(146, 8), (148, 8), baritone_two_musicmaker_three],
        # [(148, 8), (150, 8), baritone_two_musicmaker_one],
        # [(150, 8), (152, 8), baritone_two_musicmaker_one],
        # [(152, 8), (154, 8), baritone_two_musicmaker_two],
        # [(154, 8), (156, 8), baritone_two_musicmaker_one],
        # [(156, 8), (158, 8), baritone_two_musicmaker_two],
        # [(158, 8), (160, 8), baritone_two_musicmaker_two],
        # [(160, 8), (162, 8), baritone_two_musicmaker_two],
        # [(162, 8), (164, 8), baritone_two_musicmaker_three],
        # [(164, 8), (166, 8), baritone_two_musicmaker_one],
        # [(166, 8), (168, 8), baritone_two_musicmaker_one],
        #
        # [(170, 8), (172, 8), baritone_two_musicmaker_two],
        # [(172, 8), (174, 8), baritone_two_musicmaker_two],
        # [(174, 8), (176, 8), baritone_two_musicmaker_three],
        # [(176, 8), (178, 8), baritone_two_musicmaker_one],
        #
        # [(180, 8), (182, 8), baritone_two_musicmaker_two],
        # [(182, 8), (184, 8), baritone_two_musicmaker_two],
        # [(184, 8), (186, 8), baritone_two_musicmaker_two],
        # [(186, 8), (188, 8), baritone_two_musicmaker_three],
        #
        # [(190, 8), (192, 8), baritone_two_musicmaker_one],
        # [(192, 8), (194, 8), baritone_two_musicmaker_two],
        # [(194, 8), (196, 8), baritone_two_musicmaker_one],
        # [(196, 8), (198, 8), baritone_two_musicmaker_one],
        # [(198, 8), (199, 8), baritone_two_musicmaker_one],
    ]
])

voice_18_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 18',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), baritone_three_musicmaker_one],
        [(2, 8), (4, 8), baritone_three_musicmaker_one],
        [(4, 8), (6, 8), baritone_three_musicmaker_one],
        [(6, 8), (8, 8), baritone_three_musicmaker_one],
        [(8, 8), (10, 8), baritone_three_musicmaker_three],
        [(10, 8), (12, 8), baritone_three_musicmaker_two],

        [(16, 8), (18, 8), baritone_three_musicmaker_one],

        [(20, 8), (22, 8), baritone_three_musicmaker_one],
        [(22, 8), (24, 8), baritone_three_musicmaker_one],
        [(24, 8), (26, 8), baritone_three_musicmaker_three],
        [(26, 8), (28, 8), baritone_three_musicmaker_two],
        [(28, 8), (30, 8), baritone_three_musicmaker_two],
        [(30, 8), (32, 8), baritone_three_musicmaker_two],

        [(36, 8), (38, 8), baritone_three_musicmaker_one],
        [(39, 8), (40, 8), baritone_three_musicmaker_one],
        [(40, 8), (42, 8), baritone_three_musicmaker_three],
        [(42, 8), (44, 8), baritone_three_musicmaker_two],
        [(44, 8), (46, 8), baritone_three_musicmaker_two],
        [(46, 8), (48, 8), baritone_three_musicmaker_two],

        [(50, 8), (51, 8), baritone_three_musicmaker_one],
        [(52, 8), (54, 8), baritone_three_musicmaker_one],
        [(54, 8), (56, 8), baritone_three_musicmaker_one],
        # [(56, 8), (58, 8), baritone_three_musicmaker_three],
        # [(58, 8), (60, 8), baritone_three_musicmaker_two],
        # [(60, 8), (62, 8), baritone_three_musicmaker_two],
        #
        # [(64, 8), (66, 8), baritone_three_musicmaker_one],
        # [(66, 8), (68, 8), baritone_three_musicmaker_one],
        # [(68, 8), (70, 8), baritone_three_musicmaker_one],
        # [(70, 8), (72, 8), baritone_three_musicmaker_one],
        # [(72, 8), (74, 8), baritone_three_musicmaker_three],
        # [(74, 8), (76, 8), baritone_three_musicmaker_two],
        # [(76, 8), (78, 8), baritone_three_musicmaker_two],
        #
        # [(80, 8), (82, 8), baritone_three_musicmaker_one],
        # [(82, 8), (84, 8), baritone_three_musicmaker_one],
        # [(84, 8), (86, 8), baritone_three_musicmaker_one],
        # [(86, 8), (88, 8), baritone_three_musicmaker_one],
        # [(88, 8), (90, 8), baritone_three_musicmaker_three],
        # [(90, 8), (92, 8), baritone_three_musicmaker_two],
        # [(92, 8), (94, 8), baritone_three_musicmaker_two],
        # [(94, 8), (96, 8), baritone_three_musicmaker_two],
        # [(96, 8), (98, 8), baritone_three_musicmaker_one],
        # [(98, 8), (100, 8), baritone_three_musicmaker_one],
        # [(100, 8), (102, 8), baritone_three_musicmaker_one],
        # [(102, 8), (104, 8), baritone_three_musicmaker_one],
        # [(104, 8), (106, 8), baritone_three_musicmaker_three],
        # [(106, 8), (108, 8), baritone_three_musicmaker_two],
        #
        # [(110, 8), (112, 8), baritone_three_musicmaker_two],
        # [(112, 8), (114, 8), baritone_three_musicmaker_one],
        # [(114, 8), (116, 8), baritone_three_musicmaker_one],
        # [(116, 8), (118, 8), baritone_three_musicmaker_one],
        # [(118, 8), (120, 8), baritone_three_musicmaker_one],
        # [(120, 8), (122, 8), baritone_three_musicmaker_one],
        # [(122, 8), (124, 8), baritone_three_musicmaker_three],
        #
        # [(126, 8), (128, 8), baritone_three_musicmaker_two],
        # [(128, 8), (130, 8), baritone_three_musicmaker_two],
        # [(130, 8), (132, 8), baritone_three_musicmaker_two],
        # [(132, 8), (134, 8), baritone_three_musicmaker_one],
        # [(134, 8), (136, 8), baritone_three_musicmaker_one],
        # [(136, 8), (138, 8), baritone_three_musicmaker_one],
        # [(138, 8), (140, 8), baritone_three_musicmaker_one],
        # [(140, 8), (142, 8), baritone_three_musicmaker_one],
        #
        # [(144, 8), (146, 8), baritone_three_musicmaker_two],
        # [(146, 8), (148, 8), baritone_three_musicmaker_two],
        # [(148, 8), (150, 8), baritone_three_musicmaker_two],
        #
        # [(152, 8), (154, 8), baritone_three_musicmaker_one],
        # [(154, 8), (156, 8), baritone_three_musicmaker_one],
        # [(156, 8), (158, 8), baritone_three_musicmaker_one],
        #
        # [(160, 8), (162, 8), baritone_three_musicmaker_one],
        # [(162, 8), (164, 8), baritone_three_musicmaker_three],
        # [(164, 8), (166, 8), baritone_three_musicmaker_two],
        # [(166, 8), (168, 8), baritone_three_musicmaker_two],
        # [(168, 8), (170, 8), baritone_three_musicmaker_two],
        # [(170, 8), (172, 8), baritone_three_musicmaker_two],
        # [(172, 8), (174, 8), baritone_three_musicmaker_two],
        # [(174, 8), (176, 8), baritone_three_musicmaker_one],
        #
        # [(178, 8), (180, 8), baritone_three_musicmaker_one],
        # [(180, 8), (182, 8), baritone_three_musicmaker_two],
        # [(182, 8), (184, 8), baritone_three_musicmaker_one],
        # [(184, 8), (186, 8), baritone_three_musicmaker_one],
        # [(186, 8), (188, 8), baritone_three_musicmaker_three],
        # [(188, 8), (190, 8), baritone_three_musicmaker_two],
        # [(190, 8), (192, 8), baritone_three_musicmaker_one],
        # [(192, 8), (194, 8), baritone_three_musicmaker_one],
        # [(194, 8), (196, 8), baritone_three_musicmaker_two],
        # [(196, 8), (198, 8), baritone_three_musicmaker_one],
        # [(198, 8), (199, 8), baritone_three_musicmaker_one],
    ]
])

voice_19_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 19',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), bass_one_musicmaker_two],
        [(2, 8), (4, 8), bass_one_musicmaker_two],
        [(4, 8), (6, 8), bass_one_musicmaker_two],
        [(6, 8), (8, 8), bass_one_musicmaker_one],
        [(8, 8), (10, 8), bass_one_musicmaker_one],
        [(10, 8), (12, 8), bass_one_musicmaker_two],
        [(12, 8), (14, 8), bass_one_musicmaker_two],
        [(14, 8), (16, 8), bass_one_musicmaker_two],
        [(16, 8), (18, 8), bass_one_musicmaker_three],
        [(18, 8), (20, 8), bass_one_musicmaker_one],

        [(22, 8), (24, 8), bass_one_musicmaker_two],
        [(24, 8), (26, 8), bass_one_musicmaker_two],
        [(26, 8), (28, 8), bass_one_musicmaker_two],
        [(28, 8), (30, 8), bass_one_musicmaker_three],
        [(30, 8), (32, 8), bass_one_musicmaker_one],
        [(32, 8), (34, 8), bass_one_musicmaker_one],
        [(34, 8), (36, 8), bass_one_musicmaker_three],

        [(38, 8), (40, 8), bass_one_musicmaker_one],
        [(40, 8), (42, 8), bass_one_musicmaker_two],
        [(42, 8), (44, 8), bass_one_musicmaker_two],
        [(44, 8), (46, 8), bass_one_musicmaker_one],
        [(46, 8), (48, 8), bass_one_musicmaker_two],
        [(48, 8), (50, 8), bass_one_musicmaker_two],
        [(50, 8), (52, 8), bass_one_musicmaker_two],
        [(52, 8), (54, 8), bass_one_musicmaker_three],

        # [(56, 8), (58, 8), bass_one_musicmaker_two],
        # [(58, 8), (60, 8), bass_one_musicmaker_one],
        # [(60, 8), (62, 8), bass_one_musicmaker_three],
        # [(62, 8), (64, 8), bass_one_musicmaker_one],
        # [(64, 8), (68, 8), bass_one_musicmaker_one],
        # [(68, 8), (70, 8), bass_one_musicmaker_one],
        # [(70, 8), (72, 8), bass_one_musicmaker_one],
        #
        # [(74, 8), (76, 8), bass_one_musicmaker_two],
        # [(76, 8), (78, 8), bass_one_musicmaker_two],
        # [(78, 8), (80, 8), bass_one_musicmaker_two],
        # [(80, 8), (82, 8), bass_one_musicmaker_two],
        # [(82, 8), (84, 8), bass_one_musicmaker_three],
        # [(84, 8), (86, 8), bass_one_musicmaker_two],
        # [(86, 8), (88, 8), bass_one_musicmaker_two],
        # [(88, 8), (90, 8), bass_one_musicmaker_one],
        # [(90, 8), (92, 8), bass_one_musicmaker_three],
        #
        # [(94, 8), (96, 8), bass_one_musicmaker_one],
        # [(96, 8), (98, 8), bass_one_musicmaker_one],
        # [(98, 8), (100, 8), bass_one_musicmaker_one],
        # [(100, 8), (102, 8), bass_one_musicmaker_two],
        # [(102, 8), (104, 8), bass_one_musicmaker_two],
        # [(104, 8), (106, 8), bass_one_musicmaker_two],
        # [(106, 8), (108, 8), bass_one_musicmaker_two],
        # [(108, 8), (110, 8), bass_one_musicmaker_three],
        # [(110, 8), (112, 8), bass_one_musicmaker_two],
        #
        # [(114, 8), (116, 8), bass_one_musicmaker_two],
        # [(116, 8), (118, 8), bass_one_musicmaker_one],
        # [(118, 8), (120, 8), bass_one_musicmaker_one],
        # [(120, 8), (122, 8), bass_one_musicmaker_one],
        # [(122, 8), (124, 8), bass_one_musicmaker_one],
        # [(124, 8), (126, 8), bass_one_musicmaker_one],
        # [(126, 8), (128, 8), bass_one_musicmaker_three],
        # [(128, 8), (130, 8), bass_one_musicmaker_one],
        # [(130, 8), (132, 8), bass_one_musicmaker_one],
        # [(132, 8), (134, 8), bass_one_musicmaker_one],
        # [(134, 8), (136, 8), bass_one_musicmaker_one],
        #
        # [(138, 8), (140, 8), bass_one_musicmaker_two],
        # [(140, 8), (142, 8), bass_one_musicmaker_one],
        # [(142, 8), (144, 8), bass_one_musicmaker_one],
        # [(144, 8), (146, 8), bass_one_musicmaker_three],
        # [(146, 8), (148, 8), bass_one_musicmaker_two],
        # [(148, 8), (150, 8), bass_one_musicmaker_two],
        # [(150, 8), (152, 8), bass_one_musicmaker_two],
        # [(152, 8), (154, 8), bass_one_musicmaker_one],
        #
        # [(156, 8), (158, 8), bass_one_musicmaker_two],
        # [(158, 8), (160, 8), bass_one_musicmaker_two],
        # [(160, 8), (162, 8), bass_one_musicmaker_two],
        # [(162, 8), (164, 8), bass_one_musicmaker_three],
        # [(164, 8), (168, 8), bass_one_musicmaker_one],
        # [(168, 8), (170, 8), bass_one_musicmaker_two],
        # [(170, 8), (172, 8), bass_one_musicmaker_two],
        # [(172, 8), (174, 8), bass_one_musicmaker_two],
        # [(174, 8), (176, 8), bass_one_musicmaker_two],
        # [(176, 8), (178, 8), bass_one_musicmaker_two],
        #
        # [(180, 8), (182, 8), bass_one_musicmaker_one],
        # [(182, 8), (184, 8), bass_one_musicmaker_three],
        # [(184, 8), (186, 8), bass_one_musicmaker_one],
        # [(186, 8), (188, 8), bass_one_musicmaker_one],
        # [(188, 8), (190, 8), bass_one_musicmaker_two],
        # [(190, 8), (192, 8), bass_one_musicmaker_two],
        # [(192, 8), (194, 8), bass_one_musicmaker_one],
        # [(194, 8), (196, 8), bass_one_musicmaker_one],
        # [(196, 8), (198, 8), bass_one_musicmaker_one],
        # [(198, 8), (199, 8), bass_one_musicmaker_one],
    ]
])

voice_20_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 20',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), bass_two_musicmaker_two],
        [(2, 8), (4, 8), bass_two_musicmaker_two],
        [(4, 8), (6, 8), bass_two_musicmaker_two],
        [(6, 8), (8, 8), bass_two_musicmaker_one],
        [(8, 8), (10, 8), bass_two_musicmaker_one],
        [(10, 8), (12, 8), bass_two_musicmaker_two],
        [(12, 8), (14, 8), bass_two_musicmaker_two],

        [(16, 8), (18, 8), bass_two_musicmaker_two],
        [(18, 8), (20, 8), bass_two_musicmaker_one],
        [(20, 8), (22, 8), bass_two_musicmaker_three],
        [(22, 8), (24, 8), bass_two_musicmaker_two],
        [(24, 8), (26, 8), bass_two_musicmaker_two],
        [(26, 8), (28, 8), bass_two_musicmaker_two],
        [(28, 8), (30, 8), bass_two_musicmaker_two],
        [(30, 8), (32, 8), bass_two_musicmaker_three],
        [(32, 8), (34, 8), bass_two_musicmaker_one],

        [(36, 8), (38, 8), bass_two_musicmaker_two],
        [(38, 8), (40, 8), bass_two_musicmaker_one],
        [(40, 8), (42, 8), bass_two_musicmaker_one],
        [(42, 8), (44, 8), bass_two_musicmaker_one],
        [(44, 8), (46, 8), bass_two_musicmaker_one],
        [(46, 8), (48, 8), bass_two_musicmaker_two],
        [(48, 8), (50, 8), bass_two_musicmaker_three],

        [(52, 8), (54, 8), bass_two_musicmaker_two],
        [(54, 8), (56, 8), bass_two_musicmaker_two],
        # [(56, 8), (58, 8), bass_two_musicmaker_two],
        # [(58, 8), (60, 8), bass_two_musicmaker_three],
        # [(60, 8), (62, 8), bass_two_musicmaker_one],
        # [(62, 8), (64, 8), bass_two_musicmaker_one],
        # [(64, 8), (68, 8), bass_two_musicmaker_one],
        #
        # [(70, 8), (72, 8), bass_two_musicmaker_one],
        # [(72, 8), (74, 8), bass_two_musicmaker_three],
        # [(74, 8), (76, 8), bass_two_musicmaker_two],
        # [(76, 8), (78, 8), bass_two_musicmaker_two],
        # [(78, 8), (80, 8), bass_two_musicmaker_two],
        # [(80, 8), (82, 8), bass_two_musicmaker_two],
        # [(82, 8), (84, 8), bass_two_musicmaker_three],
        # [(84, 8), (86, 8), bass_two_musicmaker_two],
        # [(86, 8), (88, 8), bass_two_musicmaker_two],
        # [(88, 8), (90, 8), bass_two_musicmaker_one],
        # [(90, 8), (92, 8), bass_two_musicmaker_two],
        #
        # [(94, 8), (96, 8), bass_two_musicmaker_one],
        # [(96, 8), (98, 8), bass_two_musicmaker_one],
        # [(98, 8), (100, 8), bass_two_musicmaker_one],
        # [(100, 8), (102, 8), bass_two_musicmaker_three],
        # [(102, 8), (104, 8), bass_two_musicmaker_two],
        # [(104, 8), (106, 8), bass_two_musicmaker_two],
        #
        # [(108, 8), (110, 8), bass_two_musicmaker_two],
        # [(110, 8), (112, 8), bass_two_musicmaker_three],
        # [(112, 8), (114, 8), bass_two_musicmaker_two],
        # [(114, 8), (116, 8), bass_two_musicmaker_two],
        # [(116, 8), (118, 8), bass_two_musicmaker_one],
        # [(118, 8), (120, 8), bass_two_musicmaker_one],
        # [(120, 8), (122, 8), bass_two_musicmaker_one],
        # [(122, 8), (124, 8), bass_two_musicmaker_two],
        #
        # [(126, 8), (128, 8), bass_two_musicmaker_two],
        # [(128, 8), (130, 8), bass_two_musicmaker_one],
        # [(130, 8), (132, 8), bass_two_musicmaker_one],
        # [(132, 8), (134, 8), bass_two_musicmaker_three],
        # [(134, 8), (136, 8), bass_two_musicmaker_one],
        # [(136, 8), (138, 8), bass_two_musicmaker_two],
        # [(138, 8), (140, 8), bass_two_musicmaker_two],
        #
        # [(142, 8), (144, 8), bass_two_musicmaker_three],
        # [(144, 8), (146, 8), bass_two_musicmaker_one],
        # [(146, 8), (148, 8), bass_two_musicmaker_two],
        # [(148, 8), (150, 8), bass_two_musicmaker_two],
        # [(150, 8), (152, 8), bass_two_musicmaker_two],
        # [(152, 8), (154, 8), bass_two_musicmaker_one],
        # [(154, 8), (156, 8), bass_two_musicmaker_one],
        #
        # [(158, 8), (160, 8), bass_two_musicmaker_two],
        # [(160, 8), (162, 8), bass_two_musicmaker_three],
        # [(162, 8), (164, 8), bass_two_musicmaker_two],
        # [(164, 8), (168, 8), bass_two_musicmaker_one],
        # [(168, 8), (170, 8), bass_two_musicmaker_two],
        # [(170, 8), (172, 8), bass_two_musicmaker_two],
        # [(172, 8), (174, 8), bass_two_musicmaker_three],
        # [(174, 8), (176, 8), bass_two_musicmaker_two],
        # [(176, 8), (178, 8), bass_two_musicmaker_two],
        # [(178, 8), (180, 8), bass_two_musicmaker_one],
        #
        # [(182, 8), (184, 8), bass_two_musicmaker_one],
        # [(184, 8), (186, 8), bass_two_musicmaker_one],
        # [(186, 8), (188, 8), bass_two_musicmaker_one],
        #
        # [(190, 8), (192, 8), bass_two_musicmaker_three],
        # [(192, 8), (194, 8), bass_two_musicmaker_one],
        # [(194, 8), (196, 8), bass_two_musicmaker_two],
        # [(196, 8), (198, 8), bass_two_musicmaker_one],
        # [(198, 8), (199, 8), bass_two_musicmaker_one],
    ]
])

voice_21_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=MusicSpecifier(
            music_maker=music_maker,
            voice_name='Voice 21',
        ),
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (2, 8), contrabass_musicmaker_two],
        [(2, 8), (4, 8), contrabass_musicmaker_two],
        [(4, 8), (6, 8), contrabass_musicmaker_two],
        [(6, 8), (8, 8), contrabass_musicmaker_three],
        [(8, 8), (10, 8), contrabass_musicmaker_one],
        [(10, 8), (12, 8), contrabass_musicmaker_two],

        [(14, 8), (16, 8), contrabass_musicmaker_two],
        [(16, 8), (18, 8), contrabass_musicmaker_two],
        [(18, 8), (20, 8), contrabass_musicmaker_three],
        [(20, 8), (22, 8), contrabass_musicmaker_two],
        [(22, 8), (24, 8), contrabass_musicmaker_two],
        [(24, 8), (26, 8), contrabass_musicmaker_two],

        [(30, 8), (32, 8), contrabass_musicmaker_one],
        [(32, 8), (34, 8), contrabass_musicmaker_one],
        [(34, 8), (36, 8), contrabass_musicmaker_one],
        [(36, 8), (38, 8), contrabass_musicmaker_one],
        [(38, 8), (40, 8), contrabass_musicmaker_three],
        [(40, 8), (42, 8), contrabass_musicmaker_one],
        [(42, 8), (44, 8), contrabass_musicmaker_one],
        [(44, 8), (46, 8), contrabass_musicmaker_one],
        [(46, 8), (48, 8), contrabass_musicmaker_three],
        [(48, 8), (50, 8), contrabass_musicmaker_two],
        [(50, 8), (52, 8), contrabass_musicmaker_two],
        [(52, 8), (54, 8), contrabass_musicmaker_two],
        [(54, 8), (56, 8), contrabass_musicmaker_two],
        # [(56, 8), (58, 8), contrabass_musicmaker_two],
        # [(58, 8), (60, 8), contrabass_musicmaker_three],
        # [(60, 8), (62, 8), contrabass_musicmaker_one],
        #
        # [(64, 8), (68, 8), contrabass_musicmaker_one],
        # [(68, 8), (70, 8), contrabass_musicmaker_three],
        # [(70, 8), (72, 8), contrabass_musicmaker_one],
        # [(72, 8), (74, 8), contrabass_musicmaker_one],
        # [(74, 8), (76, 8), contrabass_musicmaker_two],
        # [(76, 8), (78, 8), contrabass_musicmaker_two],
        # [(78, 8), (80, 8), contrabass_musicmaker_two],
        # [(80, 8), (82, 8), contrabass_musicmaker_three],
        # [(82, 8), (84, 8), contrabass_musicmaker_two],
        # [(84, 8), (86, 8), contrabass_musicmaker_two],
        #
        # [(90, 8), (92, 8), contrabass_musicmaker_one],
        # [(92, 8), (94, 8), contrabass_musicmaker_one],
        # [(94, 8), (96, 8), contrabass_musicmaker_one],
        # [(96, 8), (98, 8), contrabass_musicmaker_one],
        # [(98, 8), (100, 8), contrabass_musicmaker_one],
        # [(100, 8), (102, 8), contrabass_musicmaker_three],
        # [(102, 8), (104, 8), contrabass_musicmaker_two],
        # [(104, 8), (106, 8), contrabass_musicmaker_two],
        # [(106, 8), (108, 8), contrabass_musicmaker_two],
        # [(108, 8), (110, 8), contrabass_musicmaker_three],
        # [(110, 8), (112, 8), contrabass_musicmaker_two],
        # [(112, 8), (114, 8), contrabass_musicmaker_two],
        #
        # [(116, 8), (118, 8), contrabass_musicmaker_one],
        # [(118, 8), (120, 8), contrabass_musicmaker_one],
        # [(120, 8), (122, 8), contrabass_musicmaker_three],
        # [(122, 8), (124, 8), contrabass_musicmaker_one],
        # [(124, 8), (126, 8), contrabass_musicmaker_one],
        # [(126, 8), (128, 8), contrabass_musicmaker_two],
        # [(128, 8), (130, 8), contrabass_musicmaker_three],
        # [(130, 8), (132, 8), contrabass_musicmaker_one],
        # [(132, 8), (134, 8), contrabass_musicmaker_one],
        # [(134, 8), (136, 8), contrabass_musicmaker_one],
        # [(136, 8), (138, 8), contrabass_musicmaker_two],
        # [(138, 8), (140, 8), contrabass_musicmaker_two],
        # [(140, 8), (142, 8), contrabass_musicmaker_three],
        # [(142, 8), (144, 8), contrabass_musicmaker_one],
        # [(144, 8), (146, 8), contrabass_musicmaker_one],
        # [(146, 8), (148, 8), contrabass_musicmaker_two],
        # [(148, 8), (150, 8), contrabass_musicmaker_three],
        # [(150, 8), (152, 8), contrabass_musicmaker_two],
        #
        # [(154, 8), (156, 8), contrabass_musicmaker_one],
        # [(156, 8), (158, 8), contrabass_musicmaker_two],
        # [(158, 8), (160, 8), contrabass_musicmaker_two],
        # [(160, 8), (162, 8), contrabass_musicmaker_three],
        # [(162, 8), (164, 8), contrabass_musicmaker_two],
        # [(164, 8), (168, 8), contrabass_musicmaker_one],
        # [(168, 8), (170, 8), contrabass_musicmaker_two],
        # [(170, 8), (172, 8), contrabass_musicmaker_three],
        # [(172, 8), (174, 8), contrabass_musicmaker_two],
        # [(174, 8), (176, 8), contrabass_musicmaker_two],
        #
        # [(178, 8), (180, 8), contrabass_musicmaker_one],
        # [(180, 8), (182, 8), contrabass_musicmaker_one],
        # [(182, 8), (184, 8), contrabass_musicmaker_three],
        # [(184, 8), (186, 8), contrabass_musicmaker_one],
        # [(186, 8), (188, 8), contrabass_musicmaker_one],
        # [(188, 8), (190, 8), contrabass_musicmaker_one],
        # [(190, 8), (192, 8), contrabass_musicmaker_three],
        # [(192, 8), (194, 8), contrabass_musicmaker_one],
        # [(194, 8), (196, 8), contrabass_musicmaker_one],
        # [(196, 8), (198, 8), contrabass_musicmaker_one],
        # [(198, 8), (199, 8), contrabass_musicmaker_one],
    ]
])

# Create a dictionary mapping voice names to timespan lists so we can
# maintain the association in later operations:

all_timespans = [
    voice_1_timespan_list,
    voice_2_timespan_list,
    voice_3_timespan_list,
    voice_4_timespan_list,
    voice_5_timespan_list,
    voice_6_timespan_list,
    voice_7_timespan_list,
    voice_8_timespan_list,
    voice_9_timespan_list,
    voice_10_timespan_list,
    voice_11_timespan_list,
    voice_12_timespan_list,
    voice_13_timespan_list,
    voice_14_timespan_list,
    voice_15_timespan_list,
    voice_16_timespan_list,
    voice_17_timespan_list,
    voice_18_timespan_list,
    voice_19_timespan_list,
    voice_20_timespan_list,
    voice_21_timespan_list,
]
all_timespan_lists = abjad.TimespanList([])
all_timespan_lists = make_showable_list(all_timespans)

abjad.show(all_timespan_lists,
key='annotation',
scale=2
)
