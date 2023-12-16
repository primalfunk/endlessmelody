import chess
import chess.pgn
import music21


# Add this dictionary at the beginning of your script
dynamic_to_velocity = {
    'pp': 30,  # Pianissimo
    'f': 70,  # Forte
    'ff': 100  # Fortissimo
}

# Modify the apply_additional_elements function like this:
def apply_additional_elements(note, elements):
    # Apply dynamics if specified
    if elements['dynamic']:
        dynamic_marking = elements['dynamic']
        velocity = dynamic_to_velocity.get(dynamic_marking, 64)  # Default to 64 if dynamic marking is not found
        note.volume = music21.volume.Volume(velocity=velocity)

    # Apply articulation if specified
    if elements['articulation']:
        if elements['articulation'] == 'staccato':
            note.articulations.append(music21.articulations.Staccato())
        # Additional articulations can be added here as needed

    return note

def chess_moves_to_music(game, board):
    piece_map = {
        chess.PAWN: 'C#',
        chess.KNIGHT: 'A',
        chess.BISHOP: 'F',
        chess.ROOK: 'G',
        chess.QUEEN: 'C',
        chess.KING: 'E-'
    }
    # Expanded rhythm_map based on file
    rhythm_map = {
        0: 4,    # whole note
        1: 3.5,  # seven-eighths note
        2: 3,    # three-quarters note
        3: 2.5,
        4: 2,
        5: 1.5,
        6: 1.75,
        7: 1     # quarter note
    }
    music_stream = music21.stream.Stream()
    note_list = []
    move_count = 0

    for move in game.mainline_moves():
        move_count += 1
        from_square = move.from_square
        to_square = move.to_square
        piece = board.piece_at(from_square)
        if piece:
            pitch_class = piece_map.get(piece.piece_type)
            octave = chess.square_rank(to_square) % 5 + 3
            pitch = f"{pitch_class}{octave}"
            # Transpose logic (expanded to include other musical elements)
            pitch, other_musical_elements = apply_special_move_effects(pitch, board, move)
            file = chess.square_file(to_square)
            duration = rhythm_map[file]
            note = music21.note.Note(pitch, quarterLength=duration)
            # Additional musical elements (e.g., dynamics, articulations) added to note
            apply_additional_elements(note, other_musical_elements)
            note_list.append(note)
            # Chord logic can be more sophisticated based on move count or other factors
            if len(note_list) == 2:
                chord = music21.chord.Chord(note_list)
                music_stream.append(chord)
                note_list = []
        board.push(move)
    return music_stream

def apply_special_move_effects(pitch, board, move):
    # Initialize a dictionary to hold additional musical elements
    elements = {
        'dynamic': None,
        'articulation': None
    }

    # Adjust pitch and add musical elements based on special moves
    if board.is_capture(move):
        pitch = music21.pitch.Pitch(pitch).transpose('-m2')  # Transpose down a minor second
        elements['dynamic'] = 'f'  # Forte for captures
    if board.is_check():
        pitch = music21.pitch.Pitch(pitch).transpose('m2')  # Transpose up a minor second
        elements['articulation'] = 'staccato'  # Staccato for checks
    if board.is_checkmate():
        pitch = music21.pitch.Pitch(pitch).transpose('M2')  # Transpose up a major second
        elements['dynamic'] = 'ff'  # Fortissimo for checkmate
    if board.is_stalemate():
        elements['dynamic'] = 'pp'  # Pianissimo for stalemate

    return pitch, elements


pgn = open('morphy1.pgn')
game = chess.pgn.read_game(pgn)
board = chess.Board()
s = chess_moves_to_music(game, board)
s.show('midi')
s.show()