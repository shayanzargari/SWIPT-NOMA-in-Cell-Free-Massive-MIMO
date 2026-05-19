def pair_users(sorted_channels):
    pairs = []
    left = 0
    right = len(sorted_channels) - 1

    while left < right:
        pairs.append((sorted_channels[left], sorted_channels[right]))
        left += 1
        right -= 1

    return pairs
