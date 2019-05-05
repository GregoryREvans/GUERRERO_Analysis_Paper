import abjad
outer_tuplet_one = abjad.Tuplet((2 , 3), "c'16 cs'8.")
inner_tuplet = abjad.Tuplet((4 , 5), "d'16 ds'16 e'2")
outer_tuplet_one.append(inner_tuplet)
outer_tuplet_two = abjad.Tuplet((4 , 5))
outer_tuplet_two.extend("f'8 r16 fs'16 g'16")
tuplets = [outer_tuplet_one , outer_tuplet_two]
upper_staff = abjad.Staff(tuplets , name='Upper Staff')
note_one = abjad.Note(8 , (3, 16))
upper_staff.append(note_one)
note_two = abjad.Note(abjad.NamedPitch("a'"), abjad.Duration(1, 16))
upper_staff.append(note_two)
mark = abjad.MetronomeMark((1, 4), 60)
abjad.attach(mark, upper_staff[0][0])
expression = abjad.label().with_start_offsets(clock_time=True)
for leaf in abjad.select(upper_staff).leaves():
    expression(leaf)
score = abjad.Score([upper_staff])
abjad.override(upper_staff).text_script.staff_padding = 4
abjad.override(upper_staff).tuplet_bracket.staff_padding = 0
abjad.show(score)
