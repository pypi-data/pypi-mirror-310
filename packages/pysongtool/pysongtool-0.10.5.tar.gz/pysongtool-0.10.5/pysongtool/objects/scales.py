# {name: [notes (semitones)]}

scales_list = {
    
    #Major Scales



    'maj': {
        "notes": [2, 4, 5, 7, 9, 11],
        "chords": ['maj', 'min', 'min', 'maj', 'maj', 'min', 'dim']
    },

    'min': {
        "notes": [2, 3, 5, 7, 8, 10],
        "chords": ['min', 'dim', 'maj', 'min', 'min', 'maj', 'maj']
    },

    'harmonic_min': {
        "notes": [2, 3, 5, 7, 8, 11],
        "chords": ['min', 'dim', 'aug', 'min', 'maj', 'maj', 'dim']
    },

    'melodic_min': {
        "notes": [2, 3, 5, 7, 9, 11],
        "chords": ['min', 'min', 'aug', 'maj', 'maj', 'dim', 'dim']
    },


    #The greek modes

    'ionian': {
        "notes": [2, 4, 5, 7, 9, 11],
        "chords": ['maj', 'min', 'min', 'maj', 'maj', 'min', 'dim']
    },

    'dorian': {
        "notes": [2, 3, 5, 7, 9, 10],
        "chords": ['min', 'min', 'maj', 'min', 'min', 'dim', 'dom']
    },

    'phrygian': {
        "notes": [1, 3, 5, 7, 8, 10],
        "chords": ['min', 'maj', 'maj', 'min', 'dim', 'maj', 'min']
    },

    'lydian': {
        "notes": [2, 4, 6, 7, 9, 11],
        "chords": ['maj', 'maj', 'min', 'dim', 'maj', 'min', 'min']
    },

    'mixolydian': {
        "notes": [2, 4, 5, 7, 9, 10],
        "chords": ['maj', 'min', 'dim', 'maj', 'min', 'min', 'maj']
    },

    'aeolian': {
        "notes": [2, 3, 5, 7, 8, 10],
        "chords": ['min', 'dim', 'maj', 'min', 'min', 'maj', 'maj']
    },

    'locrian': {
        "notes": [1, 3, 5, 6, 8, 10],
        "chords": ['dim', 'maj', 'min', 'min', 'maj', 'maj', 'min']
    },

    #Pentatonic Scales

    'pentatonic_maj': {
        "notes": [2, 4, 7, 9],
        "chords": ['','','','','','',]
    },

    'pentatonic_min': {
        "notes": [3, 5, 7, 10],
        "chords": ['','','','','',]
    },

    'blues': {
        "notes": [3, 5, 6, 7, 10],
        "chords": ['','','','','','',]
    }
}
