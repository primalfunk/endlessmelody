import chess
import chess.pgn
import music21

class ChessMusicComposer:
    def __init__(self, pgn_file):
        self.pgn_file = pgn_file

    def select_key(self, first_move):
        file = chess.square_file(first_move.from_square)
        major_keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        return major_keys[file % len(major_keys)] + " Major"

    def create_scale_object(self, key_string):
        return music21.scale.MajorScale(key_string.split()[0])

    def create_chord(self, move, scale_obj, is_white_move):
        file_map = {'a': 7, 'b': 6, 'c': 4, 'd': 2, 'e': 1, 'f': 3, 'g': 5, 'h': 7}
        rank_duration_map = {1: 0.25, 2: 0.25, 3: 0.5, 4: 0.5, 5: 1, 6: 1, 7: 2, 8: 4}
        file_letter = chr(chess.square_file(move.to_square) + ord('a'))
        rank = chess.square_rank(move.to_square if is_white_move else move.from_square)
        chord_degree = file_map[file_letter]
        duration = rank_duration_map[rank + 1]
        root_pitch = scale_obj.pitchFromDegree(chord_degree)
        chord_pitches = [root_pitch, root_pitch.transpose('M3' if is_white_move else 'm3'), root_pitch.transpose('P5')]
        chord = music21.chord.Chord(chord_pitches, quarterLength=duration)
        return chord

    def update_key(self, scale_obj, board, move):
        if board.is_capture(move):
            scale_obj = scale_obj.transpose('m2')
        elif board.is_check():
            scale_obj = scale_obj.transpose('M2')
        return scale_obj

    def chess_moves_to_music(self):
        with open(self.pgn_file) as pgn:
            game = chess.pgn.read_game(pgn)
            board = chess.Board()
            moves = list(game.mainline_moves())
            key_string = self.select_key(moves[0])
            scale_obj = self.create_scale_object(key_string)
            music_stream = music21.stream.Stream()

            for i, move in enumerate(moves):
                is_white_move = i % 2 == 0
                chord = self.create_chord(move, scale_obj, is_white_move)
                music_stream.append(chord)
                scale_obj = self.update_key(scale_obj, board, move)
                board.push(move)

            return music_stream

    def show_music(self):
        music_stream = self.chess_moves_to_music()
        music_stream.show('midi')
        music_stream.show()

# Example Usage
composer = ChessMusicComposer('morphy1.pgn')
composer.show_music()
