"""
#########################
Football-Data soccer data
#########################

This example illustrates the usage of Football-Data soccer dataloader.

"""

# Author: Georgios Douzas <gdouzas@icloud.com>
# Licence: MIT

from sportsbet.datasets import FDSoccerDataLoader

###############################################################################
# Getting the available parameters
###############################################################################

###############################################################################
# We can get the available parameters in order to select the training data
# to be extracted, using the :meth:`get_all_params` class method.

FDSoccerDataLoader.get_all_params()

###############################################################################
# We select to extract training data only for the year 2021 of the first
# division Spanish and Italian leagues.

param_grid = {'league': ['Spain', 'Italy'], 'division': [1], 'year': [2021]}
dataloader = FDSoccerDataLoader(param_grid=param_grid)

###############################################################################
# Getting the available odds types
###############################################################################

###############################################################################
# We can get the available odds types in order to match the output of the
# training data, using the :func:`~sportsbet.datasets.FDSoccerDataLoader.get_odds_types` class method.

dataloader.get_odds_types()

###############################################################################
# We select the odds types to be the market average.

odds_type = 'market_average'

###############################################################################
# Extracting the training data
###############################################################################

###############################################################################
# We extract the training data, keeping columns and rows with non missing
# values by setting the ``drop_na_thres``` parameter equal to ``1.0```.

X_train, Y_train, O_train = dataloader.extract_train_data(
    drop_na_thres=1.0, odds_type=odds_type
)

###############################################################################
# The input data:
print(X_train)

###############################################################################
# The targets:
print(Y_train)

###############################################################################
# The market average odds:
print(O_train)

###############################################################################
# Extracting the fixtures data
###############################################################################

###############################################################################
# We extract the fixtures data with columns that match the columns of the
# training data. On the other hand, the fixtures data are not affected by
# the ``param_grid`` selection.

X_fix, _, O_fix = dataloader.extract_fixtures_data()

###############################################################################
# The input data:
print(X_fix)

###############################################################################
# The market average odds:
print(O_fix)
