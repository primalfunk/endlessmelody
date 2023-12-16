import random
from music21 import chord, pitch, interval, key, pitch, scale, stream

class SongBuilder:
    def __init__(self):
        self.key = self.select_random_key()
        # Set tonic to the tonic of the key, with octave 4
        self.tonic = pitch.Pitch(str(self.key.tonic) + '4')
        self.dominant = self.calculate_dominant()

    def select_random_key(self):
        # List of key names
        key_names = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 
                     'C#', 'D#', 'F#', 'G#', 'A#', 
                     'Db', 'Eb', 'Gb', 'Ab', 'Bb']

        # Selecting major or minor mode
        major_minor = ['M', 'm']
        random_mode = random.choice(major_minor)

        # Forming the key string
        random_key_name = random.choice(key_names) + random_mode

        # Creating the key object
        return key.Key(random_key_name)
        
    def calculate_dominant(self):
        # Calculate the dominant note in the selected key
        dominant_scale_degree = 5
        dominant_pitch = self.key.getScale().pitchFromDegree(dominant_scale_degree)
        # Ensure the dominant pitch is in the same octave as the tonic
        return pitch.Pitch(dominant_pitch.name + '4')
    
    def generate_chords(self):
        # Generate the three chords (Tonic, Dominant, Tonic)
        tonic_chord = chord.Chord([self.tonic, interval.Interval('M3').transposePitch(pitch.Pitch(self.tonic)), interval.Interval('P5').transposePitch(pitch.Pitch(self.tonic))])
        dominant_chord = chord.Chord([self.dominant, interval.Interval('M3').transposePitch(pitch.Pitch(self.dominant)), interval.Interval('P5').transposePitch(pitch.Pitch(self.dominant))])

        # Normalize chords to fit within the specified range
        tonic_chord = self.normalize_chord(tonic_chord)
        dominant_chord = self.normalize_chord(dominant_chord)

        return tonic_chord, dominant_chord, tonic_chord

    def normalize_chord(self, chord_to_normalize):
        # Ensure the chord falls within an octave and a half range, near middle C
        while chord_to_normalize.bass().midi > pitch.Pitch('C4').midi + 12 * 1.5:
            chord_to_normalize = chord_to_normalize.inversion(1)
        while chord_to_normalize.bass().midi < pitch.Pitch('C4').midi - 12 * 1.5:
            chord_to_normalize = chord_to_normalize.inversion(-1)
        return chord_to_normalize

# Create an instance of SongBuilder and generate chords
song_builder = SongBuilder()
chords = song_builder.generate_chords()

s = stream.Stream()
for c in chords:
    nc = chord.Chord(c)
    s.append(nc)

s.show('midi')
s.show()
