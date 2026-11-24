from manim import *
import numpy as np
import wave
import bisect


# 12-note pattern: E4 F#4 B4 C#5 D5 F#4 E4 C#5 B4 F#4 D5 C#5
PATTERN_MIDI = [64, 66, 71, 73, 74, 66, 64, 73, 71, 66, 74, 73]
# Diatonic steps above E4 (bottom line of the treble staff), for vertical placement
PATTERN_STEP = [0, 1, 4, 5, 6, 1, 0, 5, 4, 1, 6, 5]
PATTERN_SHARP = [False, True, False, True, False, True, False, True, False, True, False, True]
N = len(PATTERN_MIDI)

# timing
D = 0.125          # seconds per 16th note (Reich's tempo is ~0.104)
HOLD_REPS = 4      # repetitions in lock-step before each phase shift
GLIDE_REPS = 2     # repetitions over which Piano 2 gains one 16th

HOLD_T = HOLD_REPS * N * D
GLIDE_T = GLIDE_REPS * N * D
SECTION_T = HOLD_T + GLIDE_T
TOTAL_T = N * SECTION_T + HOLD_T   # 12 shifts, then a final unison hold


def phi(t):
    # How many 16th notes Piano 2 is ahead of Piano 1 at time t.
    k = min(int(t // SECTION_T), N)
    if k >= N:
        return float(N)
    local = t - k * SECTION_T
    return k + float(np.clip((local - HOLD_T) / GLIDE_T, 0, 1))


def compute_onsets():
    # Returns (onset_times, note_indices) for each piano.
    # Piano 1: steady
    n1 = int(TOTAL_T / D)
    on1 = [i * D for i in range(n1)]
    idx1 = [i % N for i in range(n1)]

    # Piano 2: position in 16th-note units = t/D + phi(t); an onset occurs at each integer crossing
    ts = np.arange(0, TOTAL_T, 0.0005)
    pos = ts / D + np.array([phi(t) for t in ts])
    fl = np.floor(pos).astype(int)
    change = np.nonzero(np.diff(fl))[0] + 1
    on2 = [0.0] + [float(ts[i]) for i in change]
    idx2 = [0] + [int(fl[i]) % N for i in change]
    return (on1, idx1), (on2, idx2)


# ---------------- Audio synthesis ----------------
def synth_note(midi, dur=0.6, sr=44100):
    f = 440.0 * 2 ** ((midi - 69) / 12)
    t = np.linspace(0, dur, int(sr * dur), endpoint=False)
    y = sum((1 / k) * np.sin(2 * np.pi * f * k * t) for k in range(1, 6))
    env = np.exp(-t * 7) * np.minimum(1, t / 0.004)
    return y * env


def render_audio(p1, p2, path="piano_phase.wav", sr=44100):
    total = int((TOTAL_T + 1.0) * sr)
    buf = np.zeros((total, 2))
    for (onsets, idxs), pan in ((p1, 0.25), (p2, 0.75)):  # Piano 1 left, Piano 2 right
        gl, gr = np.cos(pan * np.pi / 2), np.sin(pan * np.pi / 2)
        for on, i in zip(onsets, idxs):
            s = synth_note(PATTERN_MIDI[i])
            a = int(on * sr)
            b = min(a + len(s), total)
            buf[a:b, 0] += s[: b - a] * gl
            buf[a:b, 1] += s[: b - a] * gr
    buf /= np.max(np.abs(buf)) * 1.1
    data = (buf * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(data.tobytes())
    return path

class PlayHighlight(Animation):
    """Recolors the currently sounding note on each staff every frame."""
    def __init__(self, mobject, heads1, heads2, p1, p2, hl1, hl2, **kwargs):
        self.tracks = [
            (heads1, p1[0], p1[1], hl1),
            (heads2, p2[0], p2[1], hl2),
        ]
        self.cur = [-2, -2]
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        t = alpha * TOTAL_T
        for k, (heads, onsets, idxs, color) in enumerate(self.tracks):
            i = bisect.bisect_right(onsets, t) - 1
            cur = idxs[i] if i >= 0 else -1
            if cur == self.cur[k]:
                continue
            self.cur[k] = cur
            for j, h in enumerate(heads):
                c = color if j == cur else WHITE
                h.set_fill(c, 1)
                h.set_stroke(c)

# ---------------- Scene ----------------
class PianoPhase(Scene):
    LINE_GAP = 0.25
    X0 = -5.0
    DX = 0.85
    HL1 = YELLOW
    HL2 = "#4FC3F7"

    def build_staff(self, y_center, label):
        g = LINE_GAP = self.LINE_GAP
        lines = VGroup(*[
            Line(LEFT * 6.2, RIGHT * 6.2, stroke_width=1.5, color=GREY_B).move_to(
                [0, y_center + (i - 2) * g, 0])
            for i in range(5)
        ])
        bottom = y_center - 2 * g
        top = y_center + 2 * g
        # barlines
        bars = VGroup(
            Line([-6.2, bottom, 0], [-6.2, top, 0], stroke_width=2, color=GREY_B),
            Line([6.2, bottom, 0], [6.2, top, 0], stroke_width=2, color=GREY_B),
        )
        lab = Text(label, font_size=24).next_to(lines, UP, buff=0.9).align_to(lines, LEFT)
        # clef substitute: a small "G" is avoided; just label the staff
        heads, extras = [], VGroup()
        xs = [self.X0 + i * self.DX + (0.15 if False else 0) for i in range(N)]
        for i in range(N):
            x = xs[i]
            y = bottom + PATTERN_STEP[i] * g / 2
            head = Ellipse(width=0.36, height=0.25, color=WHITE).set_fill(WHITE, 1)
            head.rotate(20 * DEGREES).move_to([x, y, 0])
            heads.append(head)
            if PATTERN_SHARP[i]:
                extras.add(Text("♯", font_size=26).move_to([x - 0.33, y, 0]))
        # stems + beams in groups of 4 sixteenths
        beam_y = top + 0.55
        for grp in range(N // 4):
            sx = []
            for i in range(grp * 4, grp * 4 + 4):
                x = xs[i] + 0.17
                y = bottom + PATTERN_STEP[i] * g / 2
                extras.add(Line([x, y, 0], [x, beam_y, 0], stroke_width=2))
                sx.append(x)
            for off in (0, 0.1):
                extras.add(Line([sx[0], beam_y - off, 0], [sx[-1], beam_y - off, 0],
                                stroke_width=6))
        return VGroup(lines, bars, lab, extras), heads

    def construct(self):
        p1, p2 = compute_onsets()
        wav = render_audio(p1, p2)

        title = Text("Piano Phase — Steve Reich (1976)", font_size=30).to_edge(UP, buff=0.3)
        staff1, heads1 = self.build_staff(1.4, "Piano 1")
        staff2, heads2 = self.build_staff(-1.5, "Piano 2")
        noteheads = VGroup(*heads1, *heads2)
        self.add(title, staff1, staff2, noteheads)

        tracker = ValueTracker(0)
        self.add(tracker)

        phase_label = always_redraw(lambda: Text(
            f"Phase offset: {phi(tracker.get_value()):.2f} / 12 sixteenths",
            font_size=24).to_edge(DOWN, buff=0.5))
        self.add(phase_label)

        highlight = PlayHighlight(
            noteheads, heads1, heads2, p1, p2, self.HL1, self.HL2,
            run_time=TOTAL_T, rate_func=linear)

        self.add_sound(wav)
        self.play(
            highlight,
            tracker.animate.set_value(TOTAL_T),
            run_time=TOTAL_T,
            rate_func=linear,
        )
        self.wait(1)