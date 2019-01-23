class sample_details():
    def __init__(self, sample, individual, center):
        self.sample = sample
        self.individual = individual
        self.center = center

    def __str__(self):
        return (f"donor:{self.individual} sample:{self.sample} "
                f"center:{self.center}")


def get_samples(detail_file):
    '''
    read in the samples detail table, returns a dict
    keyed on sample with sample details objects
    '''
    result = {}
    with open(detail_file, 'r') as details:
        details.readline()  # remove header
        for line in details:
            tokens = line.split()
            result[tokens[1]] = sample_details(sample=tokens[1],
                                               individual=tokens[0],
                                               center=tokens[-1])

    return result
