\version "2.19.82"
\language "english"

#(set-default-paper-size "letterportrait")
#(set-global-staff-size 10)
%#(print-keys-verbose 'baritone-saxophone (current-error-port))

\include "ekmel.ily"
\ekmelicStyle evans

\relative c' {
  \textLengthOn
  <
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  dtef'
  \tweak NoteHead.color #darkgreen \tweak Accidental.color #darkgreen
  e
  des'>1\ff_
  \markup {
    \center-column {
      soprano1
      " "
		\override #'(size . 0.4)
		%\override #'(thickness . 0.15)
       \woodwind-diagram
                  #'soprano-saxophone
                   #'(
			(cc . (one two three four six))
			(lh . (ees d))
			(rh . (low-c))
			)
    }
  }

  \textLengthOn
  <
  \tweak NoteHead.color #darkgreen \tweak Accidental.color #darkgreen
  cs
  dtes
  des' >1\f_
  \markup {
    \center-column {
      soprano2
      " "
		\override #'(size . 0.4)
       \woodwind-diagram
                  #'soprano-saxophone
                   #'(
			(cc . (one two three four six))
			(lh . (ees d b))
			(rh . (low-c))
			)
    }
  }

  \textLengthOn
  <
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  ctes
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  eqf
  d'>1\f_
  \markup {
    \center-column {
      soprano3
      " "
		\override #'(size . 0.4)
       \woodwind-diagram
                  #'soprano-saxophone
                   #'(
			(cc . (one two three four five))
			(lh . (ees d))
			(rh . (low-c))
			)
    }
  }

  <
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  cqs
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  g'
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  eef'
  bf'>1\ff_
  \markup {
    \center-column {
      alto1
      " "
		\override #'(size . 0.4)
       \woodwind-diagram
                  #'alto-saxophone
                   #'(
			(cc . (one two three))
			(lh . (d gis))
			(rh . ())
			)
    }
  }

  <
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  cqs
  etef
  dqf' >1\mf_
  \markup {
    \center-column {
       alto2
       " "
		\override #'(size . 0.4)
       \woodwind-diagram
          #'alto-saxophone
        #'(
			(cc . (one two three four five))
			(lh . (b))
			(rh . (low-c c))
			)
    }
  }
  <
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  def,
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  dqf'
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  btef'
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  ef
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  fs>1\ff_\markup {
    \center-column {
      alto3
      " "
		\override #'(size . 0.4)
      \woodwind-diagram
        #'alto-saxophone
        #'(
			(cc . (one two three four five six))
			(lh . (low-bes))
			(rh . ())
			)
    }
  }

  <
  \tweak NoteHead.color #darkgreen \tweak Accidental.color #darkgreen
  fs
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  fqs'>1\mf_\markup {
    \center-column {
      tenor1
      " "
		\override #'(size . 0.4)
      \woodwind-diagram
        #'tenor-saxophone
        #'(
			(cc . (one two three five six))
			(lh . (cis))
			(rh . ())
			)
    }
  }

  <
  \tweak NoteHead.color #darkgreen \tweak Accidental.color #darkgreen
  fs
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  fqs'
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  dqf'
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  fs>1\mf_\markup {
    \center-column {
      tenor2
      " "
		\override #'(size . 0.4)
      \woodwind-diagram
        #'tenor-saxophone
        #'(
			(cc . (one two three five six))
			(lh . (b))
			(rh . ())
			)
    }
  }

  <
  \tweak NoteHead.color #darkgreen \tweak Accidental.color #darkgreen
  fs
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  fqs'
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  dqf'
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  gef>1\mp_\markup {
    \center-column {
      tenor3
      " "
		\override #'(size . 0.4)
      \woodwind-diagram
        #'tenor-saxophone
        #'(
			(cc . (one two three five six))
			(lh . ())
			(rh . ())
			)
    }
  }

  <
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  dtef'
  eqf'
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  ates>1\ff_\markup {
    \center-column {
      baritone1
      " "
		\override #'(size . 0.4)
      \woodwind-diagram
        #'baritone-saxophone
        #'(
			(cc . (one two three))
			(lh . (ees d gis))
			(rh . ())
			)
    }
  }

  <
  \tweak NoteHead.color #darkgreen \tweak Accidental.color #darkgreen
  e,
  eqs'
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  bqs'>1\mf_\markup {
    \center-column {
      baritone2
      " "
		\override #'(size . 0.4)
      \woodwind-diagram
        #'baritone-saxophone
        #'(
			(cc . (one two three four five))
			(lh . (b))
			(rh . (low-c))
			)
    }
  }

  <
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  gtes
  ftes'
  dqf'
  \tweak NoteHead.color #blue \tweak Accidental.color #blue
  bf'>1\ff_\markup {
    \center-column {
      baritone3
      " "
		\override #'(size . 0.4)
      \woodwind-diagram
        #'baritone-saxophone
        #'(
			(cc . (one two three five six))
			(lh . (low-a))
			(rh . (low-c))
			)
    }
  }

}
