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
        (5, 4), (4, 4), (3, 4), (5, 4), (4, 4), (3, 4),
        (3, 4), (4, 4), (5, 4), (3, 4), (4, 4), (9, 8),
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

sopranino_notes = [14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5, 25, 25.5]
soprano_1_notes = [15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5, 25, 25.5, 26, 26.5]
soprano_2_notes = [11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23]
soprano_3_notes = [11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5]
alto_1_notes = [14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5, 25, 25.5]
alto_2_notes = [10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5]
alto_3_notes = [6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5]
alto_4_notes = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13]
alto_5_notes = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5]
alto_6_notes = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5]
tenor_1_notes = [7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5]
tenor_2_notes = [3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5]
tenor_3_notes = [-1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5]
tenor_4_notes = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12]
tenor_5_notes = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5]
baritone_1_notes = [2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5]
baritone_2_notes = [-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5]
baritone_3_notes = [-1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]
bass_1_notes = [-0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11]
bass_2_notes = [-1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5]
contrabass_notes = [6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5]

# Define rhythm-makers: two to be sued by the MusicMaker, one for silence.

rmaker_one = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(
        counts=[1, 1, 1, 5, 3, 2, 4],
        denominator=16,
        ),
    beam_specifier=abjadext.rmakers.BeamSpecifier(
        beam_divisions_together=True,
        beam_rests=False,
        ),
    extra_counts_per_division=[0, 1, -1, ],
    # burnish_specifier=abjadext.rmakers.BurnishSpecifier(
    #     left_classes=[abjad.Rest, abjad.Note],
    #     right_classes=[abjad.Rest, abjad.Note],
    #     left_counts=[1, 0, 1],
    #     right_counts=[1, 0],
    #     ),
    tuplet_specifier=abjadext.rmakers.TupletSpecifier(
        trivialize=True,
        extract_trivial=True,
        rewrite_rest_filled=True,
        rewrite_sustained=True,
        ),
    )

rmaker_two = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(
        counts=[4, 3, -1, 2],
        denominator=8,
        ),
    beam_specifier=abjadext.rmakers.BeamSpecifier(
        beam_divisions_together=True,
        beam_rests=False,
        ),
    extra_counts_per_division=[-1, 0, -1, 1, 0, ],
    # burnish_specifier=abjadext.rmakers.BurnishSpecifier(
    #     left_classes=[abjad.Rest, abjad.Note],
    #     right_classes=[abjad.Rest, abjad.Note],
    #     left_counts=[1, 0, 0, 1],
    #     right_counts=[1, 0],
    #     ),
    tuplet_specifier=abjadext.rmakers.TupletSpecifier(
        trivialize=True,
        extract_trivial=True,
        rewrite_rest_filled=True,
        rewrite_sustained=True,
        ),
    )

# Initialize AttachmentHandler

attachment_handler_one = AttachmentHandler(
    starting_dynamic='mp',
    ending_dynamic='ff',
    hairpin='<|',
    # articulation_list=['tenuto'],
)

attachment_handler_two = AttachmentHandler(
    starting_dynamic='mf',
    ending_dynamic='f',
    hairpin='<',
    articulation_list=['tenuto', '', '', '', '', ],
)

