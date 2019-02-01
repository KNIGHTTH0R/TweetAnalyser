from stanfordcorenlp import StanfordCoreNLP
from glob import glob
import pandas as pd

from secret import *
from filter import Filter

nlp = StanfordCoreNLP(LOCATION_STARFORD_CORE_NLP)

# Load Dictionaries - Create Filter
winter_storm_filenames = glob('./Dictionaries/winter_storm_terms_*.txt')
winter_storm_terms = Filter.terms_from_files(winter_storm_filenames)

print('{} winter storm terms loaded.'.format(len(winter_storm_terms)))

# Input Tweets
