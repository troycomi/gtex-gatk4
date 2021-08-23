from cosmic_pons import (read_pon_list, read_cosmic, read_pon, tabulate_pon,
                         remove_empty)
from io import StringIO
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal as afe
from numpy.testing import assert_array_equal as aae


def test_read_pon_list():
    pon_list = StringIO('pon1\n/sys/pon2\npon3')
    assert read_pon_list(pon_list) == 'pon1 /sys/pon2 pon3'.split()
    pon_list = StringIO('pon1\n/sys/pon2\npon3\n')
    assert read_pon_list(pon_list) == 'pon1 /sys/pon2 pon3'.split()
    pon_list = StringIO('pon1')
    assert read_pon_list(pon_list) == ['pon1']
    pon_list = StringIO('')
    assert read_pon_list(pon_list) == []


def test_read_cosmic():
    cosmic = StringIO(
        'Accession Number\tMutation genome position\n'
        'ENST297338\t8:117869609-117869609\n'
        'ENST288602\t\n'
        'ENST440973\t6:152129237-152129237\n'
        'ENST440974\t6:152129237-152129238\n'
        'ENST440975\t6:152129236-152129238\n'
    )
    expected = pd.read_csv(StringIO(
        'Accession Number\tchrom\tstart\tend\n'
        'ENST297338\t8\t117869609\t117869609\n'
        'ENST440973\t6\t152129237\t152129237\n'
        'ENST440974\t6\t152129237\t152129238\n'
        'ENST440975\t6\t152129236\t152129238\n'
    ), sep='\t')

    aae(read_cosmic(cosmic).values, expected.values)


def test_read_pon():
    vcf = StringIO(
        '##tumor_sample=P9-C3\n'
        '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n'
        '1\t10146\t.\tAC\tA\t.\t.\t.\n'
        '1\t10151\t.\tTA\tT,GA\t.\t.\t.\n'
        '1\t10403\t.\tACCCTAACCCTAACCCTAACCCTAACCCTAACCCTAAC\tA\t.\t.\t.\n'
        '1\t10415\t.\tACCCTAACCCTAACCCTAACCCTAAC\tA\t.\t.\t.\n'
        'hs37d5\t35466424\t.\tG\tGATTCC\t.\t.\t.\n'
        'hs37d5\t35466456\t.\tC\tT\t.\t.\t.\n'
        'X\t155260422\t.\tAGGGGTTAGGGGTTAG\tAGGGTTAGGGGTTAG,A\t.\t.\t.\n'
        'Y\t2661694\t.\tA\tG\t.\t.\t.\n'
        'MT\t151\t.\tCT\tTT,TC\t.\t.\t.'
    )

    result = read_pon(vcf)
    expected = pd.read_csv(StringIO(
        'chrom\tpos\n'
        '1\t10146\n'
        '1\t10151\n'
        '1\t10403\n'
        '1\t10415\n'
    ), sep='\t')
    afe(result, expected)


def test_tabulate_pon():
    cosmic = pd.read_csv(StringIO(
        'Accession Number\tchrom\tstart\tend\n'
        'ENST297338\t8\t117869609\t117869609\n'
        'ENST440973\t6\t152129237\t152129237\n'
        'ENST440974\t6\t152129237\t152129238\n'
        'ENST440975\t6\t152129236\t152129238\n'
    ), sep='\t')
    pon = pd.read_csv(StringIO(
        'chrom\tpos\n'
        '1\t10151\n'
        '1\t10403\n'
        '1\t10415\n'
    ), sep='\t')

    result = tabulate_pon(cosmic, pon, 'test')
    afe(result, cosmic)

    pon = pd.read_csv(StringIO(
        'chrom\tpos\n'
        '8\t117869609\n'
        '1\t10403\n'
        '1\t10415\n'
    ), sep='\t')

    cosmic = tabulate_pon(cosmic, pon, 'test')
    expected = pd.read_csv(StringIO(
        'Accession Number\tchrom\tstart\tend\ttest\n'
        'ENST297338\t8\t117869609\t117869609\t1\n'
        'ENST440973\t6\t152129237\t152129237\t0\n'
        'ENST440974\t6\t152129237\t152129238\t0\n'
        'ENST440975\t6\t152129236\t152129238\t0\n'
    ), sep='\t')
    afe(cosmic, expected)

    pon = pd.read_csv(StringIO(
        'chrom\tpos\n'
        '8\t117869609\n'
        '6\t152129235\n'
        '6\t152129236\n'
        '6\t152129237\n'
        '6\t152129238\n'
        '6\t152129239\n'
    ), sep='\t')

    cosmic = tabulate_pon(cosmic, pon, 'test2')
    expected = pd.read_csv(StringIO(
        'Accession Number\tchrom\tstart\tend\ttest\ttest2\n'
        'ENST297338\t8\t117869609\t117869609\t1\t1\n'
        'ENST440973\t6\t152129237\t152129237\t0\t1\n'
        'ENST440974\t6\t152129237\t152129238\t0\t2\n'
        'ENST440975\t6\t152129236\t152129238\t0\t3\n'
    ), sep='\t')
    afe(cosmic, expected)


def test_remove_empty():
    cosmic = pd.read_csv(StringIO(
        'Accession Number\tchrom\tstart\tend\n'
        'ENST297338\t8\t117869609\t117869609\n'
        'ENST440973\t6\t152129237\t152129237\n'
        'ENST440974\t6\t152129237\t152129238\n'
        'ENST440975\t6\t152129236\t152129238\n'
    ), sep='\t')
    with pytest.raises(ValueError) as e:
        remove_empty(cosmic)
    assert 'No matches to write' in str(e)

    cosmic = pd.read_csv(StringIO(
        'Accession Number\tchrom\tstart\tend\ttest\ttest2\n'
        'ENST297338\t8\t117869609\t117869609\t1\t1\n'
        'ENST440973\t6\t152129237\t152129237\t0\t1\n'
        'ENST440974\t6\t152129237\t152129238\t0\t2\n'
        'ENST440975\t6\t152129236\t152129238\t0\t3\n'
    ), sep='\t')
    afe(cosmic, remove_empty(cosmic))

    cosmic = pd.read_csv(StringIO(
        'Accession Number\tchrom\tstart\tend\ttest\ttest2\n'
        'ENST297338\t8\t117869609\t117869609\t1\t1\n'
        'ENST440973\t6\t152129237\t152129237\t0\t0\n'
        'ENST440974\t6\t152129237\t152129238\t0\t2\n'
        'ENST440975\t6\t152129236\t152129238\t0\t0\n'
    ), sep='\t')
    expected = pd.read_csv(StringIO(
        'Accession Number\tchrom\tstart\tend\ttest\ttest2\n'
        'ENST297338\t8\t117869609\t117869609\t1\t1\n'
        'ENST440974\t6\t152129237\t152129238\t0\t2\n'
    ), sep='\t')
    aae(expected.values, remove_empty(cosmic).values)
