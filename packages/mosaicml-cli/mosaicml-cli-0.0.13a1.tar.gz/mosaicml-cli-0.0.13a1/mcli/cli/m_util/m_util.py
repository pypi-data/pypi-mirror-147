""" CLI Get options"""
import argparse

from mcli import config
from mcli.cli.m_util.util import get_util


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.set_defaults(func=get_util, parser=parser)
    conf = config.MCLIConfig.load_config()
    registered_platforms = conf.platforms
    registered_platform_names = [x.name for x in registered_platforms] + ['all']
    parser.add_argument(
        'platform',
        choices=registered_platform_names,
        default=registered_platform_names[0],
        help='What platform would you like to get util for?',
    )

    return parser


def add_util_argparser(subparser: argparse._SubParsersAction,) -> argparse.ArgumentParser:
    """Adds the get parser to a subparser

    Args:
        subparser: the Subparser to add the Util parser to
    """

    util_parser: argparse.ArgumentParser = subparser.add_parser(
        'util',
        help='Get cluster util',
    )
    util_parser = configure_argparser(parser=util_parser)
    return util_parser
