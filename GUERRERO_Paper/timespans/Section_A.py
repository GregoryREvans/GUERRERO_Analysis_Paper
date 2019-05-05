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
        (5, 4), (4, 4), (3, 4), (4, 4), (3, 4), (4, 4),
        (5, 4), (5, 4), (4, 4), (3, 4), (4, 4), (3, 4),
        (4, 4), (5, 4), (5, 4), (4, 4), (3, 4), (4, 4),
        (3, 4), (4, 4), (4, 4),
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

sopranino_note = [27, 11, 17, 8, 0, 17, 11, 8, ]
soprano_1_note = [22, 5, 16, 13, ]
soprano_2_note = [16, 22, 13, 5, ]
soprano_3_note = [13, 16, 5, 13, 22, ]
alto_1_note = [20, 23, 1, 12, ]
alto_2_note = [12, 1, 23, 20, ]
alto_3_note = [1, 23, 12, 20, ]
alto_4_note = [20, 12, 23, 1, ]
alto_5_note = [12, 20, 1, 23, ]
alto_6_note = [1, 20, 23, 12, ]
tenor_1_note = [17, 25, 6, -1, ]
tenor_2_note = [6, -1, 25, 17, ]
tenor_3_note = [-1, 6, 25, 17, ]
tenor_4_note = [6, 17, 25, -1, ]
tenor_5_note = [-1, 17, 6, 25, ]
baritone_1_note = [13, 24, 6, 4, ]
baritone_2_note = [6, 4, 24, 13, ]
baritone_3_note = [4, 6, 13, 24, ]
bass_1_note = [11, 18, 9, 0, ]
bass_2_note = [9, 11, 0, 18, ]
contrabass_note = [-2, 7, 16, 2, 18, 25, ]
# -3 at bottom of chord for completion
sopranino_chord = [17, 27, 11, 0, 8,]
soprano_1_chord = [[13.25, 16, 26.25, ], ]
soprano_2_chord = [[13, 14.75, 26.25, ], ] #maybe it's 13.25?
soprano_3_chord = [[12.75, 15.5, 26, ], ]
alto_1_chord = [[12.5, 19, 27.75, 34, ], ]
alto_2_chord = [[12.5, 15.25, 25.5, ], ]
alto_3_chord = [[1.75, 13.5, 22.25, 27, 30, ], ]
alto_4_chord = [[12.5, 15.25, 25.5, ], ]
alto_5_chord = [[1.75, 13.5, 22.25, 27, 30, ], ]
alto_6_chord = [[12.5, 19, 27.75, 34, ], ]
tenor_1_chord = [[6, 17.5, ], ]
tenor_2_chord = [[6, 17.5, 25.5, 30, ], ]
tenor_3_chord = [[6, 17.5, 25.5, 30.75, ], ]
tenor_4_chord = [[6, 17.5, ], ]
tenor_5_chord = [[6, 17.5, 25.5, 30.75, ], ]
baritone_1_chord = [[13.25, 27.5, 33.75, ], ]
baritone_2_chord = [[4, 16.5, 23.5, ], ]
baritone_3_chord = [[7.75, 17.75, 25.5, 34, ], ]
bass_1_chord = [11, 9, 18, ]
bass_2_chord = [9, 11, 18, ]
contrabass_chord = [-2, 2, 7, -2, 7, 2, ]

seed(1)
sopranino_random_walk = []
sopranino_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = sopranino_random_walk[i-1] + movement
    sopranino_random_walk.append(value)
sopranino_random_walk_notes = [((x / 2.0) + 19) for x in sopranino_random_walk]

seed(2)
soprano_1_random_walk = []
soprano_1_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = soprano_1_random_walk[i-1] + movement
    soprano_1_random_walk.append(value)
soprano_1_random_walk_notes = [((x / 2.0) + 18) for x in soprano_1_random_walk]

seed(3)
soprano_2_random_walk = []
soprano_2_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = soprano_2_random_walk[i-1] + movement
    soprano_2_random_walk.append(value)
soprano_2_random_walk_notes = [((x / 2.0) + 17) for x in soprano_2_random_walk]

seed(4)
soprano_3_random_walk = []
soprano_3_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = soprano_3_random_walk[i-1] + movement
    soprano_3_random_walk.append(value)
soprano_3_random_walk_notes = [((x / 2.0) + 16) for x in soprano_3_random_walk]

seed(5)
alto_1_random_walk = []
alto_1_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = alto_1_random_walk[i-1] + movement
    alto_1_random_walk.append(value)
alto_1_random_walk_notes = [((x / 2.0) + 14) for x in alto_1_random_walk]

seed(6)
alto_2_random_walk = []
alto_2_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = alto_2_random_walk[i-1] + movement
    alto_2_random_walk.append(value)
alto_2_random_walk_notes = [((x / 2.0) + 13) for x in alto_2_random_walk]

seed(7)
alto_3_random_walk = []
alto_3_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = alto_3_random_walk[i-1] + movement
    alto_3_random_walk.append(value)
alto_3_random_walk_notes = [((x / 2.0) + 12) for x in alto_3_random_walk]

seed(8)
alto_4_random_walk = []
alto_4_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = alto_4_random_walk[i-1] + movement
    alto_4_random_walk.append(value)
alto_4_random_walk_notes = [((x / 2.0) + 11) for x in alto_4_random_walk]

seed(9)
alto_5_random_walk = []
alto_5_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = alto_5_random_walk[i-1] + movement
    alto_5_random_walk.append(value)
alto_5_random_walk_notes = [((x / 2.0) + 10) for x in alto_5_random_walk]

seed(10)
alto_6_random_walk = []
alto_6_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = alto_6_random_walk[i-1] + movement
    alto_6_random_walk.append(value)
alto_6_random_walk_notes = [((x / 2.0) + 10) for x in alto_6_random_walk]

seed(11)
tenor_1_random_walk = []
tenor_1_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = tenor_1_random_walk[i-1] + movement
    tenor_1_random_walk.append(value)
tenor_1_random_walk_notes = [((x / 2.0) + 9) for x in tenor_1_random_walk]

seed(12)
tenor_2_random_walk = []
tenor_2_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = tenor_2_random_walk[i-1] + movement
    tenor_2_random_walk.append(value)
tenor_2_random_walk_notes = [((x / 2.0) + 8) for x in tenor_2_random_walk]

seed(13)
tenor_3_random_walk = []
tenor_3_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = tenor_3_random_walk[i-1] + movement
    tenor_3_random_walk.append(value)
tenor_3_random_walk_notes = [((x / 2.0) + 7) for x in tenor_3_random_walk]

seed(14)
tenor_4_random_walk = []
tenor_4_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = tenor_4_random_walk[i-1] + movement
    tenor_4_random_walk.append(value)
tenor_4_random_walk_notes = [((x / 2.0) + 6) for x in tenor_4_random_walk]

seed(15)
tenor_5_random_walk = []
tenor_5_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = tenor_5_random_walk[i-1] + movement
    tenor_5_random_walk.append(value)
tenor_5_random_walk_notes = [((x / 2.0) + 6) for x in tenor_5_random_walk]

seed(16)
baritone_1_random_walk = []
baritone_1_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = baritone_1_random_walk[i-1] + movement
    baritone_1_random_walk.append(value)
baritone_1_random_walk_notes = [((x / 2.0) + 5) for x in baritone_1_random_walk]

seed(17)
baritone_2_random_walk = []
baritone_2_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = baritone_2_random_walk[i-1] + movement
    baritone_2_random_walk.append(value)
baritone_2_random_walk_notes = [((x / 2.0) + 4) for x in baritone_2_random_walk]

seed(18)
baritone_3_random_walk = []
baritone_3_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = baritone_3_random_walk[i-1] + movement
    baritone_3_random_walk.append(value)
baritone_3_random_walk_notes = [((x / 2.0) + 3) for x in baritone_3_random_walk]

seed(19)
bass_1_random_walk = []
bass_1_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = bass_1_random_walk[i-1] + movement
    bass_1_random_walk.append(value)
bass_1_random_walk_notes = [((x / 2.0) + 2) for x in bass_1_random_walk]

seed(20)
bass_2_random_walk = []
bass_2_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = bass_2_random_walk[i-1] + movement
    bass_2_random_walk.append(value)
bass_2_random_walk_notes = [((x / 2.0) + 1) for x in bass_2_random_walk]

seed(21)
contrabass_random_walk = []
contrabass_random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = contrabass_random_walk[i-1] + movement
    contrabass_random_walk.append(value)
contrabass_random_walk_notes = [(x / 2.0) for x in contrabass_random_walk]

# Define rhythm-makers: two to be used by the MusicMaker, one for silence.

rmaker_one = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(
        counts=[19, -1, 17, -1, 15, -1, 13, -1, 11, -1, 9, -1, 7, -1, ],
        denominator=16,
        ),
    beam_specifier=abjadext.rmakers.BeamSpecifier(
        beam_divisions_together=True,
        beam_rests=False,
        ),
    extra_counts_per_division=[0, 1, -1, 0, ],
    tuplet_specifier=abjadext.rmakers.TupletSpecifier(
        trivialize=True,
        extract_trivial=True,
        rewrite_rest_filled=True,
        rewrite_sustained=True,
        ),
    )

rmaker_two = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(
        counts=[1, 1, 1, 1, -1, 2, 2, 1, -2, 1, 3, 2, 2, 3, 2, -1, 1, 2, 1, -1, 1, 3, ],
        denominator=16,
        ),
    beam_specifier=abjadext.rmakers.BeamSpecifier(
        beam_divisions_together=True,
        beam_rests=False,
        ),
    extra_counts_per_division=[-1, 0, 1, 0, ],
    # burnish_specifier=abjadext.rmakers.BurnishSpecifier(
    #     left_classes=[abjad.Note, abjad.Rest],
    #     left_counts=[1, 0, 1],
    #     ),
    tuplet_specifier=abjadext.rmakers.TupletSpecifier(
        trivialize=True,
        extract_trivial=True,
        rewrite_rest_filled=True,
        ),
    )

