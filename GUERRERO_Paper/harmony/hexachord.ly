\version "2.19.82"  %! LilyPondFile
\language "english" %! LilyPondFile

\include "first_stylesheet_2.ily" %! LilyPondFile

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
                        \tweak NoteHead.color #red
						\tweak Accidental.color #red
                        c'4
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
                        %{ - \tweak color #red
                        ^ \markup { 0 } %}
                        \once \override Stem.direction = #up
                        \tweak NoteHead.color #red
						\tweak Accidental.color #red
                        cs'4
                        %{ - \tweak color #red
                        ^ \markup { 1 } %}
                        \once \override Stem.direction = #up
                        \tweak NoteHead.color #red
						\tweak Accidental.color #red
                        d'4
                        %{ - \tweak color #red
                        ^ \markup { 2 } %}
                        \once \override Stem.direction = #up
                        \tweak NoteHead.color #red
						\tweak Accidental.color #red
                        e'4
						%{ - \tweak color #red
						^ \markup { 4 } %}
                    }
                    {
                        \once \override Stem.direction = #up
                        \tweak NoteHead.color #red
						\tweak Accidental.color #red
                        g'4
						%{ - \tweak color #red
						^ \markup { 7 } %}
                        \once \override Stem.direction = #up
                        \tweak NoteHead.color #red
						\tweak Accidental.color #red
                        af'4
						%{ - \tweak color #red
						^ \markup { 8 } %}
                        \stopGroup
                    }
                }
            }
    >>
} %! LilyPondFile
