def get_map(corners, inverse_corners, fill, vertical, horizontal):
    # Taken from the Godot tilemaps 3x3 simple bitmap implementation
    map = [
        [
            # ,,,,,,
            # ,,##,,
            # ,,##,,
            [
                [corners, corners],
                [vertical, vertical],
            ],
            # ,,,,,,
            # ,,####
            # ,,##,,
            [
                [corners, horizontal],
                [vertical, inverse_corners],
            ],
            # ,,,,,,
            # ######
            # ,,##,,
            [
                [horizontal, horizontal],
                [inverse_corners, inverse_corners],
            ],
            # ,,,,,,
            # ####,,
            # ,,##,,
            [
                [horizontal, corners],
                [inverse_corners, vertical],
            ],
            # ####,,
            # ######
            # ,,##,,
            [
                [fill, inverse_corners],
                [inverse_corners, inverse_corners],
            ],
            # ,,,,,,
            # ######
            # ,,####
            [
                [horizontal, horizontal],
                [inverse_corners, fill],
            ],
            # ,,,,,,
            # ######
            # ####,,
            [
                [horizontal, horizontal],
                [fill, inverse_corners],
            ],
            # ,,####
            # ######
            # ,,##,,
            [
                [inverse_corners, fill],
                [inverse_corners, inverse_corners],
            ],
            # ,,,,,,
            # ,,####
            # ,,####
            [
                [corners, horizontal],
                [vertical, fill],
            ],
            # ,,##,,
            # ######
            # ######
            [
                [inverse_corners, inverse_corners],
                [fill, fill],
            ],
            # ,,,,,,
            # ######
            # ######
            [
                [horizontal, horizontal],
                [fill, fill],
            ],
            # ,,,,,,
            # ####,,
            # ####,,
            [
                [horizontal, corners],
                [fill, vertical],
            ],
        ],
        [
            # ,,##,,
            # ,,##,,
            # ,,##,,
            [
                [vertical, vertical],
                [vertical, vertical],
            ],
            # ,,##,,
            # ,,####
            # ,,##,,
            [
                [vertical, inverse_corners],
                [vertical, inverse_corners],
            ],
            # ,,##,,
            # ######
            # ,,##,,
            [
                [inverse_corners, inverse_corners],
                [inverse_corners, inverse_corners],
            ],
            # ,,##,,
            # ####,,
            # ,,##,,
            [
                [inverse_corners, vertical],
                [inverse_corners, vertical],
            ],
            # ,,##,,
            # ,,####
            # ,,####
            [
                [vertical, inverse_corners],
                [vertical, fill],
            ],
            # ,,####
            # ######
            # ######
            [
                [inverse_corners, fill],
                [fill, fill],
            ],
            # ####,,
            # ######
            # ######
            [
                [fill, inverse_corners],
                [fill, fill],
            ],
            # ,,##,,
            # ####,,
            # ####,,
            [
                [inverse_corners, vertical],
                [fill, vertical],
            ],
            # ,,####
            # ,,####
            # ,,####
            [
                [vertical, fill],
                [vertical, fill],
            ],
            # ,,####
            # ######
            # ####,,
            [
                [inverse_corners, fill],
                [fill, inverse_corners],
            ],
            # ,,,,,,
            # ,,,,,,
            # ,,,,,,
            [
                [None, None],
                [None, None],
            ],
            # ####,,
            # ######
            # ####,,
            [
                [fill, inverse_corners],
                [fill, inverse_corners],
            ],
        ],
        [
            # ,,##,,
            # ,,##,,
            # ,,,,,,
            [
                [vertical, vertical],
                [corners, corners],
            ],
            # ,,##,,
            # ,,####
            # ,,,,,,
            [
                [vertical, inverse_corners],
                [corners, horizontal],
            ],
            # ,,##,,
            # ######
            # ,,,,,,
            [
                [inverse_corners, inverse_corners],
                [horizontal, horizontal],
            ],
            # ,,##,,
            # ####,,
            # ,,,,,,
            [
                [inverse_corners, vertical],
                [horizontal, corners],
            ],
            # ,,####
            # ,,####
            # ,,##,,
            [
                [vertical, fill],
                [vertical, inverse_corners],
            ],
            # ######
            # ######
            # ,,####
            [
                [fill, fill],
                [inverse_corners, fill],
            ],
            # ######
            # ######
            # ####,,
            [
                [fill, fill],
                [fill, inverse_corners],
            ],
            # ####,,
            # ####,,
            # ,,##,,
            [
                [fill, vertical],
                [inverse_corners, vertical],
            ],
            # ,,####
            # ######
            # ,,####
            [
                [inverse_corners, fill],
                [inverse_corners, fill],
            ],
            # ######
            # ######
            # ######
            [
                [fill, fill],
                [fill, fill],
            ],
            # ####,,
            # ######
            # ,,####
            [
                [fill, inverse_corners],
                [inverse_corners, fill],
            ],
            # ####,,
            # ####,,
            # ####,,
            [
                [fill, vertical],
                [fill, vertical],
            ],
        ],        [
            # ,,,,,,
            # ,,##,,
            # ,,,,,,
            [
                [corners, corners],
                [corners, corners],
            ],
            # ,,,,,,
            # ,,####
            # ,,,,,,
            [
                [corners, horizontal],
                [corners, horizontal],
            ],
            # ,,,,,,
            # ######
            # ,,,,,,
            [
                [horizontal, horizontal],
                [horizontal, horizontal],
            ],
            # ,,,,,,
            # ####,,
            # ,,,,,,
            [
                [horizontal, corners],
                [horizontal, corners],
            ],
            # ,,##,,
            # ######
            # ####,,
            [
                [inverse_corners, inverse_corners],
                [fill, inverse_corners],
            ],
            # ,,####
            # ######
            # ,,,,,,
            [
                [inverse_corners, fill],
                [horizontal, horizontal],
            ],
            # ####,,
            # ######
            # ,,,,,,
            [
                [fill, inverse_corners],
                [horizontal, horizontal],
            ],
            # ,,##,,
            # ######
            # ,,####
            [
                [inverse_corners, inverse_corners],
                [inverse_corners, fill],
            ],
            # ,,####
            # ,,####
            # ,,,,,,
            [
                [vertical, fill],
                [corners, horizontal],
            ],
            # ######
            # ######
            # ,,,,,,
            [
                [fill, fill],
                [horizontal, horizontal],
            ],
            # ######
            # ######
            # ,,##,,
            [
                [fill, fill],
                [corners, corners],
            ],
            # ####,,
            # ####,,
            # ,,,,,,
            [
                [fill, vertical],
                [horizontal, corners],
            ],
        ],
    ]
    return map
