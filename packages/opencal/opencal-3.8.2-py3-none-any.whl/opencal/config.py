import logging
import os
from pathlib import Path
import tomllib


DEFAULT_CONFIG_PATH: Path = Path.home() / ".opencal.toml"

DEFAULT_CONFIG_STR: str = f"""# OpenCAL configuration file

###############################################################################
# OpenCAL                                                                     #
###############################################################################

[opencal]
db_path = "~/.opencal.sqlite"
pkb_path = "~/opencal.pkb"
db_assets_path = "~/.opencal/assets"
sqlite_backup_dir_path = "~/data_opencal"
sqlite_dump_file_path = "~/data_opencal/opencal.sql"
consolidation_professor = "doreen"
acquisition_professor = "arthur"

[opencal.professors.arthur]
cards_in_progress_increment_size = 5
right_answers_rate_threshold = 0.5

[opencal.professors.doreen]
max_cards_per_grade = 50

[[opencal.professors.doreen.priorities_per_level.0]]
sort_fn = "tag"
reverse = true

[[opencal.professors.doreen.priorities_per_level.0]]
sort_fn = "date"
reverse = true

[[opencal.professors.doreen.priorities_per_level.5]]
sort_fn = "tag"
reverse = true

[[opencal.professors.doreen.priorities_per_level.5]]
sort_fn = "date"
reverse = true

[[opencal.professors.doreen.priorities_per_level.6]]
sort_fn = "tag"
reverse = true

[[opencal.professors.doreen.priorities_per_level.6]]
sort_fn = "date"
reverse = true

[[opencal.professors.doreen.priorities_per_level.7]]
sort_fn = "tag"
reverse = true

[[opencal.professors.doreen.priorities_per_level.7]]
sort_fn = "date"
reverse = true

[[opencal.professors.doreen.priorities_per_level.8]]
sort_fn = "tag"
reverse = true

[[opencal.professors.doreen.priorities_per_level.8]]
sort_fn = "date"
reverse = true

[[opencal.professors.doreen.priorities_per_level.9]]
sort_fn = "tag"
reverse = true

[[opencal.professors.doreen.priorities_per_level.9]]
sort_fn = "date"
reverse = true

[[opencal.professors.doreen.priorities_per_level.10]]
sort_fn = "tag"
reverse = true

[[opencal.professors.doreen.priorities_per_level.10]]
sort_fn = "date"
reverse = true

[[opencal.professors.doreen.priorities_per_level.default]]
sort_fn = "tag"
reverse = true

[opencal.professors.common.tag_priorities]
"important" = 3
"superflu" = 0.5

[opencal.professors.common.tag_difficulties]
"facile" = 0.5
"difficile" = 2.0

###############################################################################
# OpenCAL UI                                                                  #
###############################################################################

[opencal_ui]
html_scale = 1.0
mathjax_path = "/usr/share/javascript/mathjax"

[opencal_ui.qtme]
default_html_base_path = "~/.opencal/assets"
"""


def get_config(config_path: Path | str | None = None) -> tuple[dict, Path]:
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
            config_path = DEFAULT_CONFIG_PATH

    # Expand the user's home directory
    config_path = Path(config_path).expanduser()   # Replace '~' with the user's home directory

    # Make sure the configuration file exists
    if not config_path.exists():
        logging.warning(f"The configuration file '{config_path}' does not exist.")
        make_default_config_file(config_path)

    # Read the TOML file
    with open(config_path, 'rb') as file:
        logging.info(f'Loading OpenCAL configuration: "{config_path}"')
        config_dict = tomllib.load(file)

    return config_dict, config_path


def make_default_config_file(config_path: Path | str | None = None) -> None:
    """
    Make a default configuration file.

    Parameters
    ----------
    config_path : Path, optional
        The path to the configuration file.
    """
    if config_path is None:
        if 'OPENCAL_TOML_CONFIG_PATH' in os.environ:
            config_path = Path(os.environ['OPENCAL_TOML_CONFIG_PATH'])
        else:
            config_path = DEFAULT_CONFIG_PATH

    # Expand the user's home directory
    config_path = Path(config_path).expanduser()   # Replace '~' with the user's home directory

    if not config_path.exists():
        config_path.write_text(DEFAULT_CONFIG_STR)