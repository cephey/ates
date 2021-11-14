import logging

logger = logging.getLogger(__name__)


def parse_title(raw_title: str) -> tuple[str, str]:
    title, jira_id = raw_title, ''

    if ('[' in title) and (']' in title):
        try:
            jira_id, title = title.split(']')
            jira_id = jira_id.strip().split('[')[1].strip()
            title = title.strip()
            if title.startswith('-'):
                title = title[1:].strip()
        except Exception as exc:
            logger.error(str(exc))

    return title, jira_id
