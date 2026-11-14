from manim import *

class Staff(VGroup):
    def __init__(self, length=10, line_spacing=0.25, **kwargs):
        super().__init__(**kwargs)
        self.line_spacing = line_spacing
        
        # Create the 5 horizontal staff lines (bottom = 0, top = 4)
        self.lines = VGroup(*[
            Line(LEFT * length / 2, RIGHT * length / 2, stroke_width=2)
            for _ in range(5)
        ])
        self.lines.arrange(UP, buff=line_spacing)
        
        # Add start and end barlines
        left_bar = Line(self.lines[0].get_start(), self.lines[-1].get_start(), stroke_width=3)
        right_bar = Line(self.lines[0].get_end(), self.lines[-1].get_end(), stroke_width=4)
        
        self.add(self.lines, left_bar, right_bar)

    def get_pitch_y(self, step):
        """
        Returns the Y-coordinate for a given staff step:
        0 = bottom line (E4 in treble)
        1 = first space (F4)
        2 = second line (G4)
        ...
        8 = top line (F5)
        """
        bottom_y = self.lines[0].get_y()
        return bottom_y + step * (self.line_spacing / 2)

class MusicStaffScene(Scene):
    def construct(self):
        # Initialize the staff
        staff = Staff(length=10, line_spacing=0.3)
        
        # Add a simple clef label (or replace with an SVGMobject treble clef)
        clef = Text("𝄞", font_size=96).move_to(staff.lines[2].get_left() + RIGHT * 0.6)
        
        # Place a notehead on the 2nd line (G4, step=2)
        note = Ellipse(width=0.35, height=0.24, color=WHITE, fill_opacity=1)
        note.rotate(20 * DEGREES)
        note.move_to([staff.get_left()[0] + 2.2, staff.get_pitch_y(2), 0])
        
        # Add a stem to the note
        stem = Line(
            note.get_right() + LEFT * 0.02,
            note.get_right() + LEFT * 0.02 + UP * 1.0,
            stroke_width=2.5
        )
        quarter_note = VGroup(note, stem)

        # Animate the scene
        self.play(Create(staff), Write(clef))
        self.play(FadeIn(quarter_note, shift=DOWN * 0.2))
        self.wait(2)
