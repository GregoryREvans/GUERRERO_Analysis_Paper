\version "2.19.82"  %! LilyPondFile
\language "english" %! LilyPondFile

\include "/Users/evansdsg2/abjad/docs/source/_stylesheets/default.ily"           %! LilyPondFile
\include "/Users/evansdsg2/spectralism_paper/lilypond_examples/talea/stylesheet_4.ily"

\header { %! LilyPondFile
    tagline = ##f
} %! LilyPondFile

\layout {}

\paper {}

\score { %! LilyPondFile
    \new Score
    <<
        \new GlobalContext
        {
            \time 3/8
            s1 * 3/8
            \time 4/8
            s1 * 1/2
            \time 3/8
            s1 * 3/8
            \time 4/8
            s1 * 1/2
        }
        \new RhythmicStaff
        {
            c'16
            [
            c'8
            c'8.
            ]
            c'4
            c'16
            [
            c'8
            c'16
            ~
            ]
            c'8
            c'4
            c'16
            [
            c'8
            c'8.
            c'8
            ]
        }
    >>
} %! LilyPondFile