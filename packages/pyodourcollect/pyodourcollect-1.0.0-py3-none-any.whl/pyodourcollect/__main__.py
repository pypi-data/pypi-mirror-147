# import requests
# from models import *
from .core import *
from .helpers import *
# from constants import *


if __name__ == '__main__':
    testparams = OCRequest(
        date_init='2022-04-01',
        date_end='2022-04-05',
        minAnnoy=-4,
        maxAnnoy=-4,
        minIntensity=0,
        maxIntensity=6,
        type=0,
        subtype=0
    )
    edar_besos = (41.409032, 2.222619)
    get_oc_data(testparams, 'test.csv', edar_besos)
    #  -s 2021-01-01 -e 2021-12-31 --hedonic=unpleasant
