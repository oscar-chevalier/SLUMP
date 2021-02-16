import configparser
import slump.config.cli_parser
from pathlib import Path
from appdirs import user_config_dir, site_config_dir


class Config:
    def __init__(self, configparser):
        args = slump.config.cli_parser.parser.parse_args()

        if 'func_rec' in configparser:
            self.func_rec: bool = configparser['func_rec']
            if 'pile' in configparser:
                self.pile: bool = configparser['pile']
            else:
                self.pile: bool = True
        else:
            self.func_rec: bool = False
            self.pile: bool = False

    def get_config(self, args):
        if args.config is not None:
            config_path = Path(args.config)
            if config_path.is_file():
                return config_path
            else:
                print('Path is not correct.')
        return self.search_config()

    @staticmethod
    def search_config():
        name_candidates = ['slump.config', '.slumprc', 'slump_config']
        path_candidates = [
            Path('.'),
            Path(user_config_dir('slump', 'slump')),
            Path.home(),
            Path(site_config_dir('slump', 'slump')),
        ]
        for path_candidate in path_candidates:
            for name_candidate in name_candidates:
                if (path_candidate / name_candidate).is_file():
                    return path_candidate / name_candidate
        return None
