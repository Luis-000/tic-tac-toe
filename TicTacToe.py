from tkinter import *

# ── Constants ─────────────────────────────────────────────────
WINDOW_BG    = "#1A1A2E"   # deep dark navy
BOARD_BG     = "#16213E"   # slightly lighter navy for board area
CELL_BG      = "#1F2B47"   # cell background
CELL_HOVER   = "#263552"   # cell hover highlight
LINE_COLOR   = "#2E3F6F"   # grid line color
X_COLOR      = "#7B68EE"   # medium slate purple for X
O_COLOR      = "#4FC3F7"   # light cyan-blue for O
TEXT_COLOR   = "#C8D0E8"   # soft gray-blue text
DIM_COLOR    = "#4A5580"   # dimmed text
WIN_COLOR    = "#A78BFA"   # purple highlight for winner
PANEL_COLOR  = "#12111F"   # top/bottom panel

CELL_SIZE    = 160
PADDING      = 14
BOARD_SIZE   = CELL_SIZE * 3 + PADDING * 2


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)
        self.root.configure(bg=PANEL_COLOR)

        self.current_player = "X"
        self.board = [""] * 9
        self.game_active = True
        self.score = {"X": 0, "O": 0}
        self.last_winner = None

        self._build_ui()
        self._center_window()

    def _build_ui(self):
        # ── Top panel ──────────────────────────────────────────
        top = Frame(self.root, bg=PANEL_COLOR, pady=18)
        top.pack(fill=X)

        self.title_label = Label(
            top, text="TIC TAC TOE",
            font=("Helvetica", 13, "bold"),
            bg=PANEL_COLOR, fg=DIM_COLOR
        )
        self.title_label.pack()

        # Turn indicator
        self.turn_frame = Frame(top, bg=PANEL_COLOR)
        self.turn_frame.pack(pady=(10, 0))

        self.turn_prefix = Label(
            self.turn_frame, text="Player",
            font=("Helvetica", 15), bg=PANEL_COLOR, fg=DIM_COLOR
        )
        self.turn_prefix.pack(side=LEFT)

        self.turn_player = Label(
            self.turn_frame, text="  X",
            font=("Helvetica", 15, "bold"), bg=PANEL_COLOR, fg=X_COLOR
        )
        self.turn_player.pack(side=LEFT)

        self.turn_suffix = Label(
            self.turn_frame, text="'s turn",
            font=("Helvetica", 15), bg=PANEL_COLOR, fg=DIM_COLOR
        )
        self.turn_suffix.pack(side=LEFT)

        # Separator
        Frame(self.root, height=1, bg=LINE_COLOR).pack(fill=X)

        # ── Canvas board ───────────────────────────────────────
        self.canvas = Canvas(
            self.root,
            width=BOARD_SIZE, height=BOARD_SIZE,
            bg=BOARD_BG, highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.bind("<Motion>",        self._on_hover)
        self.canvas.bind("<Leave>",         self._on_leave)
        self.canvas.bind("<Button-1>",      self._on_click)

        self._draw_board()

        # Separator
        Frame(self.root, height=1, bg=LINE_COLOR).pack(fill=X)

        # ── Bottom panel ───────────────────────────────────────
        bottom = Frame(self.root, bg=PANEL_COLOR, pady=14)
        bottom.pack(fill=X)

        # Score display
        score_frame = Frame(bottom, bg=PANEL_COLOR)
        score_frame.pack()

        self._score_block(score_frame, "X", X_COLOR, 0)
        Label(score_frame, text="  —  ", font=("Helvetica", 16),
              bg=PANEL_COLOR, fg=DIM_COLOR).grid(row=0, column=1, rowspan=2)
        self._score_block(score_frame, "O", O_COLOR, 2)

        # Restart button
        self.restart_btn = Button(
            bottom, text="NEW GAME",
            font=("Helvetica", 10, "bold"),
            bg=CELL_BG, fg=DIM_COLOR,
            activebackground=CELL_HOVER, activeforeground=TEXT_COLOR,
            relief=FLAT, padx=20, pady=8, cursor="hand2",
            command=self.restart
        )
        self.restart_btn.pack(pady=(12, 0))

    def _score_block(self, parent, player, color, col):
        Label(parent, text=player,
              font=("Helvetica", 13, "bold"),
              bg=PANEL_COLOR, fg=color).grid(row=0, column=col, padx=20)
        lbl = Label(parent, text="0",
                    font=("Helvetica", 26, "bold"),
                    bg=PANEL_COLOR, fg=color)
        lbl.grid(row=1, column=col, padx=20)
        if player == "X":
            self.score_x_label = lbl
        else:
            self.score_o_label = lbl

    def _draw_board(self):
        self.canvas.delete("all")
        self.cells = []

        for i in range(9):
            row, col = divmod(i, 3)
            x1 = PADDING + col * CELL_SIZE
            y1 = PADDING + row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            rect = self.canvas.create_rectangle(
                x1 + 4, y1 + 4, x2 - 4, y2 - 4,
                fill=CELL_BG, outline=LINE_COLOR, width=1,
                tags=(f"cell_{i}", "cell")
            )
            self.cells.append(rect)

    def _cell_at(self, x, y):
        col = int((x - PADDING) // CELL_SIZE)
        row = int((y - PADDING) // CELL_SIZE)
        if 0 <= col <= 2 and 0 <= row <= 2:
            return row * 3 + col
        return None

    def _on_hover(self, event):
        if not self.game_active:
            return
        idx = self._cell_at(event.x, event.y)
        for i, rect in enumerate(self.cells):
            if i == idx and self.board[i] == "":
                self.canvas.itemconfig(rect, fill=CELL_HOVER)
            elif self.board[i] == "":
                self.canvas.itemconfig(rect, fill=CELL_BG)

    def _on_leave(self, event):
        for i, rect in enumerate(self.cells):
            if self.board[i] == "":
                self.canvas.itemconfig(rect, fill=CELL_BG)

    def _on_click(self, event):
        if not self.game_active:
            return
        idx = self._cell_at(event.x, event.y)
        if idx is None or self.board[idx] != "":
            return

        self.board[idx] = self.current_player
        self._draw_symbol(idx, self.current_player)

        winner_line = self._check_winner()
        if winner_line:
            self.game_active = False
            self.last_winner = self.current_player
            self._highlight_winner(winner_line)
            self._show_result(f"Player {self.current_player} wins!")
            self.score[self.current_player] += 1
            self.score_x_label.config(text=str(self.score["X"]))
            self.score_o_label.config(text=str(self.score["O"]))
        elif "" not in self.board:
            self.game_active = False
            self._show_result("It's a draw!")
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            color = X_COLOR if self.current_player == "X" else O_COLOR
            self.turn_player.config(text=f"  {self.current_player}", fg=color)

    def _draw_symbol(self, idx, player):
        row, col = divmod(idx, 3)
        x1 = PADDING + col * CELL_SIZE
        y1 = PADDING + row * CELL_SIZE
        cx = x1 + CELL_SIZE / 2
        cy = y1 + CELL_SIZE / 2
        m  = 38   # margin from cell edge

        if player == "X":
            x1e = x1 + m + 4
            y1e = y1 + m + 4
            x2e = x1 + CELL_SIZE - m - 4
            y2e = y1 + CELL_SIZE - m - 4
            self.canvas.create_line(x1e, y1e, x2e, y2e,
                fill=X_COLOR, width=7, capstyle=ROUND, tags=f"sym_{idx}")
            self.canvas.create_line(x2e, y1e, x1e, y2e,
                fill=X_COLOR, width=7, capstyle=ROUND, tags=f"sym_{idx}")
        else:
            r = CELL_SIZE / 2 - m
            self.canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                outline=O_COLOR, width=7, tags=f"sym_{idx}"
            )

    def _check_winner(self):
        wins = [
            (0,1,2),(3,4,5),(6,7,8),  # rows
            (0,3,6),(1,4,7),(2,5,8),  # cols
            (0,4,8),(2,4,6)           # diagonals
        ]
        for a, b, c in wins:
            if self.board[a] == self.board[b] == self.board[c] != "":
                return (a, b, c)
        return None

    def _highlight_winner(self, line):
        for idx in line:
            self.canvas.itemconfig(self.cells[idx], fill="#29305A", outline=WIN_COLOR)

    def _show_result(self, message):
        color = WIN_COLOR if "wins" in message else DIM_COLOR
        self.turn_prefix.config(text="")
        self.turn_suffix.config(text="")
        self.turn_player.config(text=message, fg=color,
                                font=("Helvetica", 15, "bold"))

    def restart(self):
        self.board = [""] * 9
        self.game_active = True
        self.current_player = self.last_winner if self.last_winner else "X"
        self.last_winner = None

        color = X_COLOR if self.current_player == "X" else O_COLOR
        self.turn_prefix.config(text="Player", font=("Helvetica", 15))
        self.turn_player.config(text=f"  {self.current_player}", fg=color,
                                font=("Helvetica", 15, "bold"))
        self.turn_suffix.config(text="'s turn")
        self._draw_board()

    def _center_window(self):
        self.root.update()
        ww = self.root.winfo_width()
        wh = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x  = sw // 2 - ww // 2
        y  = sh // 2 - wh // 2
        self.root.geometry(f"{ww}x{wh}+{x}+{y}")


if __name__ == "__main__":
    root = Tk()
    TicTacToe(root)
    root.mainloop()