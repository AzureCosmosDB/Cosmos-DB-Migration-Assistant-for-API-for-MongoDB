from .assess_unique_index import *
from .assess_compound_index_nested_field import *
from .assess_unique_index_nested_field import *

def assess_partially_supported_indexing_features(self):
    assess_unique_index(self)
    assess_compound_index_nested_field(self)
    assess_unique_index_nested_field(self)