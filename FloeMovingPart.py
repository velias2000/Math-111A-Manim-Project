

from manim import *
import numpy as np


class FloeMuseScore(Scene):
    def construct(self):

        
        #Visual Style
       
        BG = "#FAF9F5"
        INK = "#171717"
        STAFF = "#333333"
        BLUE = "#3478E5"
        MUTED = "#555555"

        self.camera.background_color = BG

        
        #Title
        
        title = Text(
            "Floe — Philip Glass",
            font_size=31,
            color=INK
        ).to_edge(UP, buff=0.25)

        subtitle = Text(
            "Repetition, Triplets, and Rhythmic Symmetry",
            font_size=19,
            color=MUTED
        ).next_to(title, DOWN, buff=0.12)

        self.play(FadeIn(title), FadeIn(subtitle))

       
        #Staff Line and Geometry
        
        SPACING = 0.18
        TOP = 1.15
        BOTTOM = -0.75

        LEFT = -5.6
        RIGHT = 5.6

        def staff(center):
            return VGroup(*[
                Line(
                    [LEFT, center + i * SPACING, 0],
                    [RIGHT, center + i * SPACING, 0],
                    color=STAFF,
                    stroke_width=1.4
                )
                for i in range(-2, 3)
            ])

        treble_staff = staff(TOP)
        bass_staff = staff(BOTTOM)

        self.play(
            Create(treble_staff),
            Create(bass_staff)
        )

       
        #Clefs and The Grand Staff
        
        treble_clef = Text(
            "𝄞",
            font_size=76,
            color=INK
        ).move_to([-5.25, TOP, 0])

        bass_clef = Text(
            "𝄢",
            font_size=65,
            color=INK
        ).move_to([-5.25, BOTTOM, 0])

        left_bar = Line(
            [LEFT, TOP + 2 * SPACING, 0],
            [LEFT, BOTTOM - 2 * SPACING, 0],
            color=INK,
            stroke_width=2.2
        )

        self.play(
            FadeIn(treble_clef),
            FadeIn(bass_clef),
            Create(left_bar)
        )

        
        #Note Heads and Stems
        #
        def head(x, y, filled=True, color=INK):
            return Ellipse(
                width=0.20,
                height=0.135,
                fill_color=color if filled else BG,
                fill_opacity=1,
                stroke_color=color,
                stroke_width=1.8
            ).rotate(-PI / 7).move_to([x, y, 0])

        
        #Note Stems and Beams
        
        def stem_note(x, y, up=True, color=INK):
            note = head(x, y, color=color)

            offset = 0.085 if up else -0.085
            direction = 1 if up else -1

            stem = Line(
                [x + offset, y, 0],
                [x + offset, y + direction * 0.52, 0],
                color=color,
                stroke_width=1.8
            )

            return VGroup(note, stem)

        # ----------------------------------
        # BEAMED TRIPLET
        # ----------------------------------
        def triplet(xs, ys):
            group = VGroup()
            beam_y = max(ys) + 0.43

            for x, y in zip(xs, ys):
                group.add(head(x, y))
                group.add(
                    Line(
                        [x + 0.085, y, 0],
                        [x + 0.085, beam_y, 0],
                        color=INK,
                        stroke_width=1.8
                    )
                )

            group.add(
                Line(
                    [xs[0] + 0.085, beam_y, 0],
                    [xs[-1] + 0.085, beam_y, 0],
                    color=INK,
                    stroke_width=4.5
                )
            )

            group.add(
                Text(
                    "3",
                    font_size=15,
                    color=INK
                ).move_to([
                    np.mean(xs),
                    beam_y + 0.18,
                    0
                ])
            )

            return group

        # ----------------------------------
        # CURVED SLURS
        # ----------------------------------
        def slur(x1, x2, y, depth=0.30):
            return CubicBezier(
                [x1, y, 0],
                [x1 + (x2 - x1) * 0.20, y - depth, 0],
                [x1 + (x2 - x1) * 0.80, y - depth, 0],
                [x2, y, 0],
                color=INK,
                stroke_width=2
            )

        # ----------------------------------
        # FOUR MEASURES
        # ----------------------------------
        measure_lefts = [-4.6, -2.15, 0.30, 2.75]
        measure_width = 2.45

        score = VGroup()
        barlines = VGroup()

        # Two bass figures per measure,
        # each containing six triplet notes.
        bass_pattern = [
            0.18, 0.00, -0.18,
            -0.36, -0.18, 0.00
        ]

        for m, x0 in enumerate(measure_lefts):

            # ----------------------------------
            # BASS STAFF
            # ----------------------------------
            for half in range(2):

                start = x0 + half * 1.18

                xs1 = [
                    start + 0.12,
                    start + 0.30,
                    start + 0.48
                ]

                xs2 = [
                    start + 0.68,
                    start + 0.86,
                    start + 1.04
                ]

                shift = -0.09 if m in [1, 2] else 0

                ys1 = [
                    BOTTOM + bass_pattern[i] + shift
                    for i in range(3)
                ]

                ys2 = [
                    BOTTOM + bass_pattern[i] + shift
                    for i in range(3, 6)
                ]

                score.add(triplet(xs1, ys1))
                score.add(triplet(xs2, ys2))

                score.add(
                    slur(
                        xs1[0],
                        xs2[-1],
                        BOTTOM - 0.27 + shift,
                        depth=0.32
                    )
                )

            # ----------------------------------
            # TREBLE STAFF
            # ----------------------------------
            if m < 3:
                # Repeated single notes followed
                # by two-note chords.
                for half in range(2):

                    x = x0 + half * 1.18 + 0.15
                    chord_x = x0 + half * 1.18 + 0.76

                    score.add(
                        stem_note(
                            x,
                            TOP - 0.27,
                            up=True
                        )
                    )

                    chord = VGroup(
                        head(chord_x, TOP - 0.09),
                        head(chord_x, TOP + 0.18),
                        Line(
                            [chord_x + 0.085, TOP - 0.09, 0],
                            [chord_x + 0.085, TOP + 0.68, 0],
                            color=INK,
                            stroke_width=1.8
                        )
                    )

                    score.add(chord)

                    score.add(
                        slur(
                            x,
                            chord_x,
                            TOP - 0.35,
                            depth=0.18
                        )
                    )

            else:
                # Last measure: rest and
                # longer chord values.
                rest = Text(
                    "𝄽",
                    font_size=38,
                    color=INK
                ).move_to([x0 + 0.25, TOP, 0])

                score.add(rest)

                for x, filled in [
                    (x0 + 1.0, False),
                    (x0 + 1.9, True)
                ]:
                    chord = VGroup(
                        head(x, TOP - 0.18, filled),
                        head(x, TOP + 0.18, filled),
                        Line(
                            [x + 0.085, TOP - 0.18, 0],
                            [x + 0.085, TOP + 0.60, 0],
                            color=INK,
                            stroke_width=1.8
                        )
                    )

                    score.add(chord)

            # ----------------------------------
            # MEASURE BARLINE
            # ----------------------------------
            bar_x = x0 + measure_width

            barlines.add(
                Line(
                    [bar_x, TOP + 2 * SPACING, 0],
                    [bar_x, BOTTOM - 2 * SPACING, 0],
                    color=INK,
                    stroke_width=1.6
                )
            )

        self.play(
            FadeIn(score),
            Create(barlines),
            run_time=2
        )

        # ----------------------------------
        # PLAYBACK CURSOR
        # ----------------------------------
        cursor = Rectangle(
            width=0.16,
            height=3.15,
            fill_color=BLUE,
            fill_opacity=0.23,
            stroke_width=0
        ).move_to([-4.5, 0.2, 0])

        self.add(cursor)

        self.play(
            cursor.animate.move_to([5.1, 0.2, 0]),
            run_time=9,
            rate_func=linear
        )

        self.play(FadeOut(cursor))

        # ----------------------------------
        # ABSTRACT ALGEBRA CONNECTION
        # ----------------------------------
        explanation = Text(
            "Repeated rhythmic patterns exhibit cyclic symmetry.",
            font_size=21,
            color=INK
        ).move_to([0, -2.65, 0])

        self.play(Write(explanation))
        self.wait(2)

        conclusion = Text(
            "Three rhythmic positions: Z₃",
            font_size=23,
            color=BLUE
        ).next_to(explanation, DOWN, buff=0.2)

        self.play(FadeIn(conclusion))
        self.wait(3)

