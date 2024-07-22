import cv2
import time
import chess
import chess.engine
import win32api
import pyautogui
import numpy as np
from mss import mss
from random import randint

def normalise(x):
    if x == 1: return 0
    if x == -127: return 128
    return x

def frame_difference(frame1, frame2, diff_threshold=100, change_threshold=10000):
    diff = cv2.absdiff(cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY), cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY))
    _, thresh = cv2.threshold(diff, diff_threshold, 255, cv2.THRESH_BINARY)
    change = np.sum(thresh)
    return change

def get_board():
    with mss() as sct:
        img = np.array(sct.grab(sct.monitors[0]))
    board = img[cord[0][1]:cord[1][1], cord[0][0]:cord[1][0]]
    return board
    # piece = board[0:int(sx), 0:int(sy)]

def get_pieces(squares):
    pieces = []
    for square in squares:
        p = board.piece_at(chess.parse_square(square))
        if p:
            pieces.append(p.symbol().lower())
    return pieces

def possible_moves(squares):
    moves = []
    candid = []
    for sq in squares:
        for eq in squares:
            if sq != eq:
                candid.append(sq+eq)
    for move in candid:
        p = board.piece_at(chess.Move.from_uci(move).from_square)
        if p and p.piece_type == 1 and move[3] in '18':
            for l in 'qnrb':
                moves.append(move+l)
        else: moves.append(move)
    return moves

def find_movement(frame1, frame2):
    rank = "87654321" if playing_as else "12345678"
    file = "abcdefgh" if playing_as else "hgfedcba"
    squares = []
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    for y in range(8):
        for x in range(8):
            s1 = frame1[int(sy*y):int(sy*y+sy), int(sx*x):int(sx*x+sx)]
            s2 = frame2[int(sy*y):int(sy*y+sy), int(sx*x):int(sx*x+sx)]
            diff = np.sum(cv2.absdiff(s1, s2))
            if diff > 0:
                squares.append((file[x]+rank[y], diff))
    squares = [i[0] for i in sorted(squares, key=lambda tup: tup[1], reverse=True)][:4]
    pieces = get_pieces(squares)
    moves = possible_moves(squares)
    print(moves)
    if "k" in pieces and "r" in pieces:
        print("castling move")
        for move in moves:
            p = board.piece_at(chess.parse_square(move[:2]))
            if p and p.symbol() in ["k","K"] and chess.Move.from_uci(move) in board.legal_moves:
                if abs(file.index(move[0])-file.index(move[2])) > 1:
                    return move
    for move in moves:
        if chess.Move.from_uci(move) in board.legal_moves:
            p = board.piece_at(chess.Move.from_uci(move).from_square)
            if p and p.piece_type == 1 and move[3] in '18':
                return move + 'q' # TODO: opponent promote to what
            else:
                return move
    if moves == []: return wait_move()
    return None

def wait_move():
    board = get_board()
    prev_board = board[:]
    clock = 0
    timeout = time.time()
    while True:
        current_board = get_board()
        if frame_difference(prev_board, current_board) < 100:
            clock += 1
        else: clock = 0
        if clock > 3:
            # print(frame_difference(current_board, board))
            if frame_difference(current_board, board) > 100_000:
                break
            else:
                clock = 0
                timeout += 1
        if timeout - time.time() > 100: # no move after n second
            print("Timeout, exiting...")
            engine.quit()
            exit()
        prev_board = current_board[:]
        time.sleep(0.01)
    return find_movement(current_board, board)

def make_move(move):
    rank = "87654321" if playing_as else "12345678"
    file = "abcdefgh" if playing_as else "hgfedcba"
    promote = "qkrb"
    mfrom = (ax + (file.index(move[0])+.5)*sx, ay + (rank.index(move[1])+.5)*sy)
    mto = (ax + (file.index(move[2])+.5)*sx, ay + (rank.index(move[3])+.5)*sy)
    pyautogui.moveTo(mfrom)
    time.sleep(0.05)
    pyautogui.click()
    time.sleep(0.05)
    pyautogui.moveTo(mto)
    time.sleep(0.05)
    pyautogui.click()
    time.sleep(0.01)
    if len(move) == 5:
        print("promoting")
        promoting = promote.index(move[4])
        pyautogui.move((0, sx*promoting))
        time.sleep(0.05)

print("Click top-left and bottom-right of the chessboard")

cord = []
state = normalise(win32api.GetKeyState(0x01))
while len(cord) < 2:
    state = normalise(state)
    current = normalise(win32api.GetKeyState(0x01))
    if state != current:
        state = current
        if state != 0:
            cord.append(pyautogui.position())
    time.sleep(0.05)

x = cord[0][0] - cord[1][0]
y = cord[0][1] - cord[1][1]
ax, ay = cord[0]
sx = abs(cord[0][0] - cord[1][0])/8
sy = abs(cord[0][1] - cord[1][1])/8

playing_as = None
player = input("Got it, playing white or black?[w/b]")
if player == "w":
    playing_as = True
elif player == "b":
    playing_as = False
else:
    print("Bad input, exiting...")
    exit()
engine = chess.engine.SimpleEngine.popen_uci("obsidian.exe")
board = chess.Board()

if board.turn == playing_as:
    move = "e2e4"
else:
    move = input("White first move:")

time.sleep(0.1)
# print("Autoplay in 3 seconds...")
# time.sleep(3)

if board.turn == playing_as:
    make_move(move)
board.push(chess.Move.from_uci(move))
time.sleep(0.2)

while not board.is_game_over():
    if board.turn == playing_as:
        # if len(board.move_stack) >= 10:
        #     time.sleep(randint(0, 4))
        result = engine.play(board, chess.engine.Limit(depth=5))
        print(board.fen(), result.move)
        make_move(result.move.uci())
        board.push(result.move)
    else:
        move = wait_move()
        if move is None: engine.quit()
        print(board.fen(), move)
        board.push(chess.Move.from_uci(move))
engine.quit()

# import cv2
# import numpy as np

# def detect_chessboard(image_path):
#     # Load the image
#     image = cv2.imread(image_path)
    
#     if image is None:
#         print("Error: Image not found")
#         return None, None
    
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Define the chessboard size (number of inner corners per chessboard row and column)
#     chessboard_size = (7, 7)  # Change this based on the chessboard you are detecting
    
#     # Find the chessboard corners
#     ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    
#     if ret:
#         # Refine the corner locations
#         corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), 
#                                    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        
#         # Draw and display the corners (optional)
#         cv2.drawChessboardCorners(image, chessboard_size, corners, ret)
#         cv2.imshow('Detected Chessboard', image)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
        
#         # Get the top-left and bottom-right coordinates
#         top_left = tuple(corners[0][0])
#         bottom_right = tuple(corners[-1][0])
        
#         return top_left, bottom_right
#     else:
#         print("Chessboard not detected")
#         return None, None

# # Test the function
# image_path = 'path/to/your/chessboard/image.jpg'
# top_left, bottom_right = detect_chessboard(image_path)
# if top_left and bottom_right:
#     print("Top-left corner:", top_left)
#     print("Bottom-right corner:", bottom_right)
