# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import vx.platform

if vx.platform.IS_REAL_HARDWARE:
    import board
    import keypad

    matrix = keypad.KeyMatrix(
        row_pins = (board.A1, board.A2, board.A3, board.A4),
        column_pins = (board.A5, board.MISO, board.RX, board.TX, board.D12, board.D11, board.D10, board.D9, board.D6, board.D5)
    )
else:
    matrix = None