# Initialize MusicMakers with the rhythm-makers.
#####sopranino#####
sopranino_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=sopranino_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
sopranino_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=sopranino_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####soprano_one#####
soprano_one_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=soprano_1_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
soprano_one_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_1_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####soprano_two#####
soprano_two_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=soprano_2_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
soprano_two_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_2_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####soprano_three#####
soprano_three_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=soprano_3_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
soprano_three_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=soprano_3_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####alto_one#####
alto_one_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_1_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_one_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_1_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####alto_two#####
alto_two_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_2_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_two_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_2_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####alto_three#####
alto_three_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_3_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_three_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_3_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####alto_four#####
alto_four_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_4_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_four_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_4_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####alto_five#####
alto_five_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_5_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_five_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_5_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####alto_six#####
alto_six_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=alto_6_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
alto_six_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=alto_6_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####tenor_one#####
tenor_one_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=tenor_1_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
tenor_one_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_1_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####tenor_two#####
tenor_two_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=tenor_2_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
tenor_two_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_2_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####tenor_three#####
tenor_three_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=tenor_3_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
tenor_three_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_3_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####tenor_four#####
tenor_four_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=tenor_4_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
tenor_four_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_4_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####tenor_five#####
tenor_five_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=tenor_5_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
tenor_five_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=tenor_5_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####baritone_one#####
baritone_one_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=baritone_1_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
baritone_one_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=baritone_1_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####baritone_two#####
baritone_two_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=baritone_2_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
baritone_two_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=baritone_2_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####baritone_three#####
baritone_three_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=baritone_3_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
baritone_three_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=baritone_3_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####bass_one#####
bass_one_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=bass_1_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
bass_one_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=bass_1_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####bass_two#####
bass_two_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=bass_2_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
bass_two_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=bass_2_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
)
#####contrabass#####
contrabass_musicmaker_one = MusicMaker(
    rmaker=rmaker_one,
    pitches=contrabass_notes,
    continuous=True,
    attachment_handler=attachment_handler_one,
)
contrabass_musicmaker_two = MusicMaker(
    rmaker=rmaker_two,
    pitches=contrabass_notes,
    continuous=True,
    attachment_handler=attachment_handler_two,
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
        [(0, 4), (2, 4), sopranino_musicmaker_one],
        [(2, 4), (3, 4), sopranino_musicmaker_one],
        [(5, 4), (7, 4), sopranino_musicmaker_one],
        [(7, 4), (8, 4), sopranino_musicmaker_one],
        [(12, 4), (14, 4), sopranino_musicmaker_two],
        [(14, 4), (15, 4), sopranino_musicmaker_two],
        [(17, 4), (18, 4), sopranino_musicmaker_one],
        [(18, 4), (20, 4), sopranino_musicmaker_one],
        [(28, 4), (31, 4), sopranino_musicmaker_two],
        [(33, 4), (35, 4), sopranino_musicmaker_two],
        [(35, 4), (36, 4), sopranino_musicmaker_two],
        [(40, 4), (42, 4), sopranino_musicmaker_one],
        [(42, 4), (43, 4), sopranino_musicmaker_one],
        [(45, 4), (46, 4), sopranino_musicmaker_two],
        [(46, 4), (47, 4), sopranino_musicmaker_two],
        [(47, 4), (95, 8), sopranino_musicmaker_two],
        # [(95, 8), (96, 8), silence_maker],
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
        [(4, 4), (5, 4), soprano_one_musicmaker_two],
        [(5, 4), (6, 4), soprano_one_musicmaker_two],
        [(6, 4), (7, 4), soprano_one_musicmaker_two],
        [(9, 4), (10, 4), soprano_one_musicmaker_one],
        [(10, 4), (12, 4), soprano_one_musicmaker_one],
        [(16, 4), (17, 4), soprano_one_musicmaker_two],
        [(17, 4), (18, 4), soprano_one_musicmaker_two],
        [(18, 4), (19, 4), soprano_one_musicmaker_two],
        [(21, 4), (23, 4), soprano_one_musicmaker_one],
        [(23, 4), (24, 4), soprano_one_musicmaker_one],
        [(24, 4), (25, 4), soprano_one_musicmaker_one],
        [(25, 4), (27, 4), soprano_one_musicmaker_one],
        [(29, 4), (30, 4), soprano_one_musicmaker_two],
        [(30, 4), (31, 4), soprano_one_musicmaker_two],
        [(31, 4), (32, 4), soprano_one_musicmaker_two],
        [(36, 4), (37, 4), soprano_one_musicmaker_one],
        [(37, 4), (38, 4), soprano_one_musicmaker_one],
        [(38, 4), (39, 4), soprano_one_musicmaker_one],
        [(41, 4), (42, 4), soprano_one_musicmaker_two],
        [(42, 4), (43, 4), soprano_one_musicmaker_two],
        [(43, 4), (87, 8), soprano_one_musicmaker_two],
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
        [(2, 4), (4, 4), soprano_two_musicmaker_one],
        [(4, 4), (5, 4), soprano_two_musicmaker_one],
        [(9, 4), (10, 4), soprano_two_musicmaker_two],
        [(10, 4), (11, 4), soprano_two_musicmaker_two],
        [(11, 4), (12, 4), soprano_two_musicmaker_two],
        [(14, 4), (15, 4), soprano_two_musicmaker_two],
        [(15, 4), (17, 4), soprano_two_musicmaker_two],
        [(21, 4), (22, 4), soprano_two_musicmaker_one],
        [(22, 4), (24, 4), soprano_two_musicmaker_one],
        [(24, 4), (25, 4), soprano_two_musicmaker_two],
        [(25, 4), (26, 4), soprano_two_musicmaker_two],
        [(26, 4), (27, 4), soprano_two_musicmaker_two],
        [(31, 4), (33, 4), soprano_two_musicmaker_one],
        [(33, 4), (34, 4), soprano_two_musicmaker_one],
        [(36, 4), (37, 4), soprano_two_musicmaker_one],
        [(37, 4), (39, 4), soprano_two_musicmaker_one],
        [(43, 4), (44, 4), soprano_two_musicmaker_two],
        [(44, 4), (45, 4), soprano_two_musicmaker_two],
        [(45, 4), (91, 8), soprano_two_musicmaker_two],
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
        [(1, 8), (1, 4), soprano_three_musicmaker_two],
        [(1, 4), (2, 4), soprano_three_musicmaker_two],
        [(2, 4), (3, 4), soprano_three_musicmaker_two],
        [(7, 4), (8, 4), soprano_three_musicmaker_two],
        [(8, 4), (9, 4), soprano_three_musicmaker_two],
        [(9, 4), (10, 4), soprano_three_musicmaker_two],
        [(25, 8), (13, 4), soprano_three_musicmaker_one],
        [(13, 4), (14, 4), soprano_three_musicmaker_one],
        [(14, 4), (15, 4), soprano_three_musicmaker_one],
        [(19, 4), (20, 4), soprano_three_musicmaker_two],
        [(20, 4), (21, 4), soprano_three_musicmaker_two],
        [(21, 4), (22, 4), soprano_three_musicmaker_two],
        [(26, 4), (27, 4), soprano_three_musicmaker_one],
        [(27, 4), (28, 4), soprano_three_musicmaker_one],
        [(28, 4), (29, 4), soprano_three_musicmaker_one],
        [(33, 4), (34, 4), soprano_three_musicmaker_one],
        [(34, 4), (35, 4), soprano_three_musicmaker_one],
        [(35, 4), (36, 4), soprano_three_musicmaker_one],
        [(38, 4), (39, 4), soprano_three_musicmaker_two],
        [(39, 4), (40, 4), soprano_three_musicmaker_two],
        [(40, 4), (41, 4), soprano_three_musicmaker_two],
        [(45, 4), (46, 4), soprano_three_musicmaker_one],
        [(46, 4), (47, 4), soprano_three_musicmaker_one],
        [(47, 4), (95, 8), soprano_three_musicmaker_one],
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
        [(0, 4), (1, 4), alto_one_musicmaker_one],
        [(1, 4), (2, 4), alto_one_musicmaker_one],
        [(2, 4), (3, 4), alto_one_musicmaker_one],
        [(5, 4), (6, 4), alto_one_musicmaker_one],
        [(6, 4), (7, 4), alto_one_musicmaker_one],
        [(7, 4), (8, 4), alto_one_musicmaker_one],
        [(12, 4), (13, 4), alto_one_musicmaker_two],
        [(13, 4), (14, 4), alto_one_musicmaker_two],
        [(14, 4), (15, 4), alto_one_musicmaker_two],
        [(17, 4), (18, 4), alto_one_musicmaker_one],
        [(18, 4), (19, 4), alto_one_musicmaker_one],
        [(19, 4), (20, 4), alto_one_musicmaker_one],
        [(28, 4), (29, 4), alto_one_musicmaker_two],
        [(29, 4), (30, 4), alto_one_musicmaker_two],
        [(30, 4), (31, 4), alto_one_musicmaker_two],
        [(33, 4), (34, 4), alto_one_musicmaker_two],
        [(34, 4), (35, 4), alto_one_musicmaker_two],
        [(35, 4), (36, 4), alto_one_musicmaker_two],
        [(40, 4), (41, 4), alto_one_musicmaker_one],
        [(41, 4), (42, 4), alto_one_musicmaker_one],
        [(42, 4), (43, 4), alto_one_musicmaker_one],
        [(45, 4), (46, 4), alto_one_musicmaker_two],
        [(46, 4), (47, 4), alto_one_musicmaker_two],
        [(47, 4), (95, 8), alto_one_musicmaker_two],
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
        [(4, 4), (5, 4), alto_two_musicmaker_two],
        [(5, 4), (6, 4), alto_two_musicmaker_two],
        [(6, 4), (7, 4), alto_two_musicmaker_two],
        [(9, 4), (10, 4), alto_two_musicmaker_one],
        [(10, 4), (11, 4), alto_two_musicmaker_one],
        [(11, 4), (12, 4), alto_two_musicmaker_one],
        [(16, 4), (17, 4), alto_two_musicmaker_two],
        [(17, 4), (18, 4), alto_two_musicmaker_two],
        [(18, 4), (19, 4), alto_two_musicmaker_two],
        [(21, 4), (22, 4), alto_two_musicmaker_one],
        [(22, 4), (23, 4), alto_two_musicmaker_one],
        [(23, 4), (24, 4), alto_two_musicmaker_one],
        [(24, 4), (25, 4), alto_two_musicmaker_one],
        [(25, 4), (26, 4), alto_two_musicmaker_one],
        [(26, 4), (27, 4), alto_two_musicmaker_one],
        [(29, 4), (30, 4), alto_two_musicmaker_two],
        [(30, 4), (31, 4), alto_two_musicmaker_two],
        [(31, 4), (32, 4), alto_two_musicmaker_two],
        [(36, 4), (37, 4), alto_two_musicmaker_one],
        [(37, 4), (38, 4), alto_two_musicmaker_one],
        [(38, 4), (39, 4), alto_two_musicmaker_one],
        [(41, 4), (42, 4), alto_two_musicmaker_two],
        [(42, 4), (43, 4), alto_two_musicmaker_two],
        [(43, 4), (87, 8), alto_two_musicmaker_two],
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
        [(2, 4), (3, 4), alto_three_musicmaker_one],
        [(3, 4), (4, 4), alto_three_musicmaker_one],
        [(4, 4), (5, 4), alto_three_musicmaker_one],
        [(9, 4), (10, 4), alto_three_musicmaker_two],
        [(10, 4), (11, 4), alto_three_musicmaker_two],
        [(11, 4), (12, 4), alto_three_musicmaker_two],
        [(14, 4), (15, 4), alto_three_musicmaker_two],
        [(15, 4), (16, 4), alto_three_musicmaker_two],
        [(16, 4), (17, 4), alto_three_musicmaker_two],
        [(21, 4), (22, 4), alto_three_musicmaker_one],
        [(22, 4), (23, 4), alto_three_musicmaker_one],
        [(23, 4), (24, 4), alto_three_musicmaker_one],
        [(24, 4), (25, 4), alto_three_musicmaker_two],
        [(25, 4), (26, 4), alto_three_musicmaker_two],
        [(26, 4), (27, 4), alto_three_musicmaker_two],
        [(31, 4), (32, 4), alto_three_musicmaker_one],
        [(32, 4), (33, 4), alto_three_musicmaker_one],
        [(33, 4), (34, 4), alto_three_musicmaker_one],
        [(36, 4), (37, 4), alto_three_musicmaker_one],
        [(37, 4), (38, 4), alto_three_musicmaker_one],
        [(38, 4), (39, 4), alto_three_musicmaker_one],
        [(43, 4), (44, 4), alto_three_musicmaker_two],
        [(44, 4), (45, 4), alto_three_musicmaker_two],
        [(45, 4), (91, 8), alto_three_musicmaker_two],
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
        [(1, 8), (3, 4), alto_four_musicmaker_two],
        [(7, 4), (9, 4), alto_four_musicmaker_two],
        [(9, 4), (10, 4), alto_four_musicmaker_two],
        [(25, 8), (13, 4), alto_four_musicmaker_one],
        [(13, 4), (14, 4), alto_four_musicmaker_one],
        [(14, 4), (15, 4), alto_four_musicmaker_one],
        [(19, 4), (20, 4), alto_four_musicmaker_two],
        [(20, 4), (21, 4), alto_four_musicmaker_two],
        [(21, 4), (22, 4), alto_four_musicmaker_two],
        [(26, 4), (27, 4), alto_four_musicmaker_one],
        [(27, 4), (28, 4), alto_four_musicmaker_one],
        [(28, 4), (29, 4), alto_four_musicmaker_one],
        [(33, 4), (34, 4), alto_four_musicmaker_one],
        [(34, 4), (35, 4), alto_four_musicmaker_one],
        [(35, 4), (36, 4), alto_four_musicmaker_one],
        [(38, 4), (39, 4), alto_four_musicmaker_two],
        [(39, 4), (40, 4), alto_four_musicmaker_two],
        [(40, 4), (41, 4), alto_four_musicmaker_two],
        [(45, 4), (46, 4), alto_four_musicmaker_one],
        [(46, 4), (47, 4), alto_four_musicmaker_one],
        [(47, 4), (95, 8), alto_four_musicmaker_one],
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
        [(1, 4), (3, 4), alto_five_musicmaker_one],
        [(5, 4), (7, 4), alto_five_musicmaker_one],
        [(7, 4), (8, 4), alto_five_musicmaker_one],
        [(12, 4), (13, 4), alto_five_musicmaker_two],
        [(13, 4), (15, 4), alto_five_musicmaker_two],
        [(17, 4), (19, 4), alto_five_musicmaker_one],
        [(19, 4), (20, 4), alto_five_musicmaker_one],
        [(28, 4), (29, 4), alto_five_musicmaker_two],
        [(29, 4), (31, 4), alto_five_musicmaker_two],
        [(33, 4), (35, 4), alto_five_musicmaker_two],
        [(35, 4), (36, 4), alto_five_musicmaker_two],
        [(40, 4), (41, 4), alto_five_musicmaker_one],
        [(41, 4), (42, 4), alto_five_musicmaker_one],
        [(42, 4), (43, 4), alto_five_musicmaker_one],
        [(45, 4), (46, 4), alto_five_musicmaker_two],
        [(46, 4), (47, 4), alto_five_musicmaker_two],
        [(47, 4), (95, 8), alto_five_musicmaker_two],
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
        [(4, 4), (5, 4), alto_six_musicmaker_two],
        [(5, 4), (7, 4), alto_six_musicmaker_two],
        [(9, 4), (11, 4), alto_six_musicmaker_one],
        [(11, 4), (12, 4), alto_six_musicmaker_one],
        [(16, 4), (17, 4), alto_six_musicmaker_two],
        [(17, 4), (19, 4), alto_six_musicmaker_two],
        [(21, 4), (23, 4), alto_six_musicmaker_one],
        [(23, 4), (24, 4), alto_six_musicmaker_one],
        [(24, 4), (26, 4), alto_six_musicmaker_one],
        [(26, 4), (27, 4), alto_six_musicmaker_one],
        [(29, 4), (31, 4), alto_six_musicmaker_two],
        [(31, 4), (32, 4), alto_six_musicmaker_two],
        [(36, 4), (38, 4), alto_six_musicmaker_one],
        [(38, 4), (39, 4), alto_six_musicmaker_one],
        [(41, 4), (42, 4), alto_six_musicmaker_two],
        [(42, 4), (43, 4), alto_six_musicmaker_two],
        [(43, 4), (87, 8), alto_six_musicmaker_two],
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
        [(2, 4), (4, 4), tenor_one_musicmaker_one],
        [(4, 4), (5, 4), tenor_one_musicmaker_one],
        [(9, 4), (10, 4), tenor_one_musicmaker_two],
        [(10, 4), (12, 4), tenor_one_musicmaker_two],
        [(14, 4), (16, 4), tenor_one_musicmaker_two],
        [(16, 4), (17, 4), tenor_one_musicmaker_two],
        [(21, 4), (22, 4), tenor_one_musicmaker_one],
        [(22, 4), (24, 4), tenor_one_musicmaker_one],
        [(24, 4), (25, 4), tenor_one_musicmaker_two],
        [(25, 4), (26, 4), tenor_one_musicmaker_two],
        [(26, 4), (27, 4), tenor_one_musicmaker_two],
        [(31, 4), (33, 4), tenor_one_musicmaker_one],
        [(33, 4), (34, 4), tenor_one_musicmaker_one],
        [(36, 4), (37, 4), tenor_one_musicmaker_one],
        [(37, 4), (39, 4), tenor_one_musicmaker_one],
        [(43, 4), (45, 4), tenor_one_musicmaker_two],
        [(45, 4), (91, 8), tenor_one_musicmaker_two],
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
        [(1, 8), (2, 4), tenor_two_musicmaker_two],
        [(2, 4), (3, 4), tenor_two_musicmaker_two],
        [(7, 4), (8, 4), tenor_two_musicmaker_two],
        [(8, 4), (9, 4), tenor_two_musicmaker_two],
        [(9, 4), (10, 4), tenor_two_musicmaker_two],
        [(25, 8), (14, 4), tenor_two_musicmaker_one],
        [(14, 4), (15, 4), tenor_two_musicmaker_one],
        [(19, 4), (20, 4), tenor_two_musicmaker_two],
        [(20, 4), (21, 4), tenor_two_musicmaker_two],
        [(21, 4), (22, 4), tenor_two_musicmaker_two],
        [(26, 4), (27, 4), tenor_two_musicmaker_one],
        [(27, 4), (28, 4), tenor_two_musicmaker_one],
        [(28, 4), (29, 4), tenor_two_musicmaker_one],
        [(33, 4), (34, 4), tenor_two_musicmaker_one],
        [(34, 4), (36, 4), tenor_two_musicmaker_one],
        [(38, 4), (39, 4), tenor_two_musicmaker_two],
        [(39, 4), (40, 4), tenor_two_musicmaker_two],
        [(40, 4), (41, 4), tenor_two_musicmaker_two],
        [(45, 4), (47, 4), tenor_two_musicmaker_one],
        [(47, 4), (95, 8), tenor_two_musicmaker_one],
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
        [(0, 4), (1, 4), tenor_three_musicmaker_one],
        [(1, 4), (3, 4), tenor_three_musicmaker_one],
        [(5, 4), (7, 4), tenor_three_musicmaker_one],
        [(7, 4), (8, 4), tenor_three_musicmaker_one],
        [(12, 4), (13, 4), tenor_three_musicmaker_two],
        [(13, 4), (15, 4), tenor_three_musicmaker_two],
        [(17, 4), (19, 4), tenor_three_musicmaker_one],
        [(19, 4), (20, 4), tenor_three_musicmaker_one],
        [(28, 4), (29, 4), tenor_three_musicmaker_two],
        [(29, 4), (31, 4), tenor_three_musicmaker_two],
        [(33, 4), (35, 4), tenor_three_musicmaker_two],
        [(35, 4), (36, 4), tenor_three_musicmaker_two],
        [(40, 4), (41, 4), tenor_three_musicmaker_one],
        [(41, 4), (43, 4), tenor_three_musicmaker_one],
        [(45, 4), (46, 4), tenor_three_musicmaker_two],
        [(46, 4), (47, 4), tenor_three_musicmaker_two],
        [(47, 4), (95, 8), tenor_three_musicmaker_two],
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
        [(4, 4), (5, 4), tenor_four_musicmaker_two],
        [(5, 4), (6, 4), tenor_four_musicmaker_two],
        [(6, 4), (7, 4), tenor_four_musicmaker_two],
        [(9, 4), (10, 4), tenor_four_musicmaker_one],
        [(10, 4), (11, 4), tenor_four_musicmaker_one],
        [(11, 4), (12, 4), tenor_four_musicmaker_one],
        [(16, 4), (17, 4), tenor_four_musicmaker_two],
        [(17, 4), (18, 4), tenor_four_musicmaker_two],
        [(18, 4), (19, 4), tenor_four_musicmaker_two],
        [(21, 4), (22, 4), tenor_four_musicmaker_one],
        [(22, 4), (24, 4), tenor_four_musicmaker_one],
        [(24, 4), (26, 4), tenor_four_musicmaker_one],
        [(26, 4), (27, 4), tenor_four_musicmaker_one],
        [(29, 4), (30, 4), tenor_four_musicmaker_two],
        [(30, 4), (31, 4), tenor_four_musicmaker_two],
        [(31, 4), (32, 4), tenor_four_musicmaker_two],
        [(36, 4), (38, 4), tenor_four_musicmaker_one],
        [(38, 4), (39, 4), tenor_four_musicmaker_one],
        [(41, 4), (42, 4), tenor_four_musicmaker_two],
        [(42, 4), (43, 4), tenor_four_musicmaker_two],
        [(43, 4), (87, 8), tenor_four_musicmaker_two],
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
        [(2, 4), (3, 4), tenor_five_musicmaker_one],
        [(3, 4), (5, 4), tenor_five_musicmaker_one],
        [(9, 4), (11, 4), tenor_five_musicmaker_two],
        [(11, 4), (12, 4), tenor_five_musicmaker_two],
        [(14, 4), (15, 4), tenor_five_musicmaker_two],
        [(15, 4), (17, 4), tenor_five_musicmaker_two],
        [(21, 4), (23, 4), tenor_five_musicmaker_one],
        [(23, 4), (24, 4), tenor_five_musicmaker_one],
        [(24, 4), (26, 4), tenor_five_musicmaker_two],
        [(26, 4), (27, 4), tenor_five_musicmaker_two],
        [(31, 4), (32, 4), tenor_five_musicmaker_one],
        [(32, 4), (34, 4), tenor_five_musicmaker_one],
        [(36, 4), (38, 4), tenor_five_musicmaker_one],
        [(38, 4), (39, 4), tenor_five_musicmaker_one],
        [(43, 4), (44, 4), tenor_five_musicmaker_two],
        [(44, 4), (45, 4), tenor_five_musicmaker_two],
        [(45, 4), (91, 8), tenor_five_musicmaker_two],
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
        [(1, 8), (2, 4), baritone_one_musicmaker_two],
        [(2, 4), (3, 4), baritone_one_musicmaker_two],
        [(7, 4), (8, 4), baritone_one_musicmaker_two],
        [(8, 4), (9, 4), baritone_one_musicmaker_two],
        [(9, 4), (10, 4), baritone_one_musicmaker_two],
        [(25, 8), (13, 4), baritone_one_musicmaker_one],
        [(13, 4), (15, 4), baritone_one_musicmaker_one],
        [(19, 4), (21, 4), baritone_one_musicmaker_two],
        [(21, 4), (22, 4), baritone_one_musicmaker_two],
        [(26, 4), (27, 4), baritone_one_musicmaker_one],
        [(27, 4), (29, 4), baritone_one_musicmaker_one],
        [(33, 4), (35, 4), baritone_one_musicmaker_one],
        [(35, 4), (36, 4), baritone_one_musicmaker_one],
        [(38, 4), (39, 4), baritone_one_musicmaker_two],
        [(39, 4), (41, 4), baritone_one_musicmaker_two],
        [(45, 4), (46, 4), baritone_one_musicmaker_one],
        [(46, 4), (47, 4), baritone_one_musicmaker_one],
        [(47, 4), (95, 8), baritone_one_musicmaker_one],
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
        [(2, 4), (3, 4), baritone_two_musicmaker_one],
        [(5, 4), (6, 4), baritone_two_musicmaker_one],
        [(6, 4), (8, 4), baritone_two_musicmaker_one],
        [(12, 4), (14, 4), baritone_two_musicmaker_two],
        [(14, 4), (15, 4), baritone_two_musicmaker_two],
        [(17, 4), (18, 4), baritone_two_musicmaker_one],
        [(18, 4), (20, 4), baritone_two_musicmaker_one],
        [(28, 4), (30, 4), baritone_two_musicmaker_two],
        [(30, 4), (31, 4), baritone_two_musicmaker_two],
        [(33, 4), (34, 4), baritone_two_musicmaker_two],
        [(34, 4), (36, 4), baritone_two_musicmaker_two],
        [(40, 4), (42, 4), baritone_two_musicmaker_one],
        [(42, 4), (43, 4), baritone_two_musicmaker_one],
        [(45, 4), (47, 4), baritone_two_musicmaker_two],
        [(47, 4), (95, 8), baritone_two_musicmaker_two],
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
        [(4, 4), (5, 4), baritone_three_musicmaker_two],
        [(5, 4), (7, 4), baritone_three_musicmaker_two],
        [(9, 4), (11, 4), baritone_three_musicmaker_one],
        [(11, 4), (12, 4), baritone_three_musicmaker_one],
        [(16, 4), (17, 4), baritone_three_musicmaker_two],
        [(17, 4), (19, 4), baritone_three_musicmaker_two],
        [(21, 4), (23, 4), baritone_three_musicmaker_one],
        [(23, 4), (24, 4), baritone_three_musicmaker_one],
        [(24, 4), (25, 4), baritone_three_musicmaker_one],
        [(25, 4), (27, 4), baritone_three_musicmaker_one],
        [(29, 4), (31, 4), baritone_three_musicmaker_two],
        [(31, 4), (32, 4), baritone_three_musicmaker_two],
        [(36, 4), (37, 4), baritone_three_musicmaker_one],
        [(37, 4), (39, 4), baritone_three_musicmaker_one],
        [(41, 4), (43, 4), baritone_three_musicmaker_two],
        [(43, 4), (87, 8), baritone_three_musicmaker_two],
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
        [(2, 4), (4, 4), bass_one_musicmaker_one],
        [(4, 4), (5, 4), bass_one_musicmaker_one],
        [(9, 4), (11, 4), bass_one_musicmaker_two],
        [(11, 4), (12, 4), bass_one_musicmaker_two],
        [(14, 4), (15, 4), bass_one_musicmaker_two],
        [(15, 4), (17, 4), bass_one_musicmaker_two],
        [(21, 4), (22, 4), bass_one_musicmaker_one],
        [(22, 4), (24, 4), bass_one_musicmaker_one],
        [(24, 4), (25, 4), bass_one_musicmaker_two],
        [(25, 4), (26, 4), bass_one_musicmaker_two],
        [(26, 4), (27, 4), bass_one_musicmaker_two],
        [(31, 4), (33, 4), bass_one_musicmaker_one],
        [(33, 4), (34, 4), bass_one_musicmaker_one],
        [(36, 4), (37, 4), bass_one_musicmaker_one],
        [(37, 4), (39, 4), bass_one_musicmaker_one],
        [(43, 4), (44, 4), bass_one_musicmaker_two],
        [(44, 4), (91, 8), bass_one_musicmaker_two],
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
        [(1, 8), (1, 4), bass_two_musicmaker_two],
        [(1, 4), (2, 4), bass_two_musicmaker_two],
        [(2, 4), (3, 4), bass_two_musicmaker_two],
        [(7, 4), (8, 4), bass_two_musicmaker_two],
        [(8, 4), (9, 4), bass_two_musicmaker_two],
        [(9, 4), (10, 4), bass_two_musicmaker_two],
        [(25, 8), (13, 4), bass_two_musicmaker_one],
        [(13, 4), (14, 4), bass_two_musicmaker_one],
        [(14, 4), (15, 4), bass_two_musicmaker_one],
        [(19, 4), (20, 4), bass_two_musicmaker_two],
        [(20, 4), (21, 4), bass_two_musicmaker_two],
        [(21, 4), (22, 4), bass_two_musicmaker_two],
        [(26, 4), (27, 4), bass_two_musicmaker_one],
        [(27, 4), (28, 4), bass_two_musicmaker_one],
        [(28, 4), (29, 4), bass_two_musicmaker_one],
        [(33, 4), (34, 4), bass_two_musicmaker_one],
        [(34, 4), (35, 4), bass_two_musicmaker_one],
        [(35, 4), (36, 4), bass_two_musicmaker_one],
        [(38, 4), (39, 4), bass_two_musicmaker_two],
        [(39, 4), (40, 4), bass_two_musicmaker_two],
        [(40, 4), (41, 4), bass_two_musicmaker_two],
        [(45, 4), (46, 4), bass_two_musicmaker_one],
        [(46, 4), (47, 4), bass_two_musicmaker_one],
        [(47, 4), (95, 8), bass_two_musicmaker_one],
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
        [(0, 4), (2, 4), contrabass_musicmaker_one],
        [(2, 4), (3, 4), contrabass_musicmaker_one],
        [(5, 4), (7, 4), contrabass_musicmaker_one],
        [(7, 4), (8, 4), contrabass_musicmaker_one],
        [(12, 4), (14, 4), contrabass_musicmaker_two],
        [(14, 4), (15, 4), contrabass_musicmaker_two],
        [(17, 4), (18, 4), contrabass_musicmaker_one],
        [(18, 4), (20, 4), contrabass_musicmaker_one],
        [(28, 4), (31, 4), contrabass_musicmaker_two],
        [(33, 4), (35, 4), contrabass_musicmaker_two],
        [(35, 4), (36, 4), contrabass_musicmaker_two],
        [(40, 4), (42, 4), contrabass_musicmaker_one],
        [(42, 4), (43, 4), contrabass_musicmaker_one],
        [(45, 4), (46, 4), contrabass_musicmaker_two],
        [(46, 4), (47, 4), contrabass_musicmaker_two],
        [(47, 4), (95, 8), contrabass_musicmaker_two],
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

# abjad.show(all_timespan_lists,
# key='annotation',
# scale=2
# )
offset_counter = abjad.meter.OffsetCounter(all_timespan_lists[:])
permitted_meters = abjad.meter.MeterList([(3, 4), (4, 4), (5, 4)])
fitted_meters = abjad.meter.Meter.fit_meters(
    argument=offset_counter,
    meters=permitted_meters,
)
# abjad.show(fitted_meters, range_=(0, 5))
for x in fitted_meters:
    abjad.f(x)
