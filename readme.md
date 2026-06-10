# ✕ ○ Tic Tac Toe

A clean, two-player local Tic Tac Toe game built in Python with `tkinter`. No installs, no dependencies — just run and play.

---

## About the Project

Tic Tac Toe is deceptively simple on the surface, but building it from scratch is a genuinely satisfying exercise. This project covers the core pillars of any turn-based game: state management, win condition logic, player input handling, and real-time UI updates — all without a single external library.

The game features a custom dark navy and purple color scheme, with X rendered in slate purple and O in cyan-blue. Every detail — hover effects, winner highlighting, score persistence — is drawn manually on a `tkinter` canvas, making the codebase a clean and readable reference for anyone learning Python GUI development.

---

## Features

- 2-player local multiplayer — pass the keyboard and play
- Turn indicator that updates in real time, colored to match each player
- Win detection across all rows, columns, and diagonals
- Winning cells highlighted with a purple outline
- Draw detection when the board fills with no winner
- Persistent score tracker that survives across rounds
- Cell hover effect for clear interaction feedback
- New Game button to reset the board without losing scores
- Auto-centered window on any screen resolution

---

## Getting Started

### Prerequisites

Python 3.x only. `tkinter` is included in the standard library — no pip installs needed.

Verify it's available:

```bash
python3 -c "import tkinter; print('tkinter OK')"
```

If you're on Linux and it's missing:

```bash
sudo apt-get install python3-tk
```

### Running the Game

```bash
python3 TicTacToe.py
```

---

## How to Play

1. Player **X** always goes first
2. Click any empty cell to place your symbol
3. First to get three in a row — horizontally, vertically, or diagonally — wins
4. If all 9 cells fill with no winner, it's a draw
5. Hit **NEW GAME** to play again — scores carry over

---

## Project Structure

```
TicTacToe.py   # Main game file — everything lives here
README.md
```

The entire game is a single file organized as one class (`TicTacToe`) with clear method responsibilities: UI building, event handling, symbol drawing, win checking, and state resets.

---

## Color Palette

| Role             | Color                    |
| ---------------- | ------------------------ |
| Background       | `#1A1A2E` deep navy      |
| Board cells      | `#1F2B47` dark blue-gray |
| X symbol         | `#7B68EE` slate purple   |
| O symbol         | `#4FC3F7` cyan-blue      |
| Winner highlight | `#A78BFA` light purple   |

---

## What I Learned

- **Class-based tkinter apps:** wrapping the whole game in a class keeps state tidy and avoids global variables scattered across the file.
- **Canvas drawing primitives:** X and O are drawn manually using `create_line` and `create_oval` — no images or fonts, just coordinates and math.
- **Win logic:** checking all 8 winning combinations (3 rows, 3 columns, 2 diagonals) as a simple list of index triplets keeps the logic compact and easy to follow.
- **Hover effects:** tkinter's `<Motion>` event lets you track the mouse position and recolor cells on the fly, giving the UI a polished, interactive feel without any animation library.

---

## License

MIT — free to use, modify, and share.
