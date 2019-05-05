import abjad
import abjadext.rmakers
rhythm_maker = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(
        counts=[1, 2, 3, 4],
        denominator=16,
        ),
    )

divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
selections = rhythm_maker(divisions)
lilypond_file = abjad.LilyPondFile.rhythm(
    selections,
    divisions,
    )
abjad.show(lilypond_file)
#######
#######
rhythm_maker = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(
        counts=[1, 2, 3, 4],
        denominator=16,
        ),
    extra_counts_per_division=[0, 1, -1],
    )

divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
selections = rhythm_maker(divisions)
lilypond_file = abjad.LilyPondFile.rhythm(
    selections,
    divisions,
    )
abjad.show(lilypond_file)
#######
#######
rhythm_maker = abjadext.rmakers.TaleaRhythmMaker(
    talea=abjadext.rmakers.Talea(
        counts=[1, 2, 3, 4],
        denominator=16,
        ),
    extra_counts_per_division=[0, 1, -1],
    tuplet_specifier=abjadext.rmakers.TupletSpecifier(
        trivialize=True,
        extract_trivial=True,
        rewrite_rest_filled=True,
        rewrite_sustained=True,
        ),
    )

divisions = [(3, 8), (4, 8), (3, 8), (4, 8)]
selections = rhythm_maker(divisions)
lilypond_file = abjad.LilyPondFile.rhythm(
    selections,
    divisions,
    )
abjad.show(lilypond_file)