# Initialize AttachmentHandler

attachment_handler_one = AttachmentHandler(
    starting_dynamic='p',
    ending_dynamic='mp',
    hairpin='--',
    articulation_list=['tenuto'],
)

attachment_handler_two = AttachmentHandler(
    starting_dynamic='mp',
    ending_dynamic='f',
    hairpin='<',
    articulation_list=['espressivo'],
)

attachment_handler_three = AttachmentHandler(
    starting_dynamic='mf',
    ending_dynamic='pp',
    hairpin='>',
    articulation_list=['portato', '', '', '', '', ],
)

# Initialize MusicMakers with the rhythm-makers.
#####sopranino#####
sopranino_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=sopranino_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
sopranino_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=sopranino_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
sopranino_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=sopranino_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####soprano_one#####
soprano_one_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=soprano_1_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
soprano_one_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=soprano_1_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
soprano_one_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_1_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####soprano_two#####
soprano_two_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=soprano_2_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
soprano_two_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=soprano_2_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
soprano_two_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_2_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####soprano_three#####
soprano_three_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=soprano_3_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
soprano_three_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=soprano_3_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
soprano_three_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_3_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####alto_one#####
alto_one_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_1_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_one_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_1_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
alto_one_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_1_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####alto_two#####
alto_two_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_2_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_two_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_2_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
alto_two_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_2_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####alto_three#####
alto_three_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_3_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_three_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_3_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
alto_three_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_3_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####alto_four#####
alto_four_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_4_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_four_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_4_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
alto_four_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_4_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####alto_five#####
alto_five_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_5_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_five_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_5_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
alto_five_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_5_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####alto_six#####
alto_six_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_6_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_six_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_6_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
alto_six_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_6_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####tenor_one#####
tenor_one_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=tenor_1_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
tenor_one_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=tenor_1_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
tenor_one_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_1_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####tenor_two#####
tenor_two_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=tenor_2_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
tenor_two_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=tenor_2_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
tenor_two_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_2_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####tenor_three#####
tenor_three_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=tenor_3_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
tenor_three_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=tenor_3_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
tenor_three_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_3_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####tenor_four#####
tenor_four_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=tenor_4_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
tenor_four_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=tenor_4_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
tenor_four_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_4_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####tenor_five#####
tenor_five_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=tenor_5_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
tenor_five_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=tenor_5_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
tenor_five_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_5_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####baritone_one#####
baritone_one_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=baritone_1_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
baritone_one_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=baritone_1_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
baritone_one_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=baritone_1_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####baritone_two#####
baritone_two_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=baritone_2_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
baritone_two_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=baritone_2_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
baritone_two_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=baritone_2_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####baritone_three#####
baritone_three_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=baritone_3_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
baritone_three_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=baritone_3_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
baritone_three_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=baritone_3_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####bass_one#####
bass_one_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=bass_1_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
bass_one_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=bass_1_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
bass_one_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=bass_1_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####bass_two#####
bass_two_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=bass_2_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
bass_two_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=bass_2_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
bass_two_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=bass_2_random_walk_notes,
    continuous=True,
    attachment_handler=attachment_handler_three,
)
#####contrabass#####
contrabass_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=contrabass_note,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
contrabass_musicmaker_two = MusicMaker(
    rmaker=rmaker_one,
    pitches=contrabass_chord,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
contrabass_musicmaker_three = MusicMaker(
    rmaker=rmaker_two,
    pitches=contrabass_random_walk_notes,
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
        [(0, 4), (1, 4), sopranino_musicmaker_one],
        [(1, 4), (2, 4), sopranino_musicmaker_one],
        [(2, 4), (3, 4), sopranino_musicmaker_one],
        [(3, 4), (4, 4), sopranino_musicmaker_one],
        [(4, 4), (5, 4), sopranino_musicmaker_one],
        [(11, 8), (13, 8), sopranino_musicmaker_one],
        [(21, 8), (23, 8), sopranino_musicmaker_two],
        [(12, 4), (13, 4), sopranino_musicmaker_one],
        [(13, 4), (14, 4), sopranino_musicmaker_one],
        [(14, 4), (15, 4), sopranino_musicmaker_one],
        [(35, 8), (37, 8), sopranino_musicmaker_two],
        [(37, 8), (39, 8), sopranino_musicmaker_two],
        [(21, 4), (22, 4), sopranino_musicmaker_one],
        [(22, 4), (23, 4), sopranino_musicmaker_one],
        [(24, 4), (25, 4), sopranino_musicmaker_two],
        [(25, 4), (26, 4), sopranino_musicmaker_two],
        [(26, 4), (27, 4), sopranino_musicmaker_two],
        [(27, 4), (28, 4), sopranino_musicmaker_two],

        [(28, 4), (29, 4), sopranino_musicmaker_one],
        [(29, 4), (30, 4), sopranino_musicmaker_one],
        [(30, 4), (31, 4), sopranino_musicmaker_one],
        [(31, 4), (32, 4), sopranino_musicmaker_one],
        [(32, 4), (33, 4), sopranino_musicmaker_one],
        [(67, 8), (69, 8), sopranino_musicmaker_two],
        [(39, 4), (40, 4), sopranino_musicmaker_three],
        [(40, 4), (41, 4), sopranino_musicmaker_one],
        [(41, 4), (42, 4), sopranino_musicmaker_one],
        [(42, 4), (43, 4), sopranino_musicmaker_one],
        [(46, 4), (47, 4), sopranino_musicmaker_two],
        [(47, 4), (48, 4), sopranino_musicmaker_three],
        [(49, 4), (50, 4), sopranino_musicmaker_one],
        [(50, 4), (51, 4), sopranino_musicmaker_one],
        [(52, 4), (53, 4), sopranino_musicmaker_two],
        [(53, 4), (54, 4), sopranino_musicmaker_two],
        [(54, 4), (55, 4), sopranino_musicmaker_two],
        [(55, 4), (56, 4), sopranino_musicmaker_two],

        [(56, 4), (57, 4), sopranino_musicmaker_one],
        [(57, 4), (58, 4), sopranino_musicmaker_one],
        [(58, 4), (59, 4), sopranino_musicmaker_one],
        [(59, 4), (60, 4), sopranino_musicmaker_one],
        [(60, 4), (61, 4), sopranino_musicmaker_one],
        [(61, 4), (62, 4), sopranino_musicmaker_one],
        [(62, 4), (63, 4), sopranino_musicmaker_one],
        [(63, 4), (64, 4), sopranino_musicmaker_one],
        [(67, 4), (68, 4), sopranino_musicmaker_two],
        [(68, 4), (69, 4), sopranino_musicmaker_two],
        [(69, 4), (70, 4), sopranino_musicmaker_two],
        [(70, 4), (71, 4), sopranino_musicmaker_two],
        [(74, 4), (75, 4), sopranino_musicmaker_three],
        [(75, 4), (76, 4), sopranino_musicmaker_three],
        [(76, 4), (77, 4), sopranino_musicmaker_three],
        [(77, 4), (78, 4), sopranino_musicmaker_one],
        [(78, 4), (79, 4), sopranino_musicmaker_one],
        [(79, 4), (80, 4), sopranino_musicmaker_two],
        [(80, 4), (81, 4), sopranino_musicmaker_two],
        [(81, 4), (82, 4), sopranino_musicmaker_two],
        [(82, 4), (83, 4), sopranino_musicmaker_two],

        # [(83, 4), (167, 8), silence_maker],
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
        [(0, 4), (1, 4), soprano_one_musicmaker_one],
        [(1, 4), (2, 4), soprano_one_musicmaker_one],
        [(2, 4), (3, 4), soprano_one_musicmaker_one],
        [(3, 4), (4, 4), soprano_one_musicmaker_one],
        [(4, 4), (5, 4), soprano_one_musicmaker_one],
        [(9, 4), (10, 4), soprano_one_musicmaker_two],
        [(10, 4), (11, 4), soprano_one_musicmaker_two],
        [(11, 4), (12, 4), soprano_one_musicmaker_two],
        [(14, 4), (15, 4), soprano_one_musicmaker_one],
        [(21, 4), (22, 4), soprano_one_musicmaker_two],
        [(22, 4), (23, 4), soprano_one_musicmaker_two],
        [(23, 4), (24, 4), soprano_one_musicmaker_two],
        [(24, 4), (25, 4), soprano_one_musicmaker_two],
        [(25, 4), (26, 4), soprano_one_musicmaker_two],

        [(28, 4), (29, 4), soprano_one_musicmaker_one],
        [(29, 4), (30, 4), soprano_one_musicmaker_one],
        [(30, 4), (31, 4), soprano_one_musicmaker_one],
        [(31, 4), (32, 4), soprano_one_musicmaker_one],
        [(32, 4), (33, 4), soprano_one_musicmaker_one],
        [(37, 4), (38, 4), soprano_one_musicmaker_two],
        [(38, 4), (39, 4), soprano_one_musicmaker_two],
        [(39, 4), (40, 4), soprano_one_musicmaker_two],
        [(42, 4), (43, 4), soprano_one_musicmaker_three],
        [(49, 4), (50, 4), soprano_one_musicmaker_one],
        [(50, 4), (51, 4), soprano_one_musicmaker_one],
        [(51, 4), (52, 4), soprano_one_musicmaker_two],
        [(52, 4), (53, 4), soprano_one_musicmaker_two],
        [(53, 4), (54, 4), soprano_one_musicmaker_two],

        [(56, 4), (57, 4), soprano_one_musicmaker_one],
        [(57, 4), (58, 4), soprano_one_musicmaker_one],
        [(58, 4), (59, 4), soprano_one_musicmaker_one],
        [(59, 4), (60, 4), soprano_one_musicmaker_one],
        [(60, 4), (61, 4), soprano_one_musicmaker_one],
        [(65, 4), (66, 4), soprano_one_musicmaker_one],
        [(66, 4), (67, 4), soprano_one_musicmaker_one],
        [(67, 4), (68, 4), soprano_one_musicmaker_one],
        [(70, 4), (71, 4), soprano_one_musicmaker_two],
        [(77, 4), (78, 4), soprano_one_musicmaker_two],
        [(78, 4), (79, 4), soprano_one_musicmaker_two],
        [(79, 4), (80, 4), soprano_one_musicmaker_three],
        [(80, 4), (81, 4), soprano_one_musicmaker_three],
        [(81, 4), (82, 4), soprano_one_musicmaker_three],
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
        [(0, 4), (1, 4), soprano_two_musicmaker_two],
        [(1, 4), (2, 4), soprano_two_musicmaker_two],
        [(2, 4), (3, 4), soprano_two_musicmaker_two],
        [(3, 4), (4, 4), soprano_two_musicmaker_two],
        [(7, 4), (8, 4), soprano_two_musicmaker_one],
        [(8, 4), (9, 4), soprano_two_musicmaker_one],
        [(10, 4), (11, 4), soprano_two_musicmaker_two],
        [(11, 4), (12, 4), soprano_two_musicmaker_two],
        [(12, 4), (13, 4), soprano_two_musicmaker_two],
        [(13, 4), (14, 4), soprano_two_musicmaker_two],
        [(14, 4), (15, 4), soprano_two_musicmaker_two],
        [(15, 4), (16, 4), soprano_two_musicmaker_two],
        [(21, 4), (22, 4), soprano_two_musicmaker_one],
        [(22, 4), (23, 4), soprano_two_musicmaker_one],
        [(23, 4), (24, 4), soprano_two_musicmaker_two],
        [(24, 4), (25, 4), soprano_two_musicmaker_two],

        [(28, 4), (29, 4), soprano_two_musicmaker_one],
        [(29, 4), (30, 4), soprano_two_musicmaker_one],
        [(30, 4), (31, 4), soprano_two_musicmaker_one],
        [(31, 4), (32, 4), soprano_two_musicmaker_one],
        [(35, 4), (36, 4), soprano_two_musicmaker_two],
        [(36, 4), (37, 4), soprano_two_musicmaker_two],
        [(38, 4), (39, 4), soprano_two_musicmaker_three],
        [(39, 4), (40, 4), soprano_two_musicmaker_three],
        [(40, 4), (41, 4), soprano_two_musicmaker_one],
        [(41, 4), (42, 4), soprano_two_musicmaker_one],
        [(42, 4), (43, 4), soprano_two_musicmaker_one],
        [(43, 4), (44, 4), soprano_two_musicmaker_one],
        [(49, 4), (50, 4), soprano_two_musicmaker_two],
        [(50, 4), (51, 4), soprano_two_musicmaker_two],
        [(51, 4), (52, 4), soprano_two_musicmaker_three],
        [(52, 4), (53, 4), soprano_two_musicmaker_three],

        [(56, 4), (57, 4), soprano_two_musicmaker_one],
        [(57, 4), (58, 4), soprano_two_musicmaker_one],
        [(58, 4), (59, 4), soprano_two_musicmaker_one],
        [(59, 4), (60, 4), soprano_two_musicmaker_one],
        [(63, 4), (64, 4), soprano_two_musicmaker_one],
        [(64, 4), (65, 4), soprano_two_musicmaker_one],
        [(66, 4), (67, 4), soprano_two_musicmaker_two],
        [(67, 4), (68, 4), soprano_two_musicmaker_two],
        [(68, 4), (69, 4), soprano_two_musicmaker_two],
        [(69, 4), (70, 4), soprano_two_musicmaker_two],
        [(70, 4), (71, 4), soprano_two_musicmaker_two],
        [(71, 4), (72, 4), soprano_two_musicmaker_two],
        [(77, 4), (78, 4), soprano_two_musicmaker_three],
        [(78, 4), (79, 4), soprano_two_musicmaker_three],
        [(79, 4), (80, 4), soprano_two_musicmaker_three],
        [(80, 4), (81, 4), soprano_two_musicmaker_three],
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
        [(0, 4), (1, 4), soprano_three_musicmaker_one],
        [(1, 4), (2, 4), soprano_three_musicmaker_one],
        [(2, 4), (3, 4), soprano_three_musicmaker_one],
        [(5, 4), (6, 4), soprano_three_musicmaker_two],
        [(12, 4), (13, 4), soprano_three_musicmaker_two],
        [(13, 4), (14, 4), soprano_three_musicmaker_two],
        [(14, 4), (15, 4), soprano_three_musicmaker_two],
        [(15, 4), (16, 4), soprano_three_musicmaker_two],
        [(16, 4), (17, 4), soprano_three_musicmaker_one],
        [(21, 4), (22, 4), soprano_three_musicmaker_two],
        [(22, 4), (23, 4), soprano_three_musicmaker_two],
        [(23, 4), (24, 4), soprano_three_musicmaker_one],
        [(26, 4), (27, 4), soprano_three_musicmaker_one],

        [(28, 4), (29, 4), soprano_three_musicmaker_one],
        [(29, 4), (30, 4), soprano_three_musicmaker_one],
        [(30, 4), (31, 4), soprano_three_musicmaker_one],
        [(33, 4), (34, 4), soprano_three_musicmaker_two],
        [(40, 4), (41, 4), soprano_three_musicmaker_three],
        [(41, 4), (42, 4), soprano_three_musicmaker_three],
        [(42, 4), (43, 4), soprano_three_musicmaker_three],
        [(43, 4), (44, 4), soprano_three_musicmaker_three],
        [(44, 4), (45, 4), soprano_three_musicmaker_one],
        [(49, 4), (50, 4), soprano_three_musicmaker_two],
        [(50, 4), (51, 4), soprano_three_musicmaker_two],
        [(51, 4), (52, 4), soprano_three_musicmaker_three],
        [(54, 4), (55, 4), soprano_three_musicmaker_one],

        [(56, 4), (57, 4), soprano_three_musicmaker_one],
        [(57, 4), (58, 4), soprano_three_musicmaker_one],
        [(58, 4), (59, 4), soprano_three_musicmaker_one],
        [(61, 4), (62, 4), soprano_three_musicmaker_one],
        [(68, 4), (69, 4), soprano_three_musicmaker_two],
        [(69, 4), (70, 4), soprano_three_musicmaker_two],
        [(70, 4), (71, 4), soprano_three_musicmaker_two],
        [(71, 4), (72, 4), soprano_three_musicmaker_two],
        [(72, 4), (73, 4), soprano_three_musicmaker_two],
        [(77, 4), (78, 4), soprano_three_musicmaker_three],
        [(78, 4), (79, 4), soprano_three_musicmaker_three],
        [(79, 4), (80, 4), soprano_three_musicmaker_three],
        [(82, 4), (83, 4), soprano_three_musicmaker_one],
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
        [(0, 4), (1, 4), alto_one_musicmaker_two],
        [(1, 4), (2, 4), alto_one_musicmaker_two],
        [(3, 4), (4, 4), alto_one_musicmaker_two],
        [(4, 4), (5, 4), alto_one_musicmaker_two],
        [(5, 4), (6, 4), alto_one_musicmaker_one],
        [(6, 4), (7, 4), alto_one_musicmaker_one],
        [(7, 4), (8, 4), alto_one_musicmaker_one],
        [(8, 4), (9, 4), alto_one_musicmaker_one],
        [(14, 4), (15, 4), alto_one_musicmaker_two],
        [(15, 4), (16, 4), alto_one_musicmaker_two],
        [(16, 4), (17, 4), alto_one_musicmaker_one],
        [(17, 4), (18, 4), alto_one_musicmaker_one],
        [(21, 4), (22, 4), alto_one_musicmaker_one],
        [(22, 4), (23, 4), alto_one_musicmaker_one],
        [(47, 8), (24, 4), alto_one_musicmaker_two],
        [(24, 4), (25, 4), alto_one_musicmaker_two],
        [(25, 4), (26, 4), alto_one_musicmaker_two],
        [(26, 4), (27, 4), alto_one_musicmaker_two],
        [(27, 4), (28, 4), alto_one_musicmaker_two],

        [(28, 4), (29, 4), alto_one_musicmaker_one],
        [(29, 4), (30, 4), alto_one_musicmaker_one],
        [(31, 4), (32, 4), alto_one_musicmaker_two],
        [(32, 4), (33, 4), alto_one_musicmaker_two],
        [(33, 4), (34, 4), alto_one_musicmaker_three],
        [(34, 4), (35, 4), alto_one_musicmaker_three],
        [(35, 4), (36, 4), alto_one_musicmaker_three],
        [(36, 4), (37, 4), alto_one_musicmaker_three],
        [(42, 4), (43, 4), alto_one_musicmaker_one],
        [(43, 4), (44, 4), alto_one_musicmaker_one],
        [(44, 4), (45, 4), alto_one_musicmaker_two],
        [(45, 4), (46, 4), alto_one_musicmaker_two],
        [(48, 4), (49, 4), alto_one_musicmaker_three],
        [(49, 4), (50, 4), alto_one_musicmaker_three],
        [(52, 4), (53, 4), alto_one_musicmaker_one],
        [(53, 4), (54, 4), alto_one_musicmaker_one],
        [(54, 4), (55, 4), alto_one_musicmaker_one],
        [(55, 4), (56, 4), alto_one_musicmaker_one],

        [(56, 4), (57, 4), alto_one_musicmaker_one],
        [(57, 4), (58, 4), alto_one_musicmaker_one],
        [(59, 4), (60, 4), alto_one_musicmaker_one],
        [(60, 4), (61, 4), alto_one_musicmaker_one],
        [(61, 4), (62, 4), alto_one_musicmaker_two],
        [(62, 4), (63, 4), alto_one_musicmaker_two],
        [(63, 4), (64, 4), alto_one_musicmaker_two],
        [(64, 4), (65, 4), alto_one_musicmaker_two],
        [(70, 4), (71, 4), alto_one_musicmaker_two],
        [(71, 4), (72, 4), alto_one_musicmaker_two],
        [(72, 4), (73, 4), alto_one_musicmaker_three],
        [(73, 4), (74, 4), alto_one_musicmaker_three],
        [(76, 4), (77, 4), alto_one_musicmaker_three],
        [(77, 4), (78, 4), alto_one_musicmaker_three],
        [(80, 4), (81, 4), alto_one_musicmaker_one],
        [(81, 4), (82, 4), alto_one_musicmaker_one],
        [(82, 4), (83, 4), alto_one_musicmaker_one],
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
        [(0, 4), (1, 4), alto_two_musicmaker_two],
        [(7, 4), (8, 4), alto_two_musicmaker_one],
        [(8, 4), (9, 4), alto_two_musicmaker_one],
        [(9, 4), (10, 4), alto_two_musicmaker_two],
        [(10, 4), (11, 4), alto_two_musicmaker_two],
        [(11, 4), (12, 4), alto_two_musicmaker_two],
        [(16, 4), (17, 4), alto_two_musicmaker_one],
        [(17, 4), (18, 4), alto_two_musicmaker_one],
        [(18, 4), (19, 4), alto_two_musicmaker_one],
        [(21, 4), (22, 4), alto_two_musicmaker_one],

        [(28, 4), (29, 4), alto_two_musicmaker_one],
        [(35, 4), (36, 4), alto_two_musicmaker_two],
        [(36, 4), (37, 4), alto_two_musicmaker_two],
        [(37, 4), (38, 4), alto_two_musicmaker_three],
        [(38, 4), (39, 4), alto_two_musicmaker_three],
        [(39, 4), (40, 4), alto_two_musicmaker_three],
        [(44, 4), (45, 4), alto_two_musicmaker_one],
        [(45, 4), (46, 4), alto_two_musicmaker_one],
        [(46, 4), (47, 4), alto_two_musicmaker_one],
        [(49, 4), (50, 4), alto_two_musicmaker_two],

        [(56, 4), (57, 4), alto_two_musicmaker_one],
        [(63, 4), (64, 4), alto_two_musicmaker_one],
        [(64, 4), (65, 4), alto_two_musicmaker_one],
        [(65, 4), (66, 4), alto_two_musicmaker_two],
        [(66, 4), (67, 4), alto_two_musicmaker_two],
        [(67, 4), (68, 4), alto_two_musicmaker_two],
        [(72, 4), (73, 4), alto_two_musicmaker_two],
        [(73, 4), (74, 4), alto_two_musicmaker_two],
        [(74, 4), (75, 4), alto_two_musicmaker_two],
        [(77, 4), (78, 4), alto_two_musicmaker_three],
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
        [(0, 4), (1, 4), alto_three_musicmaker_one],
        [(1, 4), (2, 4), alto_three_musicmaker_one],
        [(2, 4), (3, 4), alto_three_musicmaker_one],
        [(3, 4), (4, 4), alto_three_musicmaker_one],
        [(4, 4), (5, 4), alto_three_musicmaker_one],
        [(5, 4), (6, 4), alto_three_musicmaker_two],
        [(11, 4), (12, 4), alto_three_musicmaker_one],
        [(12, 4), (13, 4), alto_three_musicmaker_one],
        [(13, 4), (14, 4), alto_three_musicmaker_one],
        [(14, 4), (15, 4), alto_three_musicmaker_one],
        [(18, 4), (19, 4), alto_three_musicmaker_two],
        [(19, 4), (20, 4), alto_three_musicmaker_one],
        [(21, 4), (22, 4), alto_three_musicmaker_two],
        [(22, 4), (23, 4), alto_three_musicmaker_two],
        [(23, 4), (24, 4), alto_three_musicmaker_two],
        [(24, 4), (25, 4), alto_three_musicmaker_two],
        [(25, 4), (26, 4), alto_three_musicmaker_two],
        [(26, 4), (27, 4), alto_three_musicmaker_two],

        [(28, 4), (29, 4), alto_three_musicmaker_one],
        [(29, 4), (30, 4), alto_three_musicmaker_one],
        [(30, 4), (31, 4), alto_three_musicmaker_one],
        [(31, 4), (32, 4), alto_three_musicmaker_one],
        [(32, 4), (33, 4), alto_three_musicmaker_one],
        [(33, 4), (34, 4), alto_three_musicmaker_two],
        [(39, 4), (40, 4), alto_three_musicmaker_three],
        [(40, 4), (41, 4), alto_three_musicmaker_one],
        [(41, 4), (42, 4), alto_three_musicmaker_one],
        [(42, 4), (43, 4), alto_three_musicmaker_one],
        [(46, 4), (47, 4), alto_three_musicmaker_two],
        [(47, 4), (48, 4), alto_three_musicmaker_three],
        [(49, 4), (50, 4), alto_three_musicmaker_one],
        [(50, 4), (51, 4), alto_three_musicmaker_one],
        [(51, 4), (52, 4), alto_three_musicmaker_two],
        [(52, 4), (53, 4), alto_three_musicmaker_two],
        [(53, 4), (54, 4), alto_three_musicmaker_two],
        [(54, 4), (55, 4), alto_three_musicmaker_two],

        [(56, 4), (57, 4), alto_three_musicmaker_one],
        [(57, 4), (58, 4), alto_three_musicmaker_one],
        [(58, 4), (59, 4), alto_three_musicmaker_one],
        [(59, 4), (60, 4), alto_three_musicmaker_one],
        [(60, 4), (61, 4), alto_three_musicmaker_one],
        [(61, 4), (62, 4), alto_three_musicmaker_one],
        [(67, 4), (68, 4), alto_three_musicmaker_two],
        [(68, 4), (69, 4), alto_three_musicmaker_two],
        [(69, 4), (70, 4), alto_three_musicmaker_two],
        [(70, 4), (71, 4), alto_three_musicmaker_two],
        [(74, 4), (75, 4), alto_three_musicmaker_three],
        [(75, 4), (76, 4), alto_three_musicmaker_three],
        [(77, 4), (78, 4), alto_three_musicmaker_one],
        [(78, 4), (79, 4), alto_three_musicmaker_one],
        [(79, 4), (80, 4), alto_three_musicmaker_two],
        [(80, 4), (81, 4), alto_three_musicmaker_two],
        [(81, 4), (82, 4), alto_three_musicmaker_two],
        [(82, 4), (83, 4), alto_three_musicmaker_two],
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
        [(0, 4), (1, 4), alto_four_musicmaker_two],
        [(1, 4), (2, 4), alto_four_musicmaker_two],
        [(2, 4), (3, 4), alto_four_musicmaker_two],
        [(3, 4), (4, 4), alto_four_musicmaker_two],
        [(4, 4), (5, 4), alto_four_musicmaker_two],
        [(9, 4), (10, 4), alto_four_musicmaker_one],
        [(10, 4), (11, 4), alto_four_musicmaker_one],
        [(11, 4), (12, 4), alto_four_musicmaker_one],
        [(14, 4), (15, 4), alto_four_musicmaker_one],
        [(21, 4), (22, 4), alto_four_musicmaker_two],
        [(22, 4), (23, 4), alto_four_musicmaker_two],
        [(23, 4), (24, 4), alto_four_musicmaker_one],
        [(24, 4), (25, 4), alto_four_musicmaker_one],
        [(25, 4), (26, 4), alto_four_musicmaker_one],

        [(28, 4), (29, 4), alto_four_musicmaker_one],
        [(29, 4), (30, 4), alto_four_musicmaker_one],
        [(30, 4), (31, 4), alto_four_musicmaker_one],
        [(31, 4), (32, 4), alto_four_musicmaker_one],
        [(32, 4), (33, 4), alto_four_musicmaker_one],
        [(37, 4), (38, 4), alto_four_musicmaker_two],
        [(38, 4), (39, 4), alto_four_musicmaker_two],
        [(39, 4), (40, 4), alto_four_musicmaker_two],
        [(42, 4), (43, 4), alto_four_musicmaker_three],
        [(49, 4), (50, 4), alto_four_musicmaker_one],
        [(50, 4), (51, 4), alto_four_musicmaker_one],
        [(51, 4), (52, 4), alto_four_musicmaker_two],
        [(52, 4), (53, 4), alto_four_musicmaker_two],
        [(53, 4), (54, 4), alto_four_musicmaker_two],

        [(56, 4), (57, 4), alto_four_musicmaker_one],
        [(57, 4), (58, 4), alto_four_musicmaker_one],
        [(58, 4), (59, 4), alto_four_musicmaker_one],
        [(59, 4), (60, 4), alto_four_musicmaker_one],
        [(60, 4), (61, 4), alto_four_musicmaker_one],
        [(65, 4), (66, 4), alto_four_musicmaker_one],
        [(66, 4), (67, 4), alto_four_musicmaker_one],
        [(67, 4), (68, 4), alto_four_musicmaker_one],
        [(70, 4), (71, 4), alto_four_musicmaker_two],
        [(77, 4), (78, 4), alto_four_musicmaker_two],
        [(78, 4), (79, 4), alto_four_musicmaker_two],
        [(79, 4), (80, 4), alto_four_musicmaker_three],
        [(80, 4), (81, 4), alto_four_musicmaker_three],
        [(81, 4), (82, 4), alto_four_musicmaker_three],
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
        [(0, 4), (1, 4), alto_five_musicmaker_one],
        [(1, 4), (2, 4), alto_five_musicmaker_one],
        [(2, 4), (3, 4), alto_five_musicmaker_one],
        [(3, 4), (4, 4), alto_five_musicmaker_one],
        [(7, 4), (8, 4), alto_five_musicmaker_one],
        [(8, 4), (9, 4), alto_five_musicmaker_one],
        [(10, 4), (11, 4), alto_five_musicmaker_two],
        [(11, 4), (12, 4), alto_five_musicmaker_two],
        [(12, 4), (13, 4), alto_five_musicmaker_one],
        [(13, 4), (14, 4), alto_five_musicmaker_one],
        [(14, 4), (15, 4), alto_five_musicmaker_one],
        [(15, 4), (16, 4), alto_five_musicmaker_one],
        [(21, 4), (22, 4), alto_five_musicmaker_two],
        [(22, 4), (23, 4), alto_five_musicmaker_two],
        [(23, 4), (24, 4), alto_five_musicmaker_two],
        [(24, 4), (25, 4), alto_five_musicmaker_two],

        [(28, 4), (29, 4), alto_five_musicmaker_one],
        [(29, 4), (30, 4), alto_five_musicmaker_one],
        [(30, 4), (31, 4), alto_five_musicmaker_one],
        [(31, 4), (32, 4), alto_five_musicmaker_one],
        [(35, 4), (36, 4), alto_five_musicmaker_two],
        [(36, 4), (37, 4), alto_five_musicmaker_two],
        [(38, 4), (39, 4), alto_five_musicmaker_three],
        [(39, 4), (40, 4), alto_five_musicmaker_three],
        [(40, 4), (41, 4), alto_five_musicmaker_one],
        [(41, 4), (42, 4), alto_five_musicmaker_one],
        [(42, 4), (43, 4), alto_five_musicmaker_one],
        [(43, 4), (44, 4), alto_five_musicmaker_one],
        [(49, 4), (50, 4), alto_five_musicmaker_two],
        [(50, 4), (51, 4), alto_five_musicmaker_two],
        [(51, 4), (52, 4), alto_five_musicmaker_three],
        [(52, 4), (53, 4), alto_five_musicmaker_three],

        [(56, 4), (57, 4), alto_five_musicmaker_one],
        [(57, 4), (58, 4), alto_five_musicmaker_one],
        [(58, 4), (59, 4), alto_five_musicmaker_one],
        [(59, 4), (60, 4), alto_five_musicmaker_one],
        [(63, 4), (64, 4), alto_five_musicmaker_one],
        [(64, 4), (65, 4), alto_five_musicmaker_one],
        [(66, 4), (67, 4), alto_five_musicmaker_two],
        [(67, 4), (68, 4), alto_five_musicmaker_two],
        [(68, 4), (69, 4), alto_five_musicmaker_two],
        [(69, 4), (70, 4), alto_five_musicmaker_two],
        [(70, 4), (71, 4), alto_five_musicmaker_two],
        [(71, 4), (72, 4), alto_five_musicmaker_two],
        [(77, 4), (79, 4), alto_five_musicmaker_three],
        [(79, 4), (80, 4), alto_five_musicmaker_three],
        [(80, 4), (81, 4), alto_five_musicmaker_three],
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
        [(0, 4), (1, 4), alto_six_musicmaker_one],
        [(1, 4), (2, 4), alto_six_musicmaker_one],
        [(2, 4), (3, 4), alto_six_musicmaker_one],
        [(5, 4), (6, 4), alto_six_musicmaker_two],
        [(12, 4), (13, 4), alto_six_musicmaker_one],
        [(13, 4), (14, 4), alto_six_musicmaker_one],
        [(14, 4), (15, 4), alto_six_musicmaker_one],
        [(15, 4), (16, 4), alto_six_musicmaker_one],
        [(16, 4), (17, 4), alto_six_musicmaker_two],
        [(21, 4), (22, 4), alto_six_musicmaker_two],
        [(22, 4), (23, 4), alto_six_musicmaker_two],
        [(23, 4), (24, 4), alto_six_musicmaker_one],
        [(26, 4), (27, 4), alto_six_musicmaker_two],
        [(27, 4), (28, 4), alto_six_musicmaker_two],

        [(28, 4), (29, 4), alto_six_musicmaker_one],
        [(29, 4), (30, 4), alto_six_musicmaker_one],
        [(30, 4), (31, 4), alto_six_musicmaker_one],
        [(33, 4), (34, 4), alto_six_musicmaker_two],
        [(40, 4), (41, 4), alto_six_musicmaker_three],
        [(41, 4), (42, 4), alto_six_musicmaker_three],
        [(42, 4), (43, 4), alto_six_musicmaker_three],
        [(43, 4), (44, 4), alto_six_musicmaker_three],
        [(44, 4), (45, 4), alto_six_musicmaker_one],
        [(48, 4), (49, 4), alto_six_musicmaker_two],
        [(49, 4), (50, 4), alto_six_musicmaker_two],
        [(51, 4), (52, 4), alto_six_musicmaker_three],
        [(54, 4), (55, 4), alto_six_musicmaker_one],

        [(56, 4), (57, 4), alto_six_musicmaker_one],
        [(57, 4), (58, 4), alto_six_musicmaker_one],
        [(58, 4), (59, 4), alto_six_musicmaker_one],
        [(61, 4), (62, 4), alto_six_musicmaker_one],
        [(68, 4), (69, 4), alto_six_musicmaker_two],
        [(69, 4), (70, 4), alto_six_musicmaker_two],
        [(70, 4), (71, 4), alto_six_musicmaker_two],
        [(71, 4), (72, 4), alto_six_musicmaker_two],
        [(72, 4), (73, 4), alto_six_musicmaker_two],
        [(76, 4), (77, 4), alto_six_musicmaker_three],
        [(77, 4), (78, 4), alto_six_musicmaker_three],
        [(78, 4), (79, 4), alto_six_musicmaker_three],
        [(82, 4), (83, 4), alto_six_musicmaker_one],
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
        [(0, 4), (1, 4), tenor_one_musicmaker_two],
        [(1, 4), (2, 4), tenor_one_musicmaker_two],
        [(3, 4), (4, 4), tenor_one_musicmaker_one],
        [(4, 4), (5, 4), tenor_one_musicmaker_one],
        [(5, 4), (6, 4), tenor_one_musicmaker_two],
        [(6, 4), (7, 4), tenor_one_musicmaker_two],
        [(7, 4), (8, 4), tenor_one_musicmaker_two],
        [(8, 4), (9, 4), tenor_one_musicmaker_two],
        [(14, 4), (15, 4), tenor_one_musicmaker_two],
        [(15, 4), (16, 4), tenor_one_musicmaker_two],
        [(16, 4), (17, 4), tenor_one_musicmaker_one],
        [(17, 4), (18, 4), tenor_one_musicmaker_one],
        [(21, 4), (22, 4), tenor_one_musicmaker_two],
        [(22, 4), (23, 4), tenor_one_musicmaker_two],
        [(24, 4), (25, 4), tenor_one_musicmaker_one],
        [(25, 4), (26, 4), tenor_one_musicmaker_one],
        [(26, 4), (27, 4), tenor_one_musicmaker_one],

        [(28, 4), (29, 4), tenor_one_musicmaker_one],
        [(29, 4), (30, 4), tenor_one_musicmaker_one],
        [(31, 4), (32, 4), tenor_one_musicmaker_two],
        [(32, 4), (33, 4), tenor_one_musicmaker_two],
        [(33, 4), (34, 4), tenor_one_musicmaker_three],
        [(34, 4), (35, 4), tenor_one_musicmaker_three],
        [(35, 4), (36, 4), tenor_one_musicmaker_three],
        [(36, 4), (37, 4), tenor_one_musicmaker_three],
        [(42, 4), (43, 4), tenor_one_musicmaker_one],
        [(43, 4), (44, 4), tenor_one_musicmaker_one],
        [(44, 4), (45, 4), tenor_one_musicmaker_two],
        [(45, 4), (46, 4), tenor_one_musicmaker_two],
        [(49, 4), (50, 4), tenor_one_musicmaker_three],
        [(50, 4), (51, 4), tenor_one_musicmaker_three],
        [(52, 4), (53, 4), tenor_one_musicmaker_one],
        [(53, 4), (54, 4), tenor_one_musicmaker_one],
        [(54, 4), (55, 4), tenor_one_musicmaker_one],

        [(56, 4), (57, 4), tenor_one_musicmaker_one],
        [(57, 4), (58, 4), tenor_one_musicmaker_one],
        [(59, 4), (60, 4), tenor_one_musicmaker_one],
        [(60, 4), (61, 4), tenor_one_musicmaker_one],
        [(61, 4), (62, 4), tenor_one_musicmaker_two],
        [(62, 4), (63, 4), tenor_one_musicmaker_two],
        [(63, 4), (64, 4), tenor_one_musicmaker_two],
        [(64, 4), (65, 4), tenor_one_musicmaker_two],
        [(70, 4), (71, 4), tenor_one_musicmaker_two],
        [(71, 4), (72, 4), tenor_one_musicmaker_two],
        [(72, 4), (73, 4), tenor_one_musicmaker_three],
        [(73, 4), (74, 4), tenor_one_musicmaker_three],
        [(77, 4), (78, 4), tenor_one_musicmaker_three],
        [(78, 4), (79, 4), tenor_one_musicmaker_three],
        [(80, 4), (81, 4), tenor_one_musicmaker_one],
        [(81, 4), (82, 4), tenor_one_musicmaker_one],
        [(82, 4), (83, 4), tenor_one_musicmaker_one],
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
        [(0, 4), (1, 4), tenor_two_musicmaker_one],
        [(7, 4), (8, 4), tenor_two_musicmaker_two],
        [(8, 4), (9, 4), tenor_two_musicmaker_two],
        [(9, 4), (10, 4), tenor_two_musicmaker_two],
        [(10, 4), (11, 4), tenor_two_musicmaker_two],
        [(11, 4), (12, 4), tenor_two_musicmaker_two],
        [(16, 4), (17, 4), tenor_two_musicmaker_one],
        [(17, 4), (18, 4), tenor_two_musicmaker_one],
        [(18, 4), (19, 4), tenor_two_musicmaker_one],
        [(21, 4), (22, 4), tenor_two_musicmaker_two],

        [(28, 4), (29, 4), tenor_two_musicmaker_one],
        [(35, 4), (36, 4), tenor_two_musicmaker_two],
        [(36, 4), (37, 4), tenor_two_musicmaker_two],
        [(37, 4), (38, 4), tenor_two_musicmaker_three],
        [(38, 4), (39, 4), tenor_two_musicmaker_three],
        [(39, 4), (40, 4), tenor_two_musicmaker_three],
        [(44, 4), (45, 4), tenor_two_musicmaker_one],
        [(45, 4), (46, 4), tenor_two_musicmaker_one],
        [(46, 4), (47, 4), tenor_two_musicmaker_one],
        [(49, 4), (50, 4), tenor_two_musicmaker_two],

        [(56, 4), (57, 4), tenor_two_musicmaker_one],
        [(63, 4), (64, 4), tenor_two_musicmaker_one],
        [(64, 4), (65, 4), tenor_two_musicmaker_one],
        [(65, 4), (66, 4), tenor_two_musicmaker_two],
        [(66, 4), (67, 4), tenor_two_musicmaker_two],
        [(67, 4), (68, 4), tenor_two_musicmaker_two],
        [(72, 4), (73, 4), tenor_two_musicmaker_two],
        [(73, 4), (74, 4), tenor_two_musicmaker_two],
        [(74, 4), (75, 4), tenor_two_musicmaker_two],
        [(77, 4), (78, 4), tenor_two_musicmaker_three],
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
        [(0, 4), (1, 4), tenor_three_musicmaker_two],
        [(1, 4), (2, 4), tenor_three_musicmaker_two],
        [(2, 4), (3, 4), tenor_three_musicmaker_two],
        [(3, 4), (4, 4), tenor_three_musicmaker_two],
        [(4, 4), (5, 4), tenor_three_musicmaker_two],
        [(5, 4), (6, 4), tenor_three_musicmaker_two],
        [(11, 4), (12, 4), tenor_three_musicmaker_one],
        [(12, 4), (13, 4), tenor_three_musicmaker_two],
        [(13, 4), (14, 4), tenor_three_musicmaker_two],
        [(14, 4), (15, 4), tenor_three_musicmaker_two],
        [(18, 4), (19, 4), tenor_three_musicmaker_one],
        [(19, 4), (20, 4), tenor_three_musicmaker_one],
        [(21, 4), (22, 4), tenor_three_musicmaker_two],
        [(22, 4), (23, 4), tenor_three_musicmaker_two],
        [(23, 4), (24, 4), tenor_three_musicmaker_one],
        [(24, 4), (25, 4), tenor_three_musicmaker_one],
        [(25, 4), (26, 4), tenor_three_musicmaker_one],
        [(26, 4), (27, 4), tenor_three_musicmaker_one],

        [(28, 4), (29, 4), tenor_three_musicmaker_one],
        [(29, 4), (30, 4), tenor_three_musicmaker_one],
        [(30, 4), (31, 4), tenor_three_musicmaker_one],
        [(32, 4), (33, 4), tenor_three_musicmaker_one],
        [(33, 4), (34, 4), tenor_three_musicmaker_two],
        [(39, 4), (40, 4), tenor_three_musicmaker_three],
        [(40, 4), (41, 4), tenor_three_musicmaker_one],
        [(41, 4), (42, 4), tenor_three_musicmaker_one],
        [(42, 4), (43, 4), tenor_three_musicmaker_one],
        [(46, 4), (47, 4), tenor_three_musicmaker_two],
        [(47, 4), (48, 4), tenor_three_musicmaker_three],
        [(49, 4), (50, 4), tenor_three_musicmaker_one],
        [(50, 4), (51, 4), tenor_three_musicmaker_one],
        [(51, 4), (52, 4), tenor_three_musicmaker_two],
        [(52, 4), (53, 4), tenor_three_musicmaker_two],
        [(53, 4), (54, 4), tenor_three_musicmaker_two],
        [(54, 4), (55, 4), tenor_three_musicmaker_two],

        [(56, 4), (57, 4), tenor_three_musicmaker_one],
        [(57, 4), (58, 4), tenor_three_musicmaker_one],
        [(58, 4), (59, 4), tenor_three_musicmaker_one],
        [(59, 4), (60, 4), tenor_three_musicmaker_one],
        [(60, 4), (61, 4), tenor_three_musicmaker_one],
        [(61, 4), (62, 4), tenor_three_musicmaker_one],
        [(67, 4), (68, 4), tenor_three_musicmaker_two],
        [(68, 4), (69, 4), tenor_three_musicmaker_two],
        [(69, 4), (70, 4), tenor_three_musicmaker_two],
        [(70, 4), (71, 4), tenor_three_musicmaker_two],
        [(74, 4), (75, 4), tenor_three_musicmaker_three],
        [(75, 4), (76, 4), tenor_three_musicmaker_three],
        [(77, 4), (78, 4), tenor_three_musicmaker_one],
        [(78, 4), (79, 4), tenor_three_musicmaker_one],
        [(79, 4), (80, 4), tenor_three_musicmaker_two],
        [(80, 4), (81, 4), tenor_three_musicmaker_two],
        [(81, 4), (82, 4), tenor_three_musicmaker_two],
        [(82, 4), (83, 4), tenor_three_musicmaker_two],
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
        [(0, 4), (1, 4), tenor_four_musicmaker_two],
        [(1, 4), (2, 4), tenor_four_musicmaker_two],
        [(2, 4), (3, 4), tenor_four_musicmaker_two],
        [(3, 4), (4, 4), tenor_four_musicmaker_two],
        [(4, 4), (5, 4), tenor_four_musicmaker_two],
        [(9, 4), (10, 4), tenor_four_musicmaker_one],
        [(10, 4), (11, 4), tenor_four_musicmaker_one],
        [(11, 4), (12, 4), tenor_four_musicmaker_one],
        [(14, 4), (15, 4), tenor_four_musicmaker_two],
        [(21, 4), (22, 4), tenor_four_musicmaker_one],
        [(22, 4), (23, 4), tenor_four_musicmaker_one],
        [(23, 4), (24, 4), tenor_four_musicmaker_one],
        [(24, 4), (25, 4), tenor_four_musicmaker_one],
        [(25, 4), (26, 4), tenor_four_musicmaker_one],

        [(28, 4), (29, 4), tenor_four_musicmaker_one],
        [(29, 4), (30, 4), tenor_four_musicmaker_one],
        [(30, 4), (31, 4), tenor_four_musicmaker_one],
        [(31, 4), (32, 4), tenor_four_musicmaker_one],
        [(32, 4), (33, 4), tenor_four_musicmaker_one],
        [(37, 4), (38, 4), tenor_four_musicmaker_two],
        [(38, 4), (39, 4), tenor_four_musicmaker_two],
        [(39, 4), (40, 4), tenor_four_musicmaker_two],
        [(42, 4), (43, 4), tenor_four_musicmaker_three],
        [(49, 4), (50, 4), tenor_four_musicmaker_one],
        [(50, 4), (51, 4), tenor_four_musicmaker_one],
        [(51, 4), (52, 4), tenor_four_musicmaker_two],
        [(52, 4), (53, 4), tenor_four_musicmaker_two],
        [(53, 4), (54, 4), tenor_four_musicmaker_two],

        [(56, 4), (57, 4), tenor_four_musicmaker_one],
        [(57, 4), (58, 4), tenor_four_musicmaker_one],
        [(58, 4), (59, 4), tenor_four_musicmaker_one],
        [(59, 4), (60, 4), tenor_four_musicmaker_one],
        [(60, 4), (61, 4), tenor_four_musicmaker_one],
        [(65, 4), (66, 4), tenor_four_musicmaker_one],
        [(66, 4), (67, 4), tenor_four_musicmaker_one],
        [(67, 4), (68, 4), tenor_four_musicmaker_one],
        [(70, 4), (71, 4), tenor_four_musicmaker_two],
        [(77, 4), (78, 4), tenor_four_musicmaker_two],
        [(78, 4), (79, 4), tenor_four_musicmaker_two],
        [(79, 4), (80, 4), tenor_four_musicmaker_three],
        [(80, 4), (81, 4), tenor_four_musicmaker_three],
        [(81, 4), (82, 4), tenor_four_musicmaker_three],
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
        [(0, 4), (1, 4), tenor_five_musicmaker_one],
        [(1, 4), (2, 4), tenor_five_musicmaker_one],
        [(2, 4), (3, 4), tenor_five_musicmaker_one],
        [(3, 4), (4, 4), tenor_five_musicmaker_one],
        [(7, 4), (8, 4), tenor_five_musicmaker_two],
        [(8, 4), (9, 4), tenor_five_musicmaker_two],
        [(10, 4), (11, 4), tenor_five_musicmaker_one],
        [(11, 4), (12, 4), tenor_five_musicmaker_one],
        [(12, 4), (13, 4), tenor_five_musicmaker_one],
        [(13, 4), (14, 4), tenor_five_musicmaker_one],
        [(14, 4), (15, 4), tenor_five_musicmaker_one],
        [(15, 4), (16, 4), tenor_five_musicmaker_one],
        [(21, 4), (22, 4), tenor_five_musicmaker_two],
        [(22, 4), (23, 4), tenor_five_musicmaker_two],
        [(23, 4), (24, 4), tenor_five_musicmaker_one],
        [(24, 4), (25, 4), tenor_five_musicmaker_one],

        [(28, 4), (29, 4), tenor_five_musicmaker_one],
        [(29, 4), (30, 4), tenor_five_musicmaker_one],
        [(30, 4), (31, 4), tenor_five_musicmaker_one],
        [(31, 4), (32, 4), tenor_five_musicmaker_one],
        [(35, 4), (36, 4), tenor_five_musicmaker_two],
        [(36, 4), (37, 4), tenor_five_musicmaker_two],
        [(38, 4), (39, 4), tenor_five_musicmaker_three],
        [(39, 4), (40, 4), tenor_five_musicmaker_three],
        [(40, 4), (41, 4), tenor_five_musicmaker_one],
        [(41, 4), (42, 4), tenor_five_musicmaker_one],
        [(42, 4), (43, 4), tenor_five_musicmaker_one],
        [(43, 4), (44, 4), tenor_five_musicmaker_one],
        [(49, 4), (50, 4), tenor_five_musicmaker_two],
        [(50, 4), (51, 4), tenor_five_musicmaker_two],
        [(51, 4), (52, 4), tenor_five_musicmaker_three],
        [(52, 4), (53, 4), tenor_five_musicmaker_three],

        [(56, 4), (57, 4), tenor_five_musicmaker_one],
        [(57, 4), (58, 4), tenor_five_musicmaker_one],
        [(58, 4), (59, 4), tenor_five_musicmaker_one],
        [(59, 4), (60, 4), tenor_five_musicmaker_one],
        [(63, 4), (64, 4), tenor_five_musicmaker_one],
        [(64, 4), (65, 4), tenor_five_musicmaker_one],
        [(66, 4), (67, 4), tenor_five_musicmaker_two],
        [(67, 4), (68, 4), tenor_five_musicmaker_two],
        [(68, 4), (69, 4), tenor_five_musicmaker_two],
        [(69, 4), (70, 4), tenor_five_musicmaker_two],
        [(70, 4), (71, 4), tenor_five_musicmaker_two],
        [(71, 4), (72, 4), tenor_five_musicmaker_two],
        [(77, 4), (78, 4), tenor_five_musicmaker_three],
        [(78, 4), (79, 4), tenor_five_musicmaker_three],
        [(79, 4), (80, 4), tenor_five_musicmaker_three],
        [(80, 4), (81, 4), tenor_five_musicmaker_three],
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
        [(0, 4), (1, 4), baritone_one_musicmaker_two],
        [(1, 4), (2, 4), baritone_one_musicmaker_two],
        [(2, 4), (3, 4), baritone_one_musicmaker_two],
        [(5, 4), (6, 4), baritone_one_musicmaker_one],
        [(12, 4), (13, 4), baritone_one_musicmaker_one],
        [(13, 4), (14, 4), baritone_one_musicmaker_one],
        [(14, 4), (15, 4), baritone_one_musicmaker_one],
        [(15, 4), (16, 4), baritone_one_musicmaker_one],
        [(16, 4), (17, 4), baritone_one_musicmaker_two],
        [(21, 4), (22, 4), baritone_one_musicmaker_one],
        [(22, 4), (23, 4), baritone_one_musicmaker_one],
        [(23, 4), (24, 4), baritone_one_musicmaker_two],
        [(26, 4), (27, 4), baritone_one_musicmaker_two],

        [(28, 4), (29, 4), baritone_one_musicmaker_one],
        [(29, 4), (30, 4), baritone_one_musicmaker_one],
        [(30, 4), (31, 4), baritone_one_musicmaker_one],
        [(33, 4), (34, 4), baritone_one_musicmaker_two],
        [(40, 4), (41, 4), baritone_one_musicmaker_three],
        [(41, 4), (42, 4), baritone_one_musicmaker_three],
        [(42, 4), (43, 4), baritone_one_musicmaker_three],
        [(43, 4), (44, 4), baritone_one_musicmaker_three],
        [(44, 4), (45, 4), baritone_one_musicmaker_one],
        [(49, 4), (50, 4), baritone_one_musicmaker_two],
        [(50, 4), (51, 4), baritone_one_musicmaker_two],
        [(51, 4), (52, 4), baritone_one_musicmaker_three],
        [(54, 4), (55, 4), baritone_one_musicmaker_one],

        [(56, 4), (57, 4), baritone_one_musicmaker_one],
        [(57, 4), (58, 4), baritone_one_musicmaker_one],
        [(58, 4), (59, 4), baritone_one_musicmaker_one],
        [(61, 4), (62, 4), baritone_one_musicmaker_one],
        [(68, 4), (69, 4), baritone_one_musicmaker_two],
        [(69, 4), (70, 4), baritone_one_musicmaker_two],
        [(70, 4), (71, 4), baritone_one_musicmaker_two],
        [(71, 4), (72, 4), baritone_one_musicmaker_two],
        [(72, 4), (73, 4), baritone_one_musicmaker_two],
        [(77, 4), (78, 4), baritone_one_musicmaker_three],
        [(78, 4), (79, 4), baritone_one_musicmaker_three],
        [(79, 4), (80, 4), baritone_one_musicmaker_three],
        [(82, 4), (83, 4), baritone_one_musicmaker_one],
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
        [(0, 4), (1, 4), baritone_two_musicmaker_one],
        [(1, 4), (2, 4), baritone_two_musicmaker_one],
        [(3, 4), (4, 4), baritone_two_musicmaker_one],
        [(4, 4), (5, 4), baritone_two_musicmaker_one],
        [(5, 4), (6, 4), baritone_two_musicmaker_two],
        [(6, 4), (7, 4), baritone_two_musicmaker_two],
        [(7, 4), (8, 4), baritone_two_musicmaker_two],
        [(8, 4), (9, 4), baritone_two_musicmaker_two],
        [(14, 4), (15, 4), baritone_two_musicmaker_one],
        [(15, 4), (16, 4), baritone_two_musicmaker_one],
        [(16, 4), (17, 4), baritone_two_musicmaker_two],
        [(17, 4), (18, 4), baritone_two_musicmaker_two],
        [(21, 4), (22, 4), baritone_two_musicmaker_two],
        [(22, 4), (23, 4), baritone_two_musicmaker_two],
        [(24, 4), (25, 4), baritone_two_musicmaker_one],
        [(25, 4), (26, 4), baritone_two_musicmaker_one],
        [(26, 4), (27, 4), baritone_two_musicmaker_one],

        [(28, 4), (29, 4), baritone_two_musicmaker_one],
        [(29, 4), (30, 4), baritone_two_musicmaker_one],
        [(31, 4), (32, 4), baritone_two_musicmaker_two],
        [(32, 4), (33, 4), baritone_two_musicmaker_two],
        [(33, 4), (34, 4), baritone_two_musicmaker_three],
        [(34, 4), (35, 4), baritone_two_musicmaker_three],
        [(35, 4), (36, 4), baritone_two_musicmaker_three],
        [(36, 4), (37, 4), baritone_two_musicmaker_three],
        [(42, 4), (43, 4), baritone_two_musicmaker_one],
        [(43, 4), (44, 4), baritone_two_musicmaker_one],
        [(44, 4), (45, 4), baritone_two_musicmaker_two],
        [(45, 4), (46, 4), baritone_two_musicmaker_two],
        [(49, 4), (50, 4), baritone_two_musicmaker_three],
        [(50, 4), (51, 4), baritone_two_musicmaker_three],
        [(52, 4), (53, 4), baritone_two_musicmaker_one],
        [(53, 4), (54, 4), baritone_two_musicmaker_one],
        [(54, 4), (55, 4), baritone_two_musicmaker_one],

        [(56, 4), (57, 4), baritone_two_musicmaker_one],
        [(57, 4), (58, 4), baritone_two_musicmaker_one],
        [(59, 4), (60, 4), baritone_two_musicmaker_one],
        [(60, 4), (61, 4), baritone_two_musicmaker_one],
        [(61, 4), (62, 4), baritone_two_musicmaker_two],
        [(62, 4), (63, 4), baritone_two_musicmaker_two],
        [(63, 4), (64, 4), baritone_two_musicmaker_two],
        [(64, 4), (65, 4), baritone_two_musicmaker_two],
        [(70, 4), (71, 4), baritone_two_musicmaker_two],
        [(71, 4), (72, 4), baritone_two_musicmaker_two],
        [(72, 4), (73, 4), baritone_two_musicmaker_three],
        [(73, 4), (74, 4), baritone_two_musicmaker_three],
        [(77, 4), (78, 4), baritone_two_musicmaker_three],
        [(78, 4), (79, 4), baritone_two_musicmaker_three],
        [(80, 4), (81, 4), baritone_two_musicmaker_one],
        [(81, 4), (82, 4), baritone_two_musicmaker_one],
        [(82, 4), (83, 4), baritone_two_musicmaker_one],
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
        [(0, 4), (1, 4), baritone_three_musicmaker_one],
        [(7, 4), (8, 4), baritone_three_musicmaker_two],
        [(8, 4), (9, 4), baritone_three_musicmaker_two],
        [(9, 4), (10, 4), baritone_three_musicmaker_one],
        [(10, 4), (11, 4), baritone_three_musicmaker_one],
        [(11, 4), (12, 4), baritone_three_musicmaker_one],
        [(16, 4), (17, 4), baritone_three_musicmaker_two],
        [(17, 4), (18, 4), baritone_three_musicmaker_two],
        [(18, 4), (19, 4), baritone_three_musicmaker_two],
        [(21, 4), (22, 4), baritone_three_musicmaker_two],

        [(28, 4), (29, 4), baritone_three_musicmaker_one],
        [(35, 4), (36, 4), baritone_three_musicmaker_two],
        [(36, 4), (37, 4), baritone_three_musicmaker_two],
        [(37, 4), (38, 4), baritone_three_musicmaker_three],
        [(38, 4), (39, 4), baritone_three_musicmaker_three],
        [(39, 4), (40, 4), baritone_three_musicmaker_three],
        [(44, 4), (45, 4), baritone_three_musicmaker_one],
        [(45, 4), (46, 4), baritone_three_musicmaker_one],
        [(46, 4), (47, 4), baritone_three_musicmaker_one],
        [(49, 4), (50, 4), baritone_three_musicmaker_two],

        [(56, 4), (57, 4), baritone_three_musicmaker_one],
        [(63, 4), (64, 4), baritone_three_musicmaker_one],
        [(64, 4), (65, 4), baritone_three_musicmaker_one],
        [(65, 4), (66, 4), baritone_three_musicmaker_two],
        [(66, 4), (67, 4), baritone_three_musicmaker_two],
        [(67, 4), (68, 4), baritone_three_musicmaker_two],
        [(72, 4), (73, 4), baritone_three_musicmaker_two],
        [(73, 4), (74, 4), baritone_three_musicmaker_two],
        [(74, 4), (75, 4), baritone_three_musicmaker_two],
        [(77, 4), (78, 4), baritone_three_musicmaker_three],
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
        [(0, 4), (1, 4), bass_one_musicmaker_two],
        [(1, 4), (2, 4), bass_one_musicmaker_two],
        [(2, 4), (3, 4), bass_one_musicmaker_two],
        [(3, 4), (4, 4), bass_one_musicmaker_two],
        [(4, 4), (5, 4), bass_one_musicmaker_two],
        [(5, 4), (6, 4), bass_one_musicmaker_one],
        [(11, 4), (12, 4), bass_one_musicmaker_two],
        [(12, 4), (13, 4), bass_one_musicmaker_two],
        [(13, 4), (14, 4), bass_one_musicmaker_two],
        [(14, 4), (15, 4), bass_one_musicmaker_two],
        [(18, 4), (19, 4), bass_one_musicmaker_one],
        [(19, 4), (20, 4), bass_one_musicmaker_two],
        [(21, 4), (22, 4), bass_one_musicmaker_one],
        [(22, 4), (23, 4), bass_one_musicmaker_one],
        [(23, 4), (24, 4), bass_one_musicmaker_one],
        [(24, 4), (25, 4), bass_one_musicmaker_one],
        [(25, 4), (26, 4), bass_one_musicmaker_one],
        [(26, 4), (27, 4), bass_one_musicmaker_one],

        [(28, 4), (29, 4), bass_one_musicmaker_one],
        [(29, 4), (30, 4), bass_one_musicmaker_one],
        [(30, 4), (31, 4), bass_one_musicmaker_one],
        [(31, 4), (32, 4), bass_one_musicmaker_one],
        [(32, 4), (33, 4), bass_one_musicmaker_one],
        [(33, 4), (34, 4), bass_one_musicmaker_two],
        [(39, 4), (40, 4), bass_one_musicmaker_three],
        [(40, 4), (41, 4), bass_one_musicmaker_one],
        [(41, 4), (42, 4), bass_one_musicmaker_one],
        [(42, 4), (43, 4), bass_one_musicmaker_one],
        [(46, 4), (47, 4), bass_one_musicmaker_two],
        [(47, 4), (48, 4), bass_one_musicmaker_three],
        [(49, 4), (50, 4), bass_one_musicmaker_one],
        [(50, 4), (51, 4), bass_one_musicmaker_one],
        [(51, 4), (52, 4), bass_one_musicmaker_two],
        [(52, 4), (53, 4), bass_one_musicmaker_two],
        [(53, 4), (54, 4), bass_one_musicmaker_two],
        [(54, 4), (55, 4), bass_one_musicmaker_two],

        [(56, 4), (57, 4), bass_one_musicmaker_one],
        [(57, 4), (58, 4), bass_one_musicmaker_one],
        [(58, 4), (59, 4), bass_one_musicmaker_one],
        [(59, 4), (60, 4), bass_one_musicmaker_one],
        [(60, 4), (61, 4), bass_one_musicmaker_one],
        [(61, 4), (62, 4), bass_one_musicmaker_one],
        [(67, 4), (68, 4), bass_one_musicmaker_two],
        [(68, 4), (69, 4), bass_one_musicmaker_two],
        [(69, 4), (70, 4), bass_one_musicmaker_two],
        [(70, 4), (71, 4), bass_one_musicmaker_two],
        [(74, 4), (75, 4), bass_one_musicmaker_three],
        [(75, 4), (76, 4), bass_one_musicmaker_three],
        [(77, 4), (78, 4), bass_one_musicmaker_one],
        [(78, 4), (79, 4), bass_one_musicmaker_one],
        [(79, 4), (80, 4), bass_one_musicmaker_two],
        [(80, 4), (81, 4), bass_one_musicmaker_two],
        [(81, 4), (82, 4), bass_one_musicmaker_two],
        [(82, 4), (83, 4), bass_one_musicmaker_two],
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
        [(0, 4), (1, 4), bass_two_musicmaker_one],
        [(1, 4), (2, 4), bass_two_musicmaker_one],
        [(2, 4), (3, 4), bass_two_musicmaker_one],
        [(3, 4), (4, 4), bass_two_musicmaker_one],
        [(4, 4), (5, 4), bass_two_musicmaker_one],
        [(9, 4), (10, 4), bass_two_musicmaker_two],
        [(10, 4), (11, 4), bass_two_musicmaker_two],
        [(11, 4), (12, 4), bass_two_musicmaker_two],
        [(14, 4), (15, 4), bass_two_musicmaker_one],
        [(21, 4), (22, 4), bass_two_musicmaker_two],
        [(22, 4), (23, 4), bass_two_musicmaker_two],
        [(23, 4), (24, 4), bass_two_musicmaker_two],
        [(24, 4), (25, 4), bass_two_musicmaker_two],
        [(25, 4), (26, 4), bass_two_musicmaker_two],

        [(28, 4), (29, 4), bass_two_musicmaker_one],
        [(29, 4), (30, 4), bass_two_musicmaker_one],
        [(30, 4), (31, 4), bass_two_musicmaker_one],
        [(31, 4), (32, 4), bass_two_musicmaker_one],
        [(32, 4), (33, 4), bass_two_musicmaker_one],
        [(37, 4), (38, 4), bass_two_musicmaker_two],
        [(38, 4), (39, 4), bass_two_musicmaker_two],
        [(39, 4), (40, 4), bass_two_musicmaker_two],
        [(42, 4), (43, 4), bass_two_musicmaker_three],
        [(49, 4), (50, 4), bass_two_musicmaker_one],
        [(50, 4), (51, 4), bass_two_musicmaker_one],
        [(51, 4), (52, 4), bass_two_musicmaker_two],
        [(52, 4), (53, 4), bass_two_musicmaker_two],
        [(53, 4), (54, 4), bass_two_musicmaker_two],

        [(56, 4), (57, 4), bass_two_musicmaker_one],
        [(57, 4), (58, 4), bass_two_musicmaker_one],
        [(58, 4), (59, 4), bass_two_musicmaker_one],
        [(59, 4), (60, 4), bass_two_musicmaker_one],
        [(60, 4), (61, 4), bass_two_musicmaker_one],
        [(65, 4), (66, 4), bass_two_musicmaker_one],
        [(66, 4), (67, 4), bass_two_musicmaker_one],
        [(67, 4), (68, 4), bass_two_musicmaker_one],
        [(70, 4), (71, 4), bass_two_musicmaker_two],
        [(77, 4), (78, 4), bass_two_musicmaker_two],
        [(78, 4), (79, 4), bass_two_musicmaker_two],
        [(79, 4), (80, 4), bass_two_musicmaker_three],
        [(80, 4), (81, 4), bass_two_musicmaker_three],
        [(81, 4), (82, 4), bass_two_musicmaker_three],
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
        [(0, 4), (1, 4), contrabass_musicmaker_two],
        [(1, 4), (2, 4), contrabass_musicmaker_two],
        [(2, 4), (3, 4), contrabass_musicmaker_two],
        [(3, 4), (4, 4), contrabass_musicmaker_two],
        [(6, 4), (7, 4), contrabass_musicmaker_one],
        [(7, 4), (8, 4), contrabass_musicmaker_one],
        [(10, 4), (11, 4), contrabass_musicmaker_two],
        [(11, 4), (12, 4), contrabass_musicmaker_two],
        [(12, 4), (13, 4), contrabass_musicmaker_two],
        [(13, 4), (14, 4), contrabass_musicmaker_two],
        [(14, 4), (15, 4), contrabass_musicmaker_two],
        [(15, 4), (16, 4), contrabass_musicmaker_two],
        [(20, 4), (21, 4), contrabass_musicmaker_one],
        [(21, 4), (22, 4), contrabass_musicmaker_one],
        [(23, 4), (24, 4), contrabass_musicmaker_two],
        [(24, 4), (25, 4), contrabass_musicmaker_two],

        [(28, 4), (29, 4), contrabass_musicmaker_one],
        [(29, 4), (30, 4), contrabass_musicmaker_one],
        [(30, 4), (31, 4), contrabass_musicmaker_one],
        [(31, 4), (32, 4), contrabass_musicmaker_one],
        [(35, 4), (36, 4), contrabass_musicmaker_two],
        [(36, 4), (37, 4), contrabass_musicmaker_two],
        [(38, 4), (39, 4), contrabass_musicmaker_three],
        [(39, 4), (40, 4), contrabass_musicmaker_three],
        [(40, 4), (41, 4), contrabass_musicmaker_one],
        [(41, 4), (42, 4), contrabass_musicmaker_one],
        [(42, 4), (43, 4), contrabass_musicmaker_one],
        [(43, 4), (44, 4), contrabass_musicmaker_one],
        [(48, 4), (49, 4), contrabass_musicmaker_two],
        [(49, 4), (50, 4), contrabass_musicmaker_two],
        [(51, 4), (52, 4), contrabass_musicmaker_three],
        [(52, 4), (53, 4), contrabass_musicmaker_three],

        [(56, 4), (57, 4), contrabass_musicmaker_one],
        [(57, 4), (58, 4), contrabass_musicmaker_one],
        [(58, 4), (59, 4), contrabass_musicmaker_one],
        [(59, 4), (60, 4), contrabass_musicmaker_one],
        [(62, 4), (63, 4), contrabass_musicmaker_one],
        [(63, 4), (64, 4), contrabass_musicmaker_one],
        [(66, 4), (67, 4), contrabass_musicmaker_two],
        [(67, 4), (68, 4), contrabass_musicmaker_two],
        [(68, 4), (69, 4), contrabass_musicmaker_two],
        [(69, 4), (70, 4), contrabass_musicmaker_two],
        [(70, 4), (71, 4), contrabass_musicmaker_two],
        [(71, 4), (72, 4), contrabass_musicmaker_two],
        [(76, 4), (77, 4), contrabass_musicmaker_three],
        [(77, 4), (78, 4), contrabass_musicmaker_three],
        [(78, 4), (79, 4), contrabass_musicmaker_three],
        [(79, 4), (80, 4), contrabass_musicmaker_three],
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
