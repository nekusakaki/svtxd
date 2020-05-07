def rgb_to_hex(rgb):
    r, g, b = [x >> 8 for x in rgb]
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)
