% 2018-07-17 19:54

\version "2.19.82"
\language "english"
%{ #(set-default-paper-size "letterportrait") %}
#(set-default-paper-size "letterportrait")
%{ #(set-global-staff-size 9.5) %}
#(set-global-staff-size 11)
\include "ekmel.ily"
\ekmelicStyle evans

%{ \header {
	tagline = ##f
	breakbefore = ##t
	dedication = \markup \override #'(font-name . "Didot") \fontsize #1.7 \center-column {"t  o     t  h  e     F  r  o  s  t     S  a  x  o  p  h  o  n  e    E  n  s  e  m  b  l  e"}
	title =  \markup \override #'(font-name . "Didot") \fontsize #13 \bold\center-column {"GUERRERO" }
	subtitle = \markup \override #'(font-name . "Didot") \fontsize #4 \center-column {"f o r      t w e n t y   -   o n e      s a x o p h o n e s"}
	subsubtitle = \markup \override #'(font-name . "Didot") \fontsize #3 \center-column {"b       o       c       e       t       o       s               d       e               m       a       r       t       e"}
	arranger = \markup \override #'(font-name . "Didot") \fontsize #2 {"Gregory Rowland Evans"}
} %}

\layout {
    \accidentalStyle forget
	%\accidentalStyle modern
	%\accidentalStyle modern-cautionary
	%\accidentalStyle modern
    indent = #0
	ragged-last = ##t
    ragged-right = ##t
    %left-margin = #15
	\context {
        \name GlobalContext
        \type Engraver_group
        \numericTimeSignature
        \consists Axis_group_engraver
		\consists Bar_number_engraver
        \consists Time_signature_engraver
		\consists Mark_engraver
		\consists Metronome_mark_engraver
		\override BarNumber.Y-extent = #'(0 . 0)
		\override BarNumber.Y-offset = 0
		\override BarNumber.extra-offset = #'(-4 . 0)
		%\override BarNumber.font-name = "Didot"
		%{ \override BarNumber.stencil = #(make-stencil-boxer 0.1 0.7 ly:text-interface::print) %}
		%{ \override BarNumber.stencil = #(make-stencil-circler 0.1 0.7 ly:text-interface::print) %}
		\override BarNumber.font-size = 1
		\override BarNumber.padding = 4
        \override BarNumber.transparent = ##t
		\override MetronomeMark.X-extent = #'(0 . 0)
		\override MetronomeMark.Y-extent = #'(0 . 0)
		\override MetronomeMark.break-align-symbols = #'(left-edge)
		\override MetronomeMark.extra-offset = #'(0 . 4)
		\override MetronomeMark.font-size = 4
		%\override RehearsalMark.stencil = #(make-stencil-circler 0.1 0.7 ly:text-interface::print)
		\override RehearsalMark.stencil = #(make-stencil-boxer 0.1 0.7 ly:text-interface::print)
		\override RehearsalMark.X-extent = #'(0 . 0)
		\override RehearsalMark.X-offset = 5
		\override RehearsalMark.Y-offset = -2.25
		\override RehearsalMark.break-align-symbols = #'(time-signature)
		\override RehearsalMark.break-visibility = #end-of-line-invisible
		\override RehearsalMark.font-name = "Didot"
		\override RehearsalMark.font-size = 6
		\override RehearsalMark.outside-staff-priority = 500
		\override RehearsalMark.self-alignment-X = #center
        \override TimeSignature.X-extent = #'(0 . 0)
        \override TimeSignature.X-offset = #ly:self-alignment-interface::x-aligned-on-self
        \override TimeSignature.Y-extent = #'(0 . 0)
        \override TimeSignature.break-align-symbol = ##f
        \override TimeSignature.break-visibility = #end-of-line-invisible
        \override TimeSignature.font-size = #-1
        \override TimeSignature.transparent = ##t
        \override TimeSignature.self-alignment-X = #center
        \override VerticalAxisGroup.default-staff-staff-spacing = #'((basic-distance . 1) (minimum-distance . 1) (padding . 1) (stretchability . 0))
    }
    \context {
        \Score
        \remove Bar_number_engraver
		\remove Mark_engraver
        \accepts GlobalContext
		\override BarLine.bar-extent = #'(-2 . 2)
		\override BarLine.hair-thickness = #1.2
		\override BarLine.thick-thickness = #2.7
        \override Beam.breakable = ##t
		\override Beam.concaveness = #10000
		\override DynamicText.font-size = #-3
		\override Glissando.breakable = ##t
		\override Glissando.thickness = #2.5
		\override Tie.breakable = ##t
        \override SpacingSpanner.strict-grace-spacing = ##t
        \override SpacingSpanner.strict-note-spacing = ##t
        \override SpacingSpanner.uniform-stretching = ##t
        \override StaffGrouper.staff-staff-spacing = #'((basic-distance . 1) (minimum-distance . 1) (padding . 0))
		\override Stem.stemlet-length = #1.15
        \override TupletBracket.bracket-visibility = ##t
        \override TupletBracket.minimum-length = #3
        \override TupletBracket.padding = #2
        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
        \override TupletNumber.text = #tuplet-number::calc-fraction-text
        \override TimeSignature.whiteout = ##t
		proportionalNotationDuration = #(ly:make-moment 1 30)
        autoBeaming = ##f
        tupletFullLength = ##t
        \numericTimeSignature
    }
	\context {
        \Voice
        \remove Forbid_line_break_engraver
    }
    \context {
        \Staff
        %{ \remove Time_signature_engraver %}
		fontSize = #-1
		%{ \consists Page_turn_engraver
		minimumPageTurnLength = #(ly:make-moment 1 4) %}
    }
    \context {
        \RhythmicStaff
        %{ \remove Time_signature_engraver %}
    }
       \context {
        \StaffGroup
    }
}

\paper {
	%{ page-breaking = #ly:page-turn-breaking %}
	%{ system-system-spacing = #'((basic-distance . 15) (padding . 0)) %}
	system-system-spacing = #'((basic-distance . 1) (padding . 0))

	top-margin = 1\cm
	bottom-margin = 0.6\cm
	left-margin = 1.5\cm
	right-margin = 0.6\cm

	%top-margin = .90\in
	oddHeaderMarkup = \markup ""
	evenHeaderMarkup = \markup ""
	oddFooterMarkup = \markup \fill-line {
    ""
    \concat {
      "GUERRERO ~"
	  \fontsize #2
	  \fromproperty #'page:page-number-string "~ Evans"
     }
    ""
  }
  evenFooterMarkup = \markup \fill-line {
    ""
	\concat { "GUERRERO ~" \fontsize #2
	\fromproperty #'page:page-number-string "~ Evans"
    } ""
  }
}
