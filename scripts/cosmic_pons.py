import click
from typing import List, TextIO
import pandas as pd
import numpy as np
import os
from io import StringIO
import gzip
import time


@click.command()
@click.option('--cosmic', type=click.File())
@click.option('--pon-list', type=click.File())
@click.option('--pon', type=click.File())
@click.option('--output', type=click.File('w'))
def check_overlap(cosmic, pon_list, pon, output):
    cosmic = read_cosmic(cosmic)
    click.echo('read in cosmic file')
    if pon_list:
        pons = read_pon_list(pon_list)
        click.echo(f'found {len(pons)} pon files')
        for i, pon in enumerate(pons):
            basename = os.path.basename(pon)
            basename = os.path.splitext(basename)[0]
            click.echo(f'{time.asctime()} -> pon {i+1} of {len(pons)}: {basename}')
            cosmic = tabulate_pon(cosmic,
                                  read_pon(gzip.open(pon, 'rt')), basename)
        cosmic = remove_empty(cosmic)
    else:
        click.echo('single pon')
        cosmic = tabulate_pon(cosmic, read_pon(pon), 'pon')
    cosmic.to_csv(output, sep='\t', index=False)


def read_pon_list(pon_list: TextIO) -> List[str]:
    return [pon.strip() for pon in pon_list.readlines()]


def read_cosmic(cosmic: TextIO) -> pd.DataFrame:
    result = pd.read_csv(
        cosmic, sep='\t',
        usecols=['Accession Number', 'Mutation genome position'])
    result.dropna(inplace=True)
    temp = result['Mutation genome position'].str.split(
        r'(\d+):(\d+)-(\d+)', expand=True
    ).loc[:, [1, 2, 3]].astype('int64').rename(
        columns={1: 'chrom', 2: 'start', 3: 'end'})
    result = result.merge(
        temp, left_index=True, right_index=True).drop(
            axis=1, columns='Mutation genome position')
    return result


def read_pon(pon: TextIO) -> pd.DataFrame:
    pon = StringIO('\n'.join(filter(lambda p: p.split()[0].isdigit(),
                                    pon)))
    result = pd.read_csv(
        pon, sep='\t', comment='#',
        header=None, names=['chrom', 'pos'],
        usecols=[0, 1], dtype='int64'
    )
    return result


def tabulate_pon(cosmic: pd.DataFrame, pon: pd.DataFrame, name: str
                 ) -> pd.DataFrame:
    '''
    Check all positions in pon for a matching overlap in cosmic
    If none are found, cosmic is returned without modification
    Otherwise a column is added with name 'name' and the tally is value
    '''
    # insert at end
    ponvals = pon.values
    sub_slice = 1000
    tally = np.zeros((len(cosmic.chrom),), dtype='int64')
    # for i in range(ponvals.shape[0]):
    #     tally += ((cosmic.chrom == ponvals[i, 0]) &
    #               (cosmic.start <= ponvals[i, 1]) &
    #               (cosmic.end >= ponvals[i, 1]))

    # total_slices = len(range(0, ponvals.shape[0], sub_slice))
    # for i in range(0, ponvals.shape[0], sub_slice):
    #     current = i // sub_slice
    #     if current % 10 == 0:
    #         click.echo(f'{time.asctime()} -> section {current} of {total_slices}')
    #     end = min(ponvals.shape[0], i + sub_slice)
    #     tally += np.sum(np.equal.outer(cosmic.chrom, ponvals[i:end, 0]) &
    #                     np.less_equal.outer(cosmic.start, ponvals[i:end, 1]) &
    #                     np.greater_equal.outer(cosmic.end, ponvals[i:end, 1]),
    #                     axis=1)

    for chrom in range(1, 24):
        click.echo(f'{time.asctime()} -> Chromosome {chrom}')
        p_temp = ponvals[ponvals[:, 0] == chrom, 1]
        c_match = cosmic.chrom == chrom
        total_slices = len(range(0, p_temp.shape[0], sub_slice))
        for i in range(0, p_temp.shape[0], sub_slice):
            current = i // sub_slice
            # if current % 100 == 0:
            #     click.echo(f'{time.asctime()} -> section {current} of {total_slices}')
            end = min(p_temp.shape[0], i + sub_slice)
            tally[c_match] += np.sum(
                np.less_equal.outer(cosmic.loc[c_match, 'start'], p_temp[i:end]) &
                np.greater_equal.outer(cosmic.loc[c_match, 'end'], p_temp[i:end]),
                axis=1)
    if np.sum(tally) > 0:
        cosmic[name] = tally
    return cosmic


def remove_empty(cosmic: pd.DataFrame) -> pd.DataFrame:
    '''
    Remove any rows where no pon has overlap
    '''
    tallies = cosmic.iloc[:, 4:]
    if tallies.empty:
        click.echo('No overlapping regions found in PONs')
        raise ValueError('No matches to write')

    return cosmic.loc[tallies.values.sum(axis=1) != 0, :]


if __name__ == "__main__":
    check_overlap()
