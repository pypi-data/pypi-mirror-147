""" Run Schema """
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

from mcli.api.engine.utils import dedent_indent
from mcli.api.schema.generic_model import DeserializableModel
from mcli.models.run import RunStatus


@dataclass
class GraphQLRunType(DeserializableModel):
    """ GraphQL run type """

    run_uid: str
    run_name: str
    run_status: RunStatus
    created_by_id: str
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    tags: List[str] = field(default_factory=list)

    # TODO: make this a dataclass type that is serializable
    run_config: Dict[str, Any] = field(default_factory=dict)

    property_translations = {
        'runUid': 'run_uid',
        'runName': 'run_name',
        'runConfig': 'run_config',
        'runStatus': 'run_status',
        'createdById': 'created_by_id',
        'createdAt': 'created_at',
        'updatedAt': 'updated_at',
        'isDeleted': 'is_deleted',
    }


def get_run_schema(indentation: int = 2,):
    """ Get the GraphQL schema for a :type RunModel:

    Args:
        indentation (int): Optional[int] for the indentation of the block

    Returns:
        Returns a GraphQL string with all the fields needed to initialize a
        :type RunModel:
    """
    return dedent_indent(
        """
runUid
runName
runConfig
runStatus
tags
createdById
createdAt
updatedAt
isDeleted
        """, indentation)
