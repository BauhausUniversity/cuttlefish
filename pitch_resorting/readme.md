# Detect pitches in audiofile, create note events and resort them according to an input MIDI file

Let's go:

1. Open `pitch_resorting.pd` with Pure Data.
2. Install the Cyclone external if missing. 
3. Load source material: Use a video with distinct monophonic frequencies (for example a recording with a wind instrument).
4. Extract the audio as a .wav file (44100 Hz). Open and analyze the audio with the Pd patch.
5. Use a MIDI .mid file to re-sort the notes found in the .wav according to the .mid file. 
6. If notes are missing (check console for messages) transpose the MIDI file.
7. Save as XML. 
8. paste XML inside a Shotcut file.
