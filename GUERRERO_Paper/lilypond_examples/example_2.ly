\version "2.19.82"  %! LilyPondFile
\language "english" %! LilyPondFile
\include "/Users/evansdsg2/spectralism_paper/lilypond_examples/stylesheet_2.ily"

\header { %! LilyPondFile
    tagline = ##f
} %! LilyPondFile

\layout {}

\paper {}

\score { %! LilyPondFile
    \new Score
    <<
        \context RhythmicStaff = "Upper Staff"
        \with
        {
            \override TextScript.staff-padding = #4
            \override TupletBracket.staff-padding = #0
        }
        {
            \times 2/3 {
                \tempo 4=60
                c16
                ^ \markup { 0'00'' }
                c8.
                %^ \markup { 0'00'' }
                \times 4/5 {
                    c16
                   % ^ \markup { 0'00'' }
                    c16
                  %  ^ \markup { 0'00'' }
                    c2
                  %  ^ \markup { 0'00'' }
                }
            }
            \times 4/5 {
                c8
                ^ \markup { 0'02'' }
                r16
              %  ^ \markup { 0'02'' }
                c16
             %   ^ \markup { 0'02'' }
                c16
              %  ^ \markup { 0'02'' }
            }
            c8.
            ^ \markup { 0'03'' }
            c16
           % ^ \markup { 0'03'' }
        }
    >>
} %! LilyPondFile