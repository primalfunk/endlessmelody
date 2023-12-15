from music21 import stream, note, chord, key, roman
from modulated import ModulatedProgression
import random
from rhythms import rhythm_patterns

class RhythmicBassLineCreator:
    def __init__(self):
        m = ModulatedProgression()
        self.chord_stream = m.modified_stream
        self.bass_stream = stream.Stream()
        self.create_bass_line()
        self.combined_stream = self.combine_streams()

    def set_rhythm_pattern(self, pattern):
        self.rhythm_pattern = pattern

    def extract_bass_notes(self):
        bass_notes = []
        for ch in self.chord_stream.getElementsByClass('Chord'):
            bass_note = ch.bass()
            bass_notes.append(bass_note)
        return bass_notes

    def calculate_probabilities(self, num_patterns):
        probabilities = []
        probability = 50
        for _ in range(num_patterns):
            probabilities.append(probability)
            probability = max(1, probability - 2)
        return probabilities

    def apply_rhythmic_pattern(self, bass_notes, bar_length=4, key_change_bars=[17, 33, 49]):
        probabilities = self.calculate_probabilities(len(rhythm_patterns))
        total_prob = sum(probabilities)
        weighted_patterns = [pattern for pattern, weight in zip(rhythm_patterns, probabilities) for _ in range(weight)]
        offset = 0.0
        remaining_repetitions = 0
        chosen_pattern = None
        current_bar = 1
        for bass_note in bass_notes:
            if remaining_repetitions == 0 or current_bar in key_change_bars:
                chosen_pattern = random.choice(weighted_patterns)
                repetition_choice = random.choices([1, 2, 4], weights=[25, 50, 15], k=1)[0]
                remaining_repetitions = min(repetition_choice, key_change_bars[0] - current_bar)
            for rhythm_duration in chosen_pattern:
                new_note = note.Note(bass_note)
                new_note.duration.quarterLength = rhythm_duration
                new_note.offset = offset
                self.bass_stream.append(new_note)
                offset += rhythm_duration
            remaining_repetitions -= 1
            current_bar += 1 if offset % bar_length == 0 else 0

    def create_bass_line(self):
        bass_notes = self.extract_bass_notes()
        self.apply_rhythmic_pattern(bass_notes)

    def combine_streams(self):
        combined = stream.Stream()
        for ch in self.chord_stream:
            combined.insert(ch.offset, ch)
        for bass_note in self.bass_stream:
            combined.insert(bass_note.offset, bass_note)
        return combined