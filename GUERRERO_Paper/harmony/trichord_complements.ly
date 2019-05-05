\version "2.19.82"  %! LilyPondFile
\language "english" %! LilyPondFile

\include "first_stylesheet_4.ily" %! LilyPondFile

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
            \time 2/4
            s2

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
                        ^\markup{ (012) \teeny \fraction 1 1}
                        <e' g' af'>4
                         ^\markup{ (014) \teeny \fraction 2 2}

                        <cs' d' e'>4
                        ^\markup{ (013) \teeny \fraction 1 1}
                        <c' g' af'>4
                        ^\markup{ (015) \teeny \fraction 2 2}

                        <c' cs' e'>4
                        ^\markup{ (014) \teeny \fraction 1 2}
                        <d' g' af'>4
                        ^\markup{ (016) \teeny \fraction 5 5}

                        <c' cs' af'>4
                        ^\markup{ (015) \teeny \fraction 1 2}
                        <d' e' g'>4
                        ^\markup{ (025) \teeny \fraction 1 1}

                        <c' cs' g'>4
                        ^\markup{ (016) \teeny \fraction 1 5}
                        <d' e' af'>4
                        ^\markup{ (026) \teeny \fraction 2 2}

                        <cs' d' g'>4
                        ^\markup{ (016) \teeny \fraction 2 5}
                        <c' e' af'>4
                        ^\markup{ (048) \teeny \fraction 1 1}

                        <cs' d' af'>4
                        ^\markup{ (016) \teeny \fraction 3 5}
                        <c' e' g'>4
                        ^\markup{ (037) \teeny \fraction 1 2}

                        <cs' g' af'>4
                        ^\markup{ (016) \teeny \fraction 4 5}
                        <c' d' e'>4
                        ^\markup{ (024) \teeny \fraction 1 1}

                        <c' d' af'>4
                        ^\markup{ (026) \teeny \fraction 1 2}
                        <cs' e' g'>4
                        ^\markup{ (036) \teeny \fraction 1 1}

                        <c' d' g'>4
                        ^\markup{ (027) \teeny \fraction 1 1}
                        <cs' e' af'>4
                        ^\markup{ (037) \teeny \fraction 2 2}

                    }
                }
            }
    >>
} %! LilyPondFile
