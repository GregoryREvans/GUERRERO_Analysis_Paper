import abjad

#(set-default-paper-size "ledger")

voice_1_timespan_list = abjad.TimespanList([
    abjad.AnnotatedTimespan(
        start_offset=start_offset,
        stop_offset=stop_offset,
        annotation=music_maker
    )
    for start_offset, stop_offset, music_maker in [
        [(0, 8), (95, 8), 'GUERRERO Sections'],
        [(95, 8), (261, 8), 'GUERRERO Sections'],
        [(261, 8), (365, 8), 'GUERRERO Sections'],
        [(365, 8), (397, 8), 'GUERRERO Sections'],
        [(397, 8), (507, 8), 'GUERRERO Sections'],
        [(507, 8), (707, 8), 'GUERRERO Sections'],
        [(707, 8), (907, 8), 'GUERRERO Sections'],
        [(907, 8), (1003, 8), 'GUERRERO Sections'],
        [(1003, 8), (1099, 8), 'GUERRERO Sections'],
        [(1099, 8), (1211, 8), 'GUERRERO Sections'],
        [(1211, 8), (1267, 8), 'GUERRERO Sections'],
        # title - description - harmony - rhythm - tempo
        [(0, 8), (95, 8), 'Invocation - Shepard Tone - 24 Note Ascending Glissando - Talea - 60bpm'],
        [(95, 8), (261, 8), 'Section A - Sustained - Multiphonics - Sustained - 60bpm'],
        [(261, 8), (365, 8), 'Section B - Random Walk Glissando Swells - Centered Around Chord Tones - Talea - 90bpm'],
        [(365, 8), (397, 8), 'Section C - Transition - Increase Of Density - Talea - 90bpm'],
        [(397, 8), (507, 8), 'Section D - Tongue Slaps And Air Tones - Chord Tones - Talea - 108bpm'],
        [(507, 8), (707, 8), 'Section E - Trills And Fast Random Walks - Chord Tone Trills And Sustained Tones Drawn From Multiphonics - Even Divisions And Sustain - 90bpm'],
        [(707, 8), (907, 8), 'Section F - Trills And Sustains - Chord Tone Trills And Sustained Tones Drawn From Multiphonics - Talea - 90bpm'],
        [(907, 8), (1003, 8), 'Section G - Centered Around Chord Tones - Random Walk Glissando Swells - Talea - 90bpm'],
        [(1003, 8), (1099, 8), 'Section H - Shepard Tone - Tongue Slaps And Air Tone - Talea - 60bpm'],
        [(1099, 8), (1211, 8), 'Section I - Sustained - Chord Tone Random Walks - Talea - 90bpm'],
        [(1211, 8), (1267, 8), 'Section J - Conclusion Out Of Transition Material With Increase In Density - Chord Tones And Multiphonics - Talea - 90bpm'],
    ]
])

abjad.show(voice_1_timespan_list,
key='annotation',
scale=1.5
)
