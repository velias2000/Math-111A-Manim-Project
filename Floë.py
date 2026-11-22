
from manim import *


class CyclicTransformations(Scene):
    def construct(self):

        
        #Colors
        
        WHITE_INK = "#F1F2F4"
        STAFF_COLOR = GRAY_B
        NOTE_COLORS = [BLUE, GREEN, YELLOW]

        
        #Title
        
        title = Text(
            "Floe — Philip Glass (1982)",
            font_size=36
        ).to_edge(UP, buff=0.3)

        subtitle = Text(
            "Musical Triplets and Cyclic Permutations",
            font_size=22,
            color=GRAY_B
        ).next_to(title, DOWN, buff=0.2)

        self.play(
            Write(title),
            FadeIn(subtitle)
        )

        
        #Five-Line Musical Staff 
       
        staff_center = 0.55
        spacing = 0.24

        staff = VGroup(*[
            Line(
                [-5.5, staff_center + i * spacing, 0],
                [5.5, staff_center + i * spacing, 0],
                color=STAFF_COLOR,
                stroke_width=2
            )
            for i in range(-2, 3)
        ])

        # Treble clef (font-dependent)
        clef = Text(
            "𝄞",
            font_size=100,
            color=WHITE_INK
        ).move_to([-4.8, staff_center, 0])

        self.play(
            Create(staff),
            FadeIn(clef),
            run_time=1.5
        )

        
        #Rhythmic Positions 
        
        x_positions = [-2.8, 0, 2.8]

        # Three pitches on the staff
        pitch_heights = [
            staff_center - spacing / 2,
            staff_center,
            staff_center + spacing / 2
        ]

        
        # MUSICAL NOTE FACTORY
        
        def make_note(color):

            head = Ellipse(
                width=0.34,
                height=0.23,
                fill_color=color,
                fill_opacity=1,
                stroke_width=0
            ).rotate(-PI / 8)

            stem = Line(
                [0.14, 0, 0],
                [0.14, 0.75, 0],
                color=color,
                stroke_width=3
            )

            return VGroup(head, stem)

        
        #Create Three Notes
        
        tokens = VGroup()

        for i in range(3):

            note = make_note(NOTE_COLORS[i])

            label = Text(
                str(i),
                font_size=25,
                color=NOTE_COLORS[i]
            ).next_to(note, UP, buff=0.18)

            token = VGroup(note, label)

            token.move_to([
                x_positions[i],
                pitch_heights[i],
                0
            ])

            tokens.add(token)

        self.play(
            LaggedStart(
                *[
                    FadeIn(token, shift=UP * 0.15)
                    for token in tokens
                ],
                lag_ratio=0.25
            )
        )

        
        #Position Labels
        
        positions = VGroup(*[
            Text(
                f"Position {i}",
                font_size=20,
                color=GRAY_B
            ).move_to([x_positions[i], -0.55, 0])
            for i in range(3)
        ])

        self.play(FadeIn(positions))

        
        #Algebraic Information
        
        transformation = Text(
            "Iteration 0: Identity (e)",
            font_size=27
        ).move_to([0, -1.5, 0])

        arrangement = Text(
            "(0, 1, 2)",
            font_size=32,
            color=YELLOW
        ).move_to([0, -2.15, 0])

        self.play(
            Write(transformation),
            Write(arrangement)
        )

        self.wait(1)

        
        #Cyclic Permutations of the Notes
        
        descriptions = [
            "Iteration 0: e",
            "Iteration 1: σ",
            "Iteration 2: σ²",
            "Iteration 3: σ³ = e"
        ]

        arrangements = [
            "(0, 1, 2)",
            "(2, 0, 1)",
            "(1, 2, 0)",
            "(0, 1, 2)"
        ]

        for step in range(1, 4):

            new_description = Text(
                descriptions[step],
                font_size=27
            ).move_to(transformation)

            new_arrangement = Text(
                arrangements[step],
                font_size=32,
                color=YELLOW
            ).move_to(arrangement)

            animations = []

            for i, token in enumerate(tokens):

                target_index = (i + step) % 3

                # Preserve each note's pitch
                target = [
                    x_positions[target_index],
                    pitch_heights[i],
                    0
                ]

                animations.append(
                    token.animate.move_to(target)
                )

            self.play(
                Transform(
                    transformation,
                    new_description
                ),
                Transform(
                    arrangement,
                    new_arrangement
                ),
                *animations,
                run_time=1.6
            )

            self.wait(0.8)

        
        #Complete Musical Score with Barlines
        
        self.play(
            FadeOut(staff),
            FadeOut(clef),
            FadeOut(tokens),
            FadeOut(positions),
            FadeOut(transformation),
            FadeOut(arrangement)
        )

        conclusion = VGroup(
            Text(
                "The Cyclic Group of Order 3",
                font_size=33
            ),
            Text(
                "<σ> = {e, σ, σ²}",
                font_size=37,
                color=YELLOW
            ),
            Text(
                "σ³ = e",
                font_size=46,
                color=GREEN
            ),
            Text(
                "Three cyclic shifts restore the pattern.",
                font_size=22,
                color=GRAY_B
            )
        ).arrange(DOWN, buff=0.35)

        self.play(
            LaggedStart(
                *[Write(item) for item in conclusion],
                lag_ratio=0.3
            )
        )

        self.wait(3)

