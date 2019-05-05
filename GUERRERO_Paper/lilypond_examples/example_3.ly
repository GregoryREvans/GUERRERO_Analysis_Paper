\version "2.19.82"  %! LilyPondFile
\language "english" %! LilyPondFile

\include "/Users/evansdsg2/spectralism_paper/lilypond_examples/stylesheet_3.ily"                                      %! LilyPondFile
\include "/Users/evansdsg2/abjad/docs/source/_stylesheets/abjad.ily" %! LilyPondFile

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
            % [Global Context measure 2] %! COMMENT_MEASURE_NUMBERS
            \time 5/4
            s1 * 5/4
            \bar "|"

        }
        \context StaffGroup = "Staff Group 1"
        <<
            \context BowStaff = "Staff 1"
            {
                \context Voice = "Voice 1"
                {
                    {
                        \times 16/17 {
                            % [Voice 1 measure 1] %! COMMENT_MEASURE_NUMBERS
                            \set Staff.shortInstrumentName =
                            \markup { B.H. }
                            \set Staff.instrumentName =
                            \markup { "Bow Hand" }
                            \tempo 8=60
                            \clef "percussion"
                            \tweak Y-offset #2.0
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            1
                                            1
                                }
                            a'''16
                            - \tweak style #'line
                            \glissando
                            ^ \upbow
                            \tweak Y-offset #0.4
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            3
                                            5
                                }
                            a'''16
                            - \tweak style #'line
                            \glissando
                            \tweak Y-offset #-1.2
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            1
                                            5
                                }
                            a'''16
                            - \tweak style #'line
                            \glissando
                            ^ \downbow
                            \tweak Y-offset #1.2
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            4
                                            5
                                }
                            a'''8
                            - \tweak style #'line
                            \glissando
                            ^ \upbow
                            \tweak Y-offset #-0.4
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            2
                                            5
                                }
                            a'''16
                            - \tweak style #'zigzag
                            \glissando
                            ^ \downbow
                            \tweak Y-offset #2.0
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            1
                                            1
                                }
                            a'''8.
                            - \tweak style #'zigzag
                            \glissando
                            ^ \upbow
                            \tweak Y-offset #-0.4
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            2
                                            5
                                }
                            a'''16
                            - \tweak style #'line
                            \glissando
                            ^ \downbow
                            \tweak Y-offset #1.2
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            4
                                            5
                                }
                            a'''16
                            ~
                            - \tweak style #'line
                            \glissando
                            \tweak Y-offset #1.2
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            4
                                            5
                                }
                            a'''16
                            - \tweak style #'line
                            \glissando
                            ^ \parenthesize \upbow
                            \tweak Y-offset #-1.2
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            1
                                            5
                                }
                            a'''8.
                            - \tweak style #'line
                            \glissando
                            ^ \downbow
                            \tweak Y-offset #1.2
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            4
                                            5
                                }
                            a'''16
                            - \tweak style #'dotted-line
                            \glissando
                            ^ \upbow
                            \tweak Y-offset #-1.2
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            1
                                            5
                                }
                            a'''16
                            - \tweak style #'line
                            \glissando
                            ^ \downbow
                        }
                    }
                    {
                        % [Voice 1 measure 2] %! COMMENT_MEASURE_NUMBERS
                        \tweak Y-offset #1.2
                        \tweak stencil #ly:text-interface::print
                        \tweak text \markup {
                            \center-align
                                \vcenter
                                    \fraction
                                        4
                                        5
                            }
                        a'''16
                        - \tweak style #'line
                        \glissando
                        ^ \upbow
                        \tweak Y-offset #-0.4
                        \tweak stencil #ly:text-interface::print
                        \tweak text \markup {
                            \center-align
                                \vcenter
                                    \fraction
                                        2
                                        5
                            }
                        a'''16
                        ~
                        - \tweak style #'line
                        \glissando
                        \tweak Y-offset #-0.4
                        \tweak stencil #ly:text-interface::print
                        \tweak text \markup {
                            \center-align
                                \vcenter
                                    \fraction
                                        2
                                        5
                            }
                        a'''16
                        - \tweak style #'line
                        \glissando
                        ^ \parenthesize \downbow
                        \tweak Y-offset #2.0
                        \tweak stencil #ly:text-interface::print
                        \tweak text \markup {
                            \center-align
                                \vcenter
                                    \fraction
                                        1
                                        1
                            }
                        a'''16
                        - \tweak style #'line
                        \glissando
                        ^ \upbow
                        \tweak Y-offset #1.2
                        \tweak stencil #ly:text-interface::print
                        \tweak text \markup {
                            \center-align
                                \vcenter
                                    \fraction
                                        4
                                        5
                            }
                        a'''8.
                        - \tweak style #'line
                        \glissando
                        ^ \downbow
                        \tweak Y-offset #2.0
                        \tweak stencil #ly:text-interface::print
                        \tweak text \markup {
                            \center-align
                                \vcenter
                                    \fraction
                                        1
                                        1
                            }
                        a'''16
                        - \tweak style #'dotted-line
                        \glissando
                        ^ \upbow
                        \tweak Y-offset #-0.4
                        \tweak stencil #ly:text-interface::print
                        \tweak text \markup {
                            \center-align
                                \vcenter
                                    \fraction
                                        2
                                        5
                            }
                        a'''8
                        - \tweak style #'dotted-line
                        \glissando
                        ^ \downbow
                        \tweak Y-offset #1.2
                        \tweak stencil #ly:text-interface::print
                        \tweak text \markup {
                            \center-align
                                \vcenter
                                    \fraction
                                        4
                                        5
                            }
                        a'''8
                    }
                    {
                        r2
                        \!
                    }

                }
            }
            \context BeamStaff = "Staff 5"
            {
                \context Voice = "Voice 5"
                \with
                {
                    \override TextSpanner.staff-padding = #0
                }
                {
                    {
                        \times 16/17 {
                            % [Voice 5 measure 1] %! COMMENT_MEASURE_NUMBERS
                            \set Staff.shortInstrumentName =
                            \markup { vc.I }
                            \set Staff.instrumentName =
                            \markup { "Violoncello I" }
                            \clef "percussion"
                            a'''16
                            [
                            - \abjad-dashed-line-with-arrow
                            - \tweak bound-details.left.text \markup {
                                \concat
                                    {
                                        \upright
                                            st.
                                        \hspace
                                            #0.5
                                    }
                                }
                            - \tweak bound-details.right.text \markup {
                                \upright
                                    ord.
                                }
                            \startTextSpan
                            a'''16
                            a'''16
                            a'''8
                            a'''16
                            a'''8.
                            a'''16
                            a'''16
                            ~
                            a'''16
                            a'''8.
                            a'''16
                            a'''16
                        }
                    }
                    {
                        % [Voice 5 measure 2] %! COMMENT_MEASURE_NUMBERS
                        a'''16
                        a'''16
                        ~
                        a'''16
                        a'''16
                        a'''8.
                        a'''16
                        a'''8
                        a'''8
                        \stopTextSpan
                        ]
                    }
                    {
                        r2
                        \!
                    }
                }
            }
            \context Staff = "Staff 2"
            {
                \context Voice = "Voice 2"
                {
                    {
                        \times 16/17 {
                            % [Voice 2 measure 1] %! COMMENT_MEASURE_NUMBERS
                            \set Staff.shortInstrumentName =
                            \markup { L.H. }
                            \set Staff.instrumentName =
                            \markup { "Left Hand" }
                            \clef "bass"
                            cs16
                            \fff
                            - \tenuto
                            \>
                            [
                            e,8
                            - \tenuto
                            <c, cs>16
                            - \tenuto
                            cs8.
                            - \tenuto
                            e,16
                            - \tenuto
                            <e, fs>16
                            - \tenuto
                            ~
                            <e, fs>16
                            <c fs>8.
                            - \tenuto
                            fs16
                            - \tenuto
                            c16
                            - \tenuto
                            fs16
                            - \tenuto
                            <e, fs>16
                            \mf
                            - \tenuto
                            - \tweak stencil #constante-hairpin
                            \<
                        }
                    }
                    {
                        % [Voice 2 measure 2] %! COMMENT_MEASURE_NUMBERS
                        cqs8..
                        \p
                        - \accent
                        - \tweak stencil #constante-hairpin
                        \<
                        c32
                        - \accent
                        ~
                        c16.
                        cqs32
                        - \accent
                        ~
                        cqs8
                        ~
                        cqs32
                        c16.
                        - \accent
                        cqs8
                        \mp
                        - \accent
                        - \tweak stencil #constante-hairpin
                        \<
                        ]
                    }
                    {
                        r2
                        \!
                    }
                }
            }
        >>
        \context StaffGroup = "Staff Group 2"
        <<
            \context BowStaff = "Staff 3"
            {
                \context Voice = "Voice 3"
                {
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 12/13 {
                            % [Voice 3 measure 1] %! COMMENT_MEASURE_NUMBERS
                            \set Staff.shortInstrumentName =
                            \markup { B.H. }
                            \set Staff.instrumentName =
                            \markup { "Bow Hand" }
                            \tempo 8=60
                            \clef "percussion"
                            \tweak Y-offset #-1.2
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            1
                                            5
                                }
                            a'''16
                            - \tweak style #'line
                            \glissando
                            ^ \downbow
                            \tweak Y-offset #-0.4
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            2
                                            5
                                }
                            a'''16
                            - \tweak style #'line
                            \glissando
                            \tweak Y-offset #0.4
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            3
                                            5
                                }
                            a'''16
                            ~
                            - \tweak style #'line
                            \glissando
                            \tweak Y-offset #0.4
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            3
                                            5
                                }
                            a'''16
                            - \tweak style #'line
                            \glissando
                            ^ \parenthesize \downbow
                            \tweak Y-offset #1.2
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            4
                                            5
                                }
                            a'''8.
                            - \tweak style #'line
                            \glissando
                            \tweak Y-offset #2.0
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            1
                                            1
                                }
                            a'''16
                            - \tweak style #'zigzag
                            \glissando
                            ^ \upbow
                            \tweak Y-offset #1.2
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            4
                                            5
                                }
                            a'''16
                            - \tweak style #'zigzag
                            \glissando
                            ^ \downbow
                            \tweak Y-offset #2.0
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            1
                                            1
                                }
                            a'''16
                            - \tweak style #'line
                            \glissando
                            ^ \upbow
                            \tweak Y-offset #1.2
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            4
                                            5
                                }
                            a'''16
                            ~
                            - \tweak style #'line
                            \glissando
                            \tweak Y-offset #1.2
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            4
                                            5
                                }
                            a'''16
                            - \tweak style #'line
                            \glissando
                            ^ \parenthesize \downbow
                            \tweak Y-offset #2.0
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            1
                                            1
                                }
                            a'''16
                            - \tweak style #'line
                            \glissando
                            ^ \upbow
                        }
                        \tweak Y-offset #1.2
                        \tweak stencil #ly:text-interface::print
                        \tweak text \markup {
                            \center-align
                                \vcenter
                                    \fraction
                                        4
                                        5
                            }
                        a'''8.
                        - \tweak style #'dotted-line
                        \glissando
                        \tweak Y-offset #0.4
                        \tweak stencil #ly:text-interface::print
                        \tweak text \markup {
                            \center-align
                                \vcenter
                                    \fraction
                                        3
                                        5
                            }
                        a'''16
                        - \tweak style #'line
                        \glissando
                        ^ \downbow
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 4/3 {
                            % [Voice 3 measure 2] %! COMMENT_MEASURE_NUMBERS
                            \tweak Y-offset #1.2
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            4
                                            5
                                }
                            a'''8
                            - \tweak style #'line
                            \glissando
                            \tweak Y-offset #2.0
                            \tweak stencil #ly:text-interface::print
                            \tweak text \markup {
                                \center-align
                                    \vcenter
                                        \fraction
                                            1
                                            1
                                }
                            a'''16
                        }
                    }
                    {
                        r2.
                        \!
                    }
                    {
                        \tweak Y-offset #1.2
                        \tweak stencil #ly:text-interface::print
                        \tweak text \markup {
                            \center-align
                                \vcenter
                                    \fraction
                                        4
                                        5
                            }
                        a'''8
                        - \tweak style #'line
                        \glissando
                        ^ \downbow
                        \tweak Y-offset #2.0
                        \tweak stencil #ly:text-interface::print
                        \tweak text \markup {
                            \center-align
                                \vcenter
                                    \fraction
                                        1
                                        1
                            }
                        a'''16
                        - \tweak style #'line
                        \glissando
                        ^ \upbow
                        \tweak Y-offset #1.2
                        \tweak stencil #ly:text-interface::print
                        \tweak text \markup {
                            \center-align
                                \vcenter
                                    \fraction
                                        4
                                        5
                            }
                        a'''16
                        - \tweak style #'dotted-line
                        \glissando
                        ^ \downbow
                    }
                }
            }
            \context BeamStaff = "Staff 6"
            {
                \context Voice = "Voice 6"
                \with
                {
                    \override TextSpanner.staff-padding = #0
                }
                {
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 12/13 {
                            % [Voice 6 measure 1] %! COMMENT_MEASURE_NUMBERS
                            \set Staff.shortInstrumentName =
                            \markup { vc.II }
                            \set Staff.instrumentName =
                            \markup { "Violoncello II" }
                            \clef "percussion"
                            a'''16
                            [
                            - \abjad-dashed-line-with-arrow
                            - \tweak bound-details.left.text \markup {
                                \concat
                                    {
                                        \upright
                                            sp.
                                        \hspace
                                            #0.5
                                    }
                                }
                            - \tweak bound-details.right.text \markup {
                                \upright
                                    msp.
                                }
                            \startTextSpan
                            a'''16
                            a'''16
                            ~
                            a'''16
                            a'''8.
                            a'''16
                            a'''16
                            a'''16
                            a'''16
                            ~
                            a'''16
                            a'''16
                        }
                        a'''8.
                        a'''16
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 4/3 {
                            % [Voice 6 measure 2] %! COMMENT_MEASURE_NUMBERS
                            a'''8
                            a'''16
                            \stopTextSpan
                            ]
                        }
                    }
                    {
                      \once \override Dots.transparent = ##t
                        r2.
                        \!
                    }
                    {
                        a'''8
                        [
                        - \abjad-dashed-line-with-arrow
                        - \tweak bound-details.left.text \markup {
                            \concat
                                {
                                    \upright
                                        ord.
                                    \hspace
                                        #0.5
                                }
                            }
                        - \tweak bound-details.right.text \markup {
                            \upright
                                st.
                            }
                        \startTextSpan
                        a'''16
                        a'''16 ]
                    }
                }
            }
            \context Staff = "Staff 4"
            {
                \context Voice = "Voice 4"
                {
                    {
                        % [Voice 4 measure 1] %! COMMENT_MEASURE_NUMBERS
                        \set Staff.shortInstrumentName =
                        \markup { L.H. }
                        \set Staff.instrumentName =
                        \markup { "Left Hand" }
                        \clef "bass"
                        e16.
                        \p
                        - \accent
                        - \tweak stencil #constante-hairpin
                        \<
                        [
                        eqf32
                        ~
                        eqf8
                        ef16.
                        - \accent
                        dqs32
                        - \accent
                        ~
                        dqs8
                        ~
                        dqs32
                        d16.
                        - \accent
                        ~
                        d32
                        dqs16.
                        \mp
                        - \accent
                        - \tweak stencil #constante-hairpin
                        \<
                    }
                    {
                        <e, fs>8
                        \fff
                        - \tenuto
                        \>
                        <c fs>16
                        - \tenuto
                        fs16
                        \mf
                        - \tenuto
                        - \tweak stencil #constante-hairpin
                        \<
                    }
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 8/7 {
                            % [Voice 4 measure 2] %! COMMENT_MEASURE_NUMBERS
                            ef8
                            \p
                            - \accent
                            - \tweak stencil #constante-hairpin
                            \<
                            dqs16.
                            \mp
                            - \accent
                            - \tweak stencil #constante-hairpin
                            \<
                            ]
                        }
                    }
                    {
                        r2.
                        \!
                    }
                    {
                        ef32
                        \p
                        - \accent
                        - \tweak stencil #constante-hairpin
                        \<
                        [
                        eqf32
                        - \accent
                        ~
                        eqf8
                        ~
                        eqf32
                        ef32 ]
                        \mp
                        - \accent
                        - \tweak stencil #constante-hairpin
                        \<
                    }
                }
            }
        >>
    >>
} %! LilyPondFile
