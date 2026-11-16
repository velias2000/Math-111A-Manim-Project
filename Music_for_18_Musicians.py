
import math
import wave
import struct
import random
from pathlib import Path

from manim import *


# We configure the settings


config.background_color = "#111318"

WHITE_TEXT = "#F5F5F5"
ACCENT_A = "#59C3C3"
ACCENT_B = "#F4B860"
REST_COLOR = "#454B55"
CURSOR_COLOR = "#B7E4C7"

BPM = 120
PULSES = 12
SECONDS_PER_PULSE = 60 / BPM

# Original illustrative pattern, not Reich's score.
PATTERN = [1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1]

AUDIO_DIR = Path(__file__).resolve().parent / "sounds"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_RATE = 44100



# AUDIO GENERATION

def create_clap_samples(duration=0.12, seed=42):
    """Generate a short synthetic handclap."""

    rng = random.Random(seed)
    count = int(duration * SAMPLE_RATE)
    samples = []

    previous_noise = 0.0

    for i in range(count):
        t = i / SAMPLE_RATE

        noise = rng.uniform(-1, 1)

        # High-pass-like noise for a sharp clap.
        filtered = noise - 0.85 * previous_noise
        previous_noise = noise

        envelope = math.exp(-35 * t)

        # Several tiny transients imitate hand contact.
        transient = (
            math.exp(-900 * t)
            + 0.65 * math.exp(-900 * abs(t - 0.012))
            + 0.4 * math.exp(-900 * abs(t - 0.024))
        )

        value = filtered * envelope * (0.4 + transient)
        samples.append(value)

    peak = max(max(abs(s) for s in samples), 1e-9)
    return [s / peak for s in samples]


def create_clapping_audio(filename, pattern_a, pattern_b):
    """Create stereo audio for two clapping performers."""

    total_duration = PULSES * SECONDS_PER_PULSE
    count = int(total_duration * SAMPLE_RATE)

    left = [0.0] * count
    right = [0.0] * count

    clap_a = create_clap_samples(seed=10)
    clap_b = create_clap_samples(seed=25)

    for pulse in range(PULSES):
        start = int(
            pulse * SECONDS_PER_PULSE * SAMPLE_RATE
        )

        if pattern_a[pulse]:
            for j, sample in enumerate(clap_a):
                if start + j < count:
                    left[start + j] += 0.7 * sample
                    right[start + j] += 0.2 * sample

        if pattern_b[pulse]:
            for j, sample in enumerate(clap_b):
                if start + j < count:
                    left[start + j] += 0.2 * sample
                    right[start + j] += 0.7 * sample

    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)

    with wave.open(str(filename), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)

        frames = bytearray()

        for l, r in zip(left, right):
            l = max(-1, min(1, l))
            r = max(-1, min(1, r))

            frames.extend(
                struct.pack(
                    "<hh",
                    int(l * 32767),
                    int(r * 32767),
                )
            )

        wav.writeframes(frames)



# MAIN MANIM SCENE


class ClappingMusic(Scene):

    def construct(self):

        
        # TITLE
        

        title = Text(
            "CLAPPING MUSIC",
            font_size=46,
            weight=BOLD,
            color=WHITE_TEXT,
        )

        subtitle = Text(
            "A Visualization of Rhythmic Phasing",
            font_size=23,
            color=GRAY_B,
        )

        heading = VGroup(
            title, subtitle
        ).arrange(DOWN, buff=0.2)

        heading.to_edge(UP, buff=0.4)

        self.add(heading)

        
        # RHYTHM GRID
        

        grid_spacing = 0.78
        start_x = -4.3

        performer_a_y = 0.9
        performer_b_y = -0.7

        label_a = Text(
            "Performer A",
            font_size=23,
            color=ACCENT_A,
        ).move_to([-5.7, performer_a_y, 0])

        label_b = Text(
            "Performer B",
            font_size=23,
            color=ACCENT_B,
        ).move_to([-5.7, performer_b_y, 0])

        self.add(label_a, label_b)

        row_a = VGroup()
        row_b = VGroup()

        for i in range(PULSES):
            x = start_x + i * grid_spacing

            dot_a = Circle(
                radius=0.22,
                stroke_color=ACCENT_A,
                stroke_width=2,
                fill_color=(
                    ACCENT_A if PATTERN[i] else REST_COLOR
                ),
                fill_opacity=1,
            ).move_to([x, performer_a_y, 0])

            dot_b = Circle(
                radius=0.22,
                stroke_color=ACCENT_B,
                stroke_width=2,
                fill_color=(
                    ACCENT_B if PATTERN[i] else REST_COLOR
                ),
                fill_opacity=1,
            ).move_to([x, performer_b_y, 0])

            row_a.add(dot_a)
            row_b.add(dot_b)

        self.add(row_a, row_b)

        # PLAYBACK CURSOR
        

        cursor = Line(
            [start_x, -1.25, 0],
            [start_x, 1.45, 0],
            color=CURSOR_COLOR,
            stroke_width=3,
        )

        self.add(cursor)

        shift_label = Text(
            "Shift: 0 pulses",
            font_size=26,
            color=WHITE_TEXT,
        ).move_to([0, -2.15, 0])

        self.add(shift_label)


        # 12 PHASES
        

        for shift in range(PULSES):

            # Performer B shifts cyclically.
            shifted_pattern = [
                PATTERN[(i - shift) % PULSES]
                for i in range(PULSES)
            ]

            new_row_b = VGroup()

            for i in range(PULSES):
                x = start_x + i * grid_spacing

                dot = Circle(
                    radius=0.22,
                    stroke_color=ACCENT_B,
                    stroke_width=2,
                    fill_color=(
                        ACCENT_B
                        if shifted_pattern[i]
                        else REST_COLOR
                    ),
                    fill_opacity=1,
                ).move_to([x, performer_b_y, 0])

                new_row_b.add(dot)

            new_label = Text(
                f"Shift: {shift} pulses",
                font_size=26,
                color=WHITE_TEXT,
            ).move_to(shift_label)

            self.play(
                Transform(row_b, new_row_b),
                Transform(shift_label, new_label),
                run_time=0.35,
            )

            audio_path = (
                AUDIO_DIR / f"clapping_phase_{shift}.wav"
            )

            create_clapping_audio(
                audio_path,
                PATTERN,
                shifted_pattern,
            )

            self.add_sound(str(audio_path))

            # One full 12-pulse rhythmic cycle.
            for pulse in range(PULSES):

                x = start_x + pulse * grid_spacing

                cursor.move_to([
                    x,
                    (performer_a_y + performer_b_y) / 2,
                    0,
                ])

                active = []

                if PATTERN[pulse]:
                    active.append(row_a[pulse])

                if shifted_pattern[pulse]:
                    active.append(row_b[pulse])

                if active:
                    self.play(
                        *[
                            dot.animate.scale(1.22)
                            for dot in active
                        ],
                        run_time=0.12,
                    )

                    self.play(
                        *[
                            dot.animate.scale(1 / 1.22)
                            for dot in active
                        ],
                        run_time=0.12,
                    )

                self.wait(
                    SECONDS_PER_PULSE - 0.24
                    if active
                    else SECONDS_PER_PULSE
                )


        # END


        ending = Text(
            "Rhythm Through Cyclic Permutation",
            font_size=28,
            color=CURSOR_COLOR,
        ).to_edge(DOWN, buff=0.45)

        self.play(FadeIn(ending), run_time=0.8)
        self.wait(1.5)


