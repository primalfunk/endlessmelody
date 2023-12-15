from music21 import stream, chord, note, interval, pitch
from bass_elaborator import RhythmicBassLineCreator

class AutoMelody:
    def __init__(self):
        r = RhythmicBassLineCreator()
        self.chords_and_bass = r.combined_stream
        self.melody_scaffolding = self.create_melody_scaffolding()

    def analyze_chords(self, bar_chords):
        highest_note = None
        pitch_classes = {}

        for ch in bar_chords:
            # Find the highest note in the chord
            top_note = ch.sortAscending()[-1]
            if highest_note is None or top_note > highest_note:
                highest_note = top_note

            # Count the pitch classes
            for p in ch.pitches:
                pc = p.pitchClass
                pitch_classes[pc] = pitch_classes.get(pc, 0) + 1

        # Get the common pitch classes
        common_pitches = [pitch.Pitch(pc) for pc in pitch_classes if pitch_classes[pc] > 1]
        return highest_note, common_pitches

    def select_melody_note(self, highest_note, common_pitches):
        # Convert highest_note to a Pitch object if it's a Note
        highest_pitch = highest_note.pitch if isinstance(highest_note, note.Note) else highest_note

        # Find a note that is a perfect fourth or more above the highest chord note
        melody_note_pitch = highest_pitch.transpose('P4')
        common_pitch_classes = [p.pitchClass for p in common_pitches]

        while melody_note_pitch.pitchClass not in common_pitch_classes:
            melody_note_pitch = melody_note_pitch.transpose('m2')

        # Return the transposed Pitch
        return melody_note_pitch

    def create_melody_scaffolding(self):
        melody_stream = stream.Stream()
        chords = list(self.chords_and_bass.getElementsByClass('Chord'))

        for i in range(0, len(chords), 4):
            bar_chords = chords[i:i + 4]
            highest_note, common_pitches = self.analyze_chords(bar_chords)
            melody_note_pitch = self.select_melody_note(highest_note, common_pitches)

            for ch in bar_chords:
                melodic_note = note.Note()
                melodic_note.pitch = melody_note_pitch
                melodic_note.duration.type = 'whole'
                melody_stream.append(melodic_note)

        return melody_stream


    def play_combined(self):
        combined = self.merge_streams()
        combined.show('text')
        combined.show('midi')
        combined.show()

    def merge_streams(self):
        combined_stream = stream.Stream()
        for element in self.chords_and_bass:
            combined_stream.insert(element.offset, element)
        for element in self.melody_scaffolding:
            combined_stream.insert(element.offset, element)
        return combined_stream

# Example usage
# Assuming 'stream_from_previous_step' is the stream you've created in the previous steps
a = AutoMelody()
a.play_combined()
