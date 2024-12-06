#from dataclasses import dataclass
import logging
import os
from pathlib import Path
import random
import string
import tomllib
from typing import Tuple, Dict, Any
try:
    import yaml
except ImportError:
    logging.warning("PyYAML is not installed. Please install it using 'pip install pyyaml'.")

import opencal.path


DEFAULT_CONFIG_PATH: str = "~/.opencal.yml"
DEFAULT_TOML_CONFIG_PATH: str = "~/.opencal.toml"

DEFAULT_CONFIG_STR: str = f"""# OpenCAL configuration file

opencal:

    db_path: "~/.opencal.sqlite"

    # The directory containing assets (images, video, audio, ...) stored in the database
    db_assets_path: "~/.opencal/assets"

    sqlite_backup_dir_path: "~/data_opencal"
    sqlite_dump_file_path: "~/data_opencal/opencal.sql"

    # Unique key of the shared memory used to prevent more than one instance of the application
    shm_key: "{ ''.join(random.choice(string.ascii_letters) for _ in range(16)) }"

    # Consolidation professor
    # Possible choices are: alice, berenice, celia, doreen
    consolidation_professor: doreen

    # Acquisition professor
    # Possible choices are: ralf, randy, arthur
    acquisition_professor: arthur

    professors:

        arthur:

            active_list_increment_size: 5

        berenice:

            max_cards_per_grade: 5
            reverse_level_0: true

        celia:

            max_cards_per_grade: 5
            reverse_level_0: true

        doreen:

            max_cards_per_grade: 5
            priorities_per_level:
                0:
                    - sort_fn: "tag"
                      reverse: True
                    - sort_fn: "date"
                      reverse: True
                default:
                    - sort_fn: "tag"
                      reverse: True

        common:

            tag_priorities:
                important: 3
                superflu: 0.5
                todo: 0.5

            tag_difficulties:
                easy: 0.5
                facile: 0.5
                hard: 2.0
                difficile: 2.0

opencal_ui:

    html_scale: 1.0

    mathjax_path: /usr/share/javascript/mathjax

    qtme:

        # The directory containing assets (images, video, audio, ...) rendered in HTML views
        default_html_base_path: "~/.opencal/assets"
"""


# # Dataclass: c.f. https://docs.python.org/3/library/dataclasses.html and https://stackoverflow.com/questions/31252939/changing-values-of-a-list-of-namedtuples/31253184
# @dataclass
# class Config:
#     pkb_path: str
#     pkb_medias_path: str
#     mathjax_path: str
#     html_scale: float
#     consolidation_professor: str
#     acquisition_professor: str
#     active_list_increment_size: int
#     max_cards_per_grade: int
#     tag_priority_dict: dict
#     tag_difficulty_dict: dict
#     reverse_level_0: bool
#     default_html_base_path: str

def get_config(config_path: str = None) -> Tuple[Dict[Any, Any], str]:
    """
    Get the configuration dictionary and the path to the configuration file.

    Parameters
    ----------
    config_path : str, optional
        The path to the configuration file.

    Returns
    -------
    (dict, str)
        The configuration dictionary and the path to the configuration file.
    """
    if config_path is None:
        if 'OPENCAL_CONFIG_PATH' in os.environ:
            config_path = os.environ['OPENCAL_CONFIG_PATH']
        else:
            config_path = DEFAULT_CONFIG_PATH

    config_path = opencal.path.expand_path(config_path)

    # Make sure the configuration file exists
    if not os.path.exists(config_path):
        make_default_config_file(config_path)

    with open(config_path) as stream:
        config_dict = yaml.safe_load(stream)
        # config = Config(**config_dict)

    return config_dict, config_path


def get_toml_config(config_path: Path | None = None) -> tuple[dict, Path]:
    """
    Get the configuration dictionary and the path to the configuration file.

    Parameters
    ----------
    config_path : Path, optional
        The path to the configuration file.
    
    Returns
    -------
    dict
        The configuration dictionary.
    """
    if config_path is None:
        if 'OPENCAL_TOML_CONFIG_PATH' in os.environ:
            config_path = Path(os.environ['OPENCAL_TOML_CONFIG_PATH'])
        else:
            config_path = Path(DEFAULT_TOML_CONFIG_PATH)

    # Expand the user's home directory
    config_path = Path(config_path).expanduser()   # Replace '~' with the user's home directory

    # Make sure the configuration file exists
    if not config_path.exists():
        logging.error(f"The configuration file '{config_path}' does not exist.")

    # Read the TOML file
    with open(config_path, 'rb') as file:
        config_dict = tomllib.load(file)

    # # Create a dynamic model
    # pydantic_model = pydantic.create_model('DynamicConfig', **{k: (Any, v) for k, v in config_dict.items()})
    # config = pydantic_model(**config_dict)

    return config_dict, config_path


def make_default_config_file(config_path: str = None):
    """
    Make a default configuration file.

    Parameters
    ----------
    config_path : str, optional
        The path to the configuration file.
    """    
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH

    config_path = opencal.path.expand_path(config_path)
    
    if not os.path.exists(config_path):
        with open(config_path, 'w') as stream:
            stream.write(DEFAULT_CONFIG_STR)
