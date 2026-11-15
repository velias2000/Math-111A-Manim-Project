
from manim import *
import numpy as np
import wave
import os

class MusicalStaff(Scene):
    def construct(self):
        # Musical staff
        spacing = 0.25
        staff = VGroup(*[
            Line(
                LEFT * 5 + UP * (i * spacing),
                RIGHT * 5 + UP * (i * spacing),
                color=WHITE
            )
            for i in range(-2, 3)
        ])

        title = Text("C Major Scale", font_size=40)
        title.to_edge(UP)

        self.play(Write(title), Create(staff))

        # Treble clef (requires a music font)
        clef = Text("𝄞", font="Bravura", font_size=95)
        clef.move_to(LEFT * 4.4 + UP * 0.1)
        self.play(FadeIn(clef))

        # Notes: name, frequency, staff position
        # Bottom line E4 is position 0
        notes = [
            ("C4", 261.63, -2),
            ("D4", 293.66, -1),
            ("E4", 329.63, 0),
            ("F4", 349.23, 1),
            ("G4", 392.00, 2),
            ("A4", 440.00, 3),
            ("B4", 493.88, 4),
            ("C5", 523.25, 5),
        ]

        os.makedirs("sounds", exist_ok=True)
        sample_rate = 44100
        duration = 0.6

        for i, (name, freq, pos) in enumerate(notes):
            x = -3.2 + i * 0.85
            y = -0.5 + pos * (spacing / 2)

            # Note head
            head = Ellipse(
                width=0.3,
                height=0.2,
                color=WHITE,
                fill_opacity=1
            )
            head.rotate(-PI / 6)
            head.move_to([x, y, 0])

            # Stem
            stem = Line(
                [x + 0.13, y, 0],
                [x + 0.13, y + 0.75, 0],
                color=WHITE
            )

            note = VGroup(head, stem)

            # Ledger line for middle C
            if name == "C4":
                ledger = Line(
                    [x - 0.25, y, 0],
                    [x + 0.25, y, 0],
                    color=WHITE
                )
                note.add(ledger)

            # Generate audio
            t = np.linspace(
                0, duration,
                int(sample_rate * duration),
                endpoint=False
            )

            audio = 0.3 * np.sin(2 * PI * freq * t)

            fade = min(1000, len(audio) // 2)
            envelope = np.ones(len(audio))
            envelope[:fade] = np.linspace(0, 1, fade)
            envelope[-fade:] = np.linspace(1, 0, fade)
            audio *= envelope

            filename = f"sounds/scale_{i}.wav"

            with wave.open(filename, "w") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(sample_rate)
                wav.writeframes(
                    (audio * 32767).astype(np.int16).tobytes()
                )

            self.add_sound(filename)
            self.play(FadeIn(note), run_time=duration)

        self.wait(2)



