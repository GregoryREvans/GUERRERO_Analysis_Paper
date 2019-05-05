\version "2.19.82"  %! LilyPondFile
\language "english" %! LilyPondFile

\include "first_stylesheet_3.ily" %! LilyPondFile

\header { %! LilyPondFile
    tagline = ##f
} %! LilyPondFile

\layout {}

\paper {}

\score { %! LilyPondFile
    \new Score
    <<
        \context TimeSignatureContext = "Global Context"
        {
            % [Global Context measure 1] %! COMMENT_MEASURE_NUMBERS
            \time 1/4
            s4

            \time 1/4
            s4

            \time 2/4
            s2

            \time 2/4
            s2

            \time 5/4
            s1
            s4

            \time 1/4
            s4

            \time 1/4
            s4

            \time 2/4
            s2

            \time 1/4
            s4

            \time 1/4
            s4

            \time 2/4
            s2

            \time 1/4
            s4
        }
            \context Staff = "Staff 1"
            \with
            {
                \consists Horizontal_bracket_engraver
                \override TextScript.staff-padding = #4
            }
            {
                \context Voice = "Voice 1"
                \with
                {
                    \override TextScript.staff-padding = #2
                }
                {
                    {
                        % [Voice 1 measure 1] %! COMMENT_MEASURE_NUMBERS
                        \override Stem.direction = #up
                        \clef "treble"
                        <c' cs' d'>4
                        ^\markup{ (012) }

                        <cs' d' e'>4
                        ^\markup{ (013) }

                        <c' cs' e'>4
                        ^\markup{ (014) }
                        <e' g' af'>4

                        <c' cs' af'>4
                        ^\markup{ (015) }
                        <c' g' af'>4

                        <c' cs' g'>4
                        ^\markup{ (016) }
                        <cs' d' g'>4
                        <cs' d' af'>4
                        <cs' g' af'>4
                        <d' g' af'>4

                        <c' d' e'>4
                        ^\markup{ (024) }

                        <d' e' g'>4
                        ^\markup{ (025) }

                        <c' d' af'>4
                        ^\markup{ (026) }
                        <d' e' af'>4

                        <c' d' g'>4
                        ^\markup{ (027) }

                        <cs' e' g'>4
                        ^\markup{ (036) }

                        <c' e' g'>4
                        ^\markup{ (037) }
                        <cs' e' af'>4

                        <c' e' af'>4
                        ^\markup{ (048) }

                    }
                }
            }
    >>
} %! LilyPondFile
