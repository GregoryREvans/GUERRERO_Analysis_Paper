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
            \time 3/16
            s1 * 3/16
        }
        \new RhythmicStaff
        {
                            \tweak TupletNumber.text #(tuplet-number::append-note-wrapper(tuplet-number::non-default-tuplet-fraction-text 9 6) "32")
                            \times 2/3 {
                                % [Voice 1 measure 2] %! COMMENT_MEASURE_NUMBERS
                                \once \override Staff.NoteHead.style = #'default
                                \clef "varC"
                                c8
                                c8 ~
                                c32
                                ]
                            }
        }
    >>
} %! LilyPondFile
