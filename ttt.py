#!/usr/bin/python

import sys, os, copy
from random import randint

CLEARSCR = 0
SHOW_THINKING = 1

m = [[' ', ' ', ' '],
     [' ', ' ', ' '], 
     [' ', ' ', ' ']] 

def draw_board():
    if CLEARSCR:
        os.system('clear')
    print
    print "     1   2   3"
    print "   +---+---+---+"
    print "A  | %s | %s | %s |  " % (m[0][0], m[1][0], m[2][0])
    print "   +---+---+---+"
    print "B  | %s | %s | %s |  " % (m[0][1], m[1][1], m[2][1])
    print "   +---+---+---+"
    print "C  | %s | %s | %s |  " % (m[0][2], m[1][2], m[2][2])
    print "   +---+---+---+"
    print

def make_move():
    odd_move = move%2
    if (odd_move and player == 'X') or (not odd_move and player == 'O'):
        player_move()
    else:
        computer_move()

def player_move():

    x = None
    y = None
    while x is None:
        print
        print "Make a move: ",

        move = sys.stdin.readline()
        move = move.strip()

        # q for quite
        if move == 'q':
            print 'quit'
            exit(1)

        xs = ys = None
        if len(move) == 2:
            xs = move[0].lower()
            ys = move[1]

        # validate move
        if len(move)!=2 or xs not in ('a','b','c') or ys not in ('1','2','3'):
            print 'move must be of the form a1, a2, a3, b1, ... etc.'
            continue
        
        x = int(ys)-1
        y = ord(xs)-97

        if m[x][y] != ' ':
            print "%s is already taken" % move
            x = None
            continue

    m[x][y] = player

def computer_move():
    cmove = None
    if SHOW_THINKING:
        print 'computer:'
        print 1, 'check for win'
    # check if computer can win:
    for y in range(3):
        for x in range(3):
            if m[x][y] == ' ':
                m2 = copy.deepcopy(m)
                m2[x][y] = computer
                winner, msg = is_game_over(m2)
                if winner:
                    m[x][y] = computer
                    return
    # block a win
    if SHOW_THINKING:
        print 2, 'check for block win'
    for y in range(3):
        for x in range(3):
            if m[x][y] == ' ':
                m2 = copy.deepcopy(m)
                m2[x][y] = player
                winner, msg = is_game_over(m2)
                if winner:
                    m[x][y] = computer
                    return

    if SHOW_THINKING:
        print 3, 'take center'
    # take center if pos:
    if m[1][1] == ' ':
        m[1][1] = computer
        return

    if SHOW_THINKING:
        print 4, 'random move'
    # random
    possibles = []
    for y in range(3):
        for x in range(3):
            if m[x][y] == ' ':
                possibles.append((x,y))
    print 'possibles: ', possibles

    ch = possibles[randint(0, len(possibles)-1)]
    print 'ch:', ch
    m[ch[0]][ch[1]] = computer
            
def is_game_over(m):
    game_msg = None

    # flatten board
    board = ''
    for y in range(3):
        for x in range(3):
            board += m[x][y]

    if ' ' not in board:
        game_msg = 'No one wins.'
        return True, game_msg

    for mark in (player, computer):
        # compos
        for c in ((0,1,2), (3,4,5), (6,7,8), # rows
                  (0,3,6), (1,4,7), (2,5,8), # columns
                  (0,4,8), (2,4,6)):         # diagnals
            if board[c[0]] == board[c[1]] == board[c[2]] == mark:
                game_msg = '%s Wins!' % mark
                return True, game_msg
    return False, game_msg

# Main Loop

# X goes first
player='X'
computer='O'

draw_board()

move = 0
done = False
while not done:
    move += 1
    make_move()
    draw_board()
    done, game_msg = is_game_over(m)
print game_msg
