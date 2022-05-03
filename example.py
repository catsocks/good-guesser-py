from good_guesser import good_guesser


def count_pixels(bmp):
    return sum([line.count("*") for line in bmp])


def concave_pixels(bmp):
    count = 0
    for rows in zip(bmp, bmp[1:], bmp[2:]):
        triples = list(zip(*rows))
        for k in zip(triples, triples[1:], triples[2:]):
            if k[1][1] == " " and count_pixels(k) > 4:
                count += 1
    return count


def num_squares(bmp):
    for row in bmp:
        print("".join(row))
    return good_guesser("num_squares", bmp, count_pixels, concave_pixels)
