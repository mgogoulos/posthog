from typing import Any, Dict, Literal, Tuple

from ee.clickhouse.models.action import format_action_filter
from ee.clickhouse.models.property import parse_prop_clauses
from posthog.constants import TREND_FILTER_TYPE_ACTIONS
from posthog.models.entity import Entity


def get_entity_filtering_params(
    entity: Entity, team_id: int, table_name: str = "", *, with_prop_filters: bool = False
) -> Tuple[Dict, Dict]:
    params: Dict[str, Any]
    content_sql_params: Dict[Literal["entity_query"], str]
    if entity.type == TREND_FILTER_TYPE_ACTIONS:
        action = entity.get_action()
        action_query, params = format_action_filter(action, table_name=table_name)
        content_sql_params = {"entity_query": "AND {action_query}".format(action_query=action_query)}
    else:
        prop_filters = ""
        params = {"event": entity.id}
        if with_prop_filters:
            prop_filters, params = parse_prop_clauses(entity.properties, team_id)
        content_sql_params = {"entity_query": f"AND event = %(event)s {prop_filters}"}

    return params, content_sql_params
