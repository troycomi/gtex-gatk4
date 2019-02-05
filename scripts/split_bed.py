import sys
import math


def count_chunks(bed_file,
                 chunk_size):
    '''
    count the number of chunks required to cover the input file
    '''
    total = 0
    with open(bed_file, 'r') as reader:
        for line in reader:
            tokens = line.split()
            total += int(tokens[2]) - int(tokens[1])

    chunks = math.ceil(total / chunk_size)

    if chunks * chunk_size < total:
        chunks += 1

    return chunks


def main():
    '''
    Split a bed file into chunks smaller than a specific size
    Emit the ith window to stdout
    Usage: python split_bed.py <InputBed> <Size> <Window>
    '''

    bedfile = sys.argv[1]
    chunk_size = int(sys.argv[2])
    window = int(sys.argv[3])

    length = 0
    with open(bedfile, 'r') as reader:

        for line in reader:
            tokens = line.split()
            size = int(tokens[2]) - int(tokens[1])
            length += size
            if length > chunk_size * window:
                if length > chunk_size * (window + 1):
                    break
                print(line, end='')


if __name__ == "__main__":
    main()
