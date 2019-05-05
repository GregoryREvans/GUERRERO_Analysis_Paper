\version "2.19.82"  %! LilyPondFile
\language "english" %! LilyPondFile

\include "first_stylesheet.ily" %! LilyPondFile

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
            \time 4/4
            s1 * 1
        }
        \context PianoStaff = "Staff Group"
        <<
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
                    \consists Horizontal_bracket_engraver
                    \override HorizontalBracket.staff-padding = #3
                    \override TextScript.staff-padding = #2
                }
                {
                    {
                        % [Voice 1 measure 1] %! COMMENT_MEASURE_NUMBERS
                        \once \override Stem.direction = #up
                        \clef "treble"
                        \change Staff = "Staff 2"
                        \ottava #-1
                        c,,4
                        ^ \markup { \translate #'(6 . 0) m2 }
                        \once \override Stem.direction = #up
                        \change Staff = "Staff 2"
                        cs,,4
                        ^ \markup { \translate #'(6 . 0) M3 }
                        \once \override Stem.direction = #up
                        \change Staff = "Staff 2"
                        f,,4
                        ^ \markup { \translate #'(6 . 0) P4 }
                        \once \override Stem.direction = #up
                        \change Staff = "Staff 2"
                        \tweak NoteHead.color #red
						\tweak Accidental.color #red
                        bf,,4
						- \tweak color #red
						^ \markup { 1 }
                        ^ \markup { \translate #'(6 . 0) M6 }
						- \tweak color #red
                        ^ \markup {
                            \large
                                \line
                                    {
                                        "SC(6-17){0, 1, 2, 4, 7, 8}"
                                    }
                            }
						- \tweak color #red
                        \startGroup
                    }
                    {
                        \once \override Stem.direction = #up
                        \change Staff = "Staff 2"
                        \ottava #0
                        \tweak color #red
                        g,4
						- \tweak color #red
						^ \markup { 4 }
                        ^ \markup { \translate #'(6 . 0) "M2" }
                        \once \override Stem.direction = #up
                        \change Staff = "Staff 2"
                        \tweak color #red
                        a,4
						- \tweak color #red
						^ \markup { 2 }
                        ^ \markup { \translate #'(6 . 0) P5 }
                        \once \override Stem.direction = #up
                        \change Staff = "Staff 2"
                        \tweak color #red
                        e4
						- \tweak color #red
						^ \markup { 7 }
                        ^ \markup { \translate #'(6 . 0) M7 }
                        \once \override Stem.direction = #down
                        \change Staff = "Staff 1"
                        \tweak NoteHead.color #red
						\tweak Accidental.color #red
                        ef'4
						- \tweak color #red
						^ \markup { 8 }
                        ^ \markup { \translate #'(6 . 0) m6 }
                        \once \override Stem.direction = #down
                        \change Staff = "Staff 1"
                        \tweak color #red
                        b'4
                        ^ \markup { \translate #'(6 . 0) m3 }
						- \tweak color #red
						^ \markup { 0 }
                        \stopGroup
                        \once \override Stem.direction = #down
                        \change Staff = "Staff 1"
                        d''4
                        ^ \markup { \translate #'(6 . 0) d5 }
                        \once \override Stem.direction = #down
                        \change Staff = "Staff 1"
                        af''4
                        ^ \markup { \translate #'(6 . 0) m7 }
                        \once \override Stem.direction = #down
                        \change Staff = "Staff 1"
                        fs'''4
                    }
                }
            }
            \context Staff = "Staff 2"
            \with
            {
                \consists Horizontal_bracket_engraver
                \override TextScript.staff-padding = #4
            }
            {
                \context Voice = "Voice 2"
                \with
                {
                    \consists Horizontal_bracket_engraver
                    \override HorizontalBracket.staff-padding = #3
                    \override TextScript.staff-padding = #2
                }
                {
                    {
                        % [Voice 2 measure 1] %! COMMENT_MEASURE_NUMBERS
                        \clef "bass"
                        r1
                    }
                    {
                        r\breve
                    }
                }
            }
        >>
    >>
} %! LilyPondFile
