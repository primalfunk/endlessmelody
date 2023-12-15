import random
from one_progression import ProgressionFromKey
from music21 import chord, note, interval, key, roman, stream, pitch

class ModulatedProgression:
    def __init__(self):
        self.number_of_progressions = 4  # Total number of progressions including the original
        self.keys = [self.select_random_key()]
        self.progressions = [ProgressionFromKey(self.keys[0])]
        for _ in range(1, self.number_of_progressions):
            new_key = self.select_modulated_key()
            self.keys.append(new_key)
            new_progression = ProgressionFromKey(new_key)
            self.progressions.append(new_progression)
        for i in range(self.number_of_progressions - 1):
            self.modulate_progression(i)
        self.combined_stream = self.combine_streams()
        self.modified_stream = self.drop_lowest_note_octave(self.combined_stream)

    def select_random_key(self):
        self.key_sig = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
        self.modes = ['major', 'minor']
        return key.Key(random.choice(self.key_sig), random.choice(self.modes))

    def select_modulated_key(self):
        last_key = self.keys[-1]  # Get the most recently added key
        possible_keys = [k for k in self.key_sig if k not in [key.tonic.name for key in self.keys]]
        original_key_chords = self.get_chords_from_key(last_key)
        valid_modulation_keys = []
        for k in possible_keys:
            mod_key = key.Key(k, last_key.mode)
            mod_key_chords = self.get_chords_from_key(mod_key)
            common_chords = set(original_key_chords).intersection(set(mod_key_chords))
            if common_chords and not self.is_relative_major_minor(k, last_key):
                valid_modulation_keys.append(k)
        if valid_modulation_keys:
            return key.Key(random.choice(valid_modulation_keys), last_key.mode)
        else:
            return key.Key(random.choice(possible_keys), last_key.mode)

    def is_relative_major_minor(self, key_name, last_key):
            return key.Key(key_name).relative == last_key

    def modulate_progression(self, index):
        if index >= len(self.progressions) - 1:
            return  # No modulation needed for the last progression
        current_key = self.keys[index]
        next_key = self.keys[index + 1]
        current_progression = self.progressions[index]
        pivot_chord = self.find_pivot_chord(current_key, next_key)
        if pivot_chord:
            V_of_pivot_key = roman.RomanNumeral('V', next_key)
            V_of_pivot_key.duration.quarterLength = 4
            current_progression.chords[-2] = V_of_pivot_key
            pivot_chord.duration.quarterLength = 4
            current_progression.chords[-1] = pivot_chord
        else:
            diminished_chord = roman.RomanNumeral('vii°', current_key)
            diminished_chord.duration.quarterLength = 4
            current_progression.chords[-1] = diminished_chord

    def find_pivot_chord(self, current_key, target_key):
        current_key_chords = self.get_chords_from_key(current_key)
        for figure in current_key_chords:
            rn_current = roman.RomanNumeral(figure, current_key)
            rn_target = roman.RomanNumeral(figure, target_key)
            if rn_current.pitchNames == rn_target.pitchNames:
                return rn_current
        return None

    def get_chords_from_key(self, key_obj):
        temp_progression = ProgressionFromKey(key_obj)
        chord_figures = [chord.figure for chord in temp_progression.chords]
        return list(set(chord_figures))

    def combine_streams(self):
        combined = stream.Stream()
        for i, progression in enumerate(self.progressions):
            for chord in progression.chords:
                new_chord = roman.RomanNumeral(chord.figure, self.keys[i])
                new_chord.duration = chord.duration
                combined.append(new_chord)
        self.adjust_chords_to_middle_c(combined)
        self.combined_stream = combined  # Set the combined_stream attribute
        return combined

    def show_original(self):
        self.combined_stream.show('text')
        self.combined_stream.show('midi')
        self.combined_stream.show()

    def show_modified(self):
        self.modified_stream.show('text')
        self.modified_stream.show('midi')
        self.modified_stream.show()

    def adjust_chords_to_middle_c(self, stream_to_adjust):
        target_pitch = note.Note('C4')
        for chord in stream_to_adjust.getElementsByClass('Chord'):
            # Find the closest octave of the chord's root to the target pitch
            root = chord.root()
            interval_to_target = interval.Interval(root, target_pitch)
            closest_octave_transposition = interval_to_target.semitones % 12
            # Transpose chord to the closest octave
            chord.transpose(closest_octave_transposition, inPlace=True)
            # Optional: Further optimize chord voicing to minimize the spread of notes
            chord.closedPosition(forceOctave=4, inPlace=True)


    def drop_lowest_note_octave(self, roman_stream):
        modified_stream = stream.Stream()
        for item in roman_stream:
            if isinstance(item, roman.RomanNumeral):
                chord_obj = chord.Chord(item.pitches)
                chord_obj.duration.quarterLength = 4
                lowest_note = min(chord_obj.notes, key=lambda n: n.pitch.midi)
                lowest_note.transpose(interval.Interval(-12), inPlace=True)
                modified_stream.append(chord_obj)
            else:
                modified_stream.append(item)
        return modified_stream