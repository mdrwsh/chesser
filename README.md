# Chesser

## Overview

Chesser is designed to play chess autonomously on a graphical chessboard interface. It captures the screen to recognize the board state, detects the opponent's moves by analyzing frame differences, and makes moves using a chess engine. The bot can play as either white or black.

## Features

- **Screen Capture**: Captures the chessboard from the screen.
- **Move Detection**: Detects the opponent's moves by comparing frame differences.
- **Autonomous Play**: Plays the game autonomously using a chess engine.
- **Castling and Promotion**: Handles castling and pawn promotion.
- **User Interaction**: Allows the user to click on the top-left and bottom-right corners of the chessboard to define the board area.

## Requirements

- Python 3.x
- OpenCV
- NumPy
- MSS
- PyAutoGUI
- Python Chess
- pywin32 (for Windows key state handling)

## Installation

1. Install Python 3.x from [python.org](https://www.python.org/).
2. Install the required libraries:
   ```bash
   pip install opencv-python-headless numpy mss pyautogui python-chess pywin32
   ```

## Usage

1. Specify your chess engine executable (e.g., `stockfish.exe`) in chesser.py
2. Run the script:
   ```bash
   python chesser.py
   ```
3. Click on the top-left and bottom-right corners of the chessboard to define the board area.
4. Choose whether you want to play as white or black.
5. The bot will start playing the game autonomously.

### Main Program

1. **Initialize the board area**:
   - The user clicks on the top-left and bottom-right corners of the chessboard to define the board area.
2. **Determine playing side**:
   - The user inputs whether they are playing as white or black.
3. **Start the chess engine**:
   - The script starts the chess engine and initializes the chessboard.
4. **Main game loop**:
   - The bot makes moves using the chess engine if it is the bot's turn.
   - The bot waits and detects the opponent's move if it is the opponent's turn.

### Example Usage

To use the bot, simply run the script and follow the prompts to define the board area and select your playing side. The bot will handle the rest.

```bash
python chess_bot.py
```

## Notes

- This script requires a graphical chessboard interface to interact with.
- The chess engine executable can be specified in chesser.py.
- The bot uses frame differences to detect moves, so it may not work well with animations or highly dynamic interfaces.
- Only work in Windows currently.
- Please report any issue, PR will be ignored.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This project uses the [python-chess](https://python-chess.readthedocs.io/en/latest/) library for chess move generation and validation.
- This project uses the [MSS](https://python-mss.readthedocs.io/) library for screen capturing.
- This project uses the [PyAutoGUI](https://pyautogui.readthedocs.io/) library for automating mouse movements and clicks.
