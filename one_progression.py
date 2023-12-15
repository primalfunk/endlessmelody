from progressions import *
import random
from music21 import scale, stream, note, roman, key

class ProgressionFromKey:
    def __init__(self, input_key=None):
        if input_key is None:
            self.selected_key = self.select_random_key()
        else:
            self.selected_key = input_key
        self.progressions = []
        self.get_progressions()
        self.chords = []
        self.convert_roman_to_chords(self.selected_key)
        self.stream = self.convert_to_stream()

    def select_random_key(self):
        key_sig = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
        modes = ['major', 'minor']
        random_mode = random.choice(modes)
        random_key = key.Key(random.choice(key_sig), random_mode)
        return random_key
    
    def get_progressions(self, count=4):
        for i in range(count):
            if self.selected_key.mode == 'minor':
                progression = random.choice(list(minor_progressions.values()))
            else:
                progression = random.choice(list(major_progressions.values()))
            self.progressions.append(progression)

    def convert_roman_to_chords(self, key_name):
        list_of_romans = self._flatten_sum(self.progressions)
        self.chords = []
        for numeral in list_of_romans:
            rn = roman.RomanNumeral(numeral, key_name)
            self.chords.append(rn)

    def _flatten_sum(self, matrix):
        return sum(matrix, [])
    
    def convert_to_stream(self):
        s = stream.Stream()
        for rn in self.chords:
            rn.duration.quarterLength = 4
            s.append(rn)
        return s