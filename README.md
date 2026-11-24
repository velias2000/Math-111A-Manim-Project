# Guideline of Using the Materials in This Repo

## Piano Phase

In the `piano-phase` folder:

- **`PianoPhase.mp4`**: The finished video of the Piano Phase animation, with sound. You can download and play it directly, with no setup needed.
- **`piano_phase.py`**: The Python code that generates the animation, written with [Manim](https://www.manim.community/).
- **`piano_phase.wav`**: The audio track used in the video.

## Floe

In the `Floe` folder:

- **`CyclicTransformations.mp4`:** Video demonstrating the animation for how cyclic groups are positioned on a musical staff.
- **`Floe.py`:** The Python code that generates the animation, written with Manim.

## Viewing the Animation Yourself

To run and view the animations, you'll need Manim (and the Manim Sideview extension if you're using VS Code).

1. **Install Manim:** Follow the official installation guide: https://docs.manim.community/en/stable/installation.html
2. **Install VS Code:** If you don't already have it, install at https://code.visualstudio.com/download
3. **Install the Manim Sideview extension:** In VS Code, open the Extensions tab, search for "Manim Sideview", and install it
4. **Run the Piano Phase animation:** In VS Code, open `piano_phase.py`, use the Manim Sideview panel to render and preview the animation next to your code. Or, you can run the following in your terminal:
```bash
manim -pqh piano_phase.py PianoPhase
```
5. **Run the Floe animation:** In VS Code, open `Floe.py`, use the Manim Sideview panel to render and preview the animation next to your code.
