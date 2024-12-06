import argparse
import logging
import sys
import json

from bw_save_game import __version__
from bw_save_game.container import *
from bw_save_game.db_object_codec import *

__author__ = "Tim Niederhausen"
__copyright__ = "Tim Niederhausen"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----


def dump_save_game_json(filename: str, output: str):
    with open(filename, 'rb') as f:
        m, d = read_save_from_reader(f)

    m = loads(m)
    d = loads(d)

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=m, data=d), f, default=str, indent=2)


def edit_save_game(filename):
    with open(filename, 'rb') as f:
        m, d = read_save_from_reader(f)

    m = loads(m)
    d = loads(d)

    #m[None]['description'] = ''

    registered_persistence = next(filter(lambda c: c['name'] == 'RegisteredPersistence', d['server']['contributors']))
    persistence_entries = registered_persistence['data']['RegisteredData']['Persistence']

    entry_to_edit = next(filter(lambda e: e['DefinitionId'] == 1250272560, persistence_entries))

    entry_to_edit['PropertyValueData']['DefinitionProperties'] = list(filter(lambda prop: ",2643758781:Int32" not in prop, entry_to_edit['PropertyValueData']['DefinitionProperties']))
    print(entry_to_edit)

    m = dumps(m)
    d = dumps(d)

    with open('out/' + filename, 'wb') as f:
        write_save_to_writer(f, m, d)


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    setup_logging(logging.DEBUG)

    dump_save_game_json('1-correct_romance_1.csav', 'xcorrect_romance_1.csav.json')
    dump_save_game_json('2-wrong_romance_1.csav', 'xwrong_romance_1.csav.json')
    dump_save_game_json('3-correct_romance_2.csav', 'xcorrect_romance_2.csav.json')
    dump_save_game_json('4-wrong_romance_2.csav', 'xwrong_romance_2.csav.json')
    dump_save_game_json('0-439591 Saria-Inquisitor #1884.csav', 'xtest.csav.json')

    edit_save_game('0-439591 Saria-baby bunny! #3123.csav')




def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m bw_save_game.skeleton 42
    #
    run()
