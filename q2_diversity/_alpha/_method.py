# ----------------------------------------------------------------------------
# Copyright (c) 2016-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import biom
import pandas as pd
import skbio.diversity
import unifrac

from q2_types.feature_table import BIOMV210Format
from q2_types.tree import NewickFormat


# We should consider moving these functions to scikit-bio. They're part of
# the private API here for now.

def phylogenetic_metrics():
    return {'faith_pd'}


# must contain an entry for every metric in phylogenetic_metrics
def _phylogenetic_functions():
    return {'faith_pd': unifrac.faith_pd}


def non_phylogenetic_metrics():
    return {'ace', 'chao1', 'chao1_ci', 'berger_parker_d', 'brillouin_d',
            'dominance', 'doubles', 'enspie', 'esty_ci', 'fisher_alpha',
            'goods_coverage', 'heip_e', 'kempton_taylor_q', 'margalef',
            'mcintosh_d', 'mcintosh_e', 'menhinick', 'michaelis_menten_fit',
            'observed_otus', 'osd', 'pielou_e', 'robbins', 'shannon',
            'simpson', 'simpson_e', 'singles', 'strong', 'gini_index',
            'lladser_pe', 'lladser_ci'}


def alpha_phylogenetic(table: BIOMV210Format, phylogeny: NewickFormat,
                       metric: str) -> pd.Series:
    metrics = phylogenetic_metrics()
    if metric not in metrics:
        raise ValueError("Unknown phylogenetic metric: %s" % metric)

    f = _phylogenetic_functions()[metric]

    result = f(str(table), str(phylogeny))

    result.name = metric
    return result


def alpha(table: biom.Table, metric: str) -> pd.Series:
    if metric not in non_phylogenetic_metrics():
        raise ValueError("Unknown metric: %s" % metric)
    if table.is_empty():
        raise ValueError("The provided table object is empty")

    counts = table.matrix_data.toarray().astype(int).T
    sample_ids = table.ids(axis='sample')

    result = skbio.diversity.alpha_diversity(metric=metric, counts=counts,
                                             ids=sample_ids)
    result.name = metric
    return result
