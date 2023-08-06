""" mcli run Entrypoint """
import argparse
import logging
import textwrap
from typing import List, Optional

from mcli import config
from mcli.models.run import RunModel
from mcli.runs import pipeline
from mcli.submit.kubernetes.runners import Runner
from mcli.submit.kubernetes.runners_future import Runner as RunnerFuture
from mcli.submit.platforms_future.experimental import ExperimentalFlag
from mcli.submit.platforms_future.registry import PlatformRegistry as PlatformRegistryFuture

logger = logging.getLogger(__name__)


def run(
    file: Optional[str] = None,
    experimental: Optional[List[ExperimentalFlag]] = None,
    **kwargs,
) -> int:
    del kwargs
    logger.info(
        textwrap.dedent("""
    ------------------------------------------------------
    Let's run this run
    ------------------------------------------------------
    """))

    partial_run_model = pipeline.create_partial_run_models(file=file,)

    # merge the partial run models into a single complete run model
    run_model = RunModel.from_partial_run_model(partial_run_model)
    #-
    # convert the run model into a mcli job object
    mcli_job = pipeline.mcli_job_from_run_model(run_model)

    # Write the run to the MAPI DB if enabled
    if config.feature_enabled(config.FeatureFlag.USE_FEATUREDB):
        # pylint: disable-next=import-outside-toplevel
        from mcli.api.runs.create_run import create_run
        if not create_run(run_model):
            print('Failed to persist run')

    if config.feature_enabled(config.FeatureFlag.USE_PLATFORMS_FUTURE):
        # TODO(HEK-323): Refactor so this hack isn't necessary to get the platform
        registry = PlatformRegistryFuture()
        platform, instance_type = registry.get_mcli_platform_and_instance_type(instance_str=run_model.instance,)
        # END TODO(HEK-323):
        runner = RunnerFuture()
        runner.submit(
            job=mcli_job,
            instance=instance_type,
            platform=platform,
            experimental_flags=experimental,
        )
    else:
        runner = Runner()
        runner.submit(
            mcli_job,  # type: ignore
            run_model.instance,
        )
    print('Submitted job')
    return 0


def add_run_argparser(subparser: argparse._SubParsersAction) -> None:
    run_parser: argparse.ArgumentParser = subparser.add_parser(
        'run',
        aliases=['r'],
        help='Run stuff',
    )
    run_parser.set_defaults(func=run)
    _configure_parser(run_parser)


def _configure_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        '-f',
        '--file',
        dest='file',
        help='File from which to load arguments.',
    )

    parser.add_argument(
        '--experimental',
        choices=ExperimentalFlag.permitted(),
        type=ExperimentalFlag,
        nargs='+',
        default=None,
        metavar='FLAG',
        help=
        'Enable one or more experimental flags. These flags are designed to take advantage of a specific feature that '
        'may still be too experimental for long-term inclusion in mcli.')
