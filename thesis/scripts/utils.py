METHODS = ["moe",
           "mopgfm",
           "poe",
           "iwmogfm_amortized",
           "mofop",
           "iwmogfm2",
           "mopoe"]

method_footnote_mapping = {'mopoe': r'mopoe \footnote{mixture-of-product-of-expert}',
                           'mopgfm': r'mopgfm \footnote{mixture-of-parameter-generalized-$f$-mean}',
                           # 'mogfm': r'mogfm \footnote{mixture-of-generalized-$f$-mean}',
                           'moe': r'moe \footnote{mixture-of-experts}',
                           'poe': r'poe \footnote{product-of-experts}',
                           'mofop': r'mofop \footnote{mixture-of-flow-of-experts}',
                           'iwmogfm2': r'iwmogfm2 \footnote{importance-weighted-mixture-of-generalized-$f$-mean}',
                           'iwmogfm_amortized': r'iwmogfm amortized \footnote{amortized-importance-weighted-mixture-of-generalized-$f$-mean}',
                           }
