\version "2.19.82"  %! LilyPondFile
\language "english" %! LilyPondFile
\include "/Users/evansdsg2/spectralism_paper/lilypond_examples/stylesheet.ily"

\header { %! LilyPondFile
    tagline = ##f
} %! LilyPondFile

\layout {}

\paper {}

\score { %! LilyPondFile
    \new Score
    <<
        \context RhythmicStaff = "Upper Staff"
        {
            \times 2/3 {
\tempo 4=60
                c16 [
                c8.
                \times 4/5 {
                    c16
                    c16 ]
                    c2
                }
            }
            \times 4/5 {
                c8
                r16
                c16 [
                c16
            }
            c8.
            c16 ]
        }
    >>
} %! LilyPondFile
