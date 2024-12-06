MEMORY_WORD_COUNT_LIMIT = 300

INNER_THOUGHT_TAG = "INNER_THOUGHT_MONOLOGUE"
SYSTEM_INSTRUCTION_LABEL = "*Elroy System Instruction*"

UNKNOWN = "Unknown"
MEMORY_TITLE_EXAMPLES = """
Examples of good and bad memory titles are below. Note, the BETTER examples, some titles have been split into two.:

BAD:
- [User Name]'s project progress and personal goals: 'Personal goals' is too vague, and the title describes two different topics.

BETTER:
- [User Name]'s project on building a treehouse: More specific, and describes a single topic.
- [User Name]'s goal to be more thoughtful in conversation: Describes a specific goal.

BAD:
- [User Name]'s weekend plans: 'Weekend plans' is too vague, and dates must be referenced in ISO 8601 format.

BETTER:
- [User Name]'s plan to attend a concert on 2022-02-11: More specific, and includes a specific date.

BAD:
- [User Name]'s preferred name and well being: Two different topics, and 'well being' is too vague.

BETTER:
- [User Name]'s preferred name: Describes a specific topic.
- [User Name]'s feeling of rejuvenation after rest: Describes a specific topic.
"""

CLI_USER_ID = 1

### Model parameters ###

# TODO: make this dynamic
EMBEDDING_SIZE = 1536


RESULT_SET_LIMIT_COUNT = 5

REPO_LINK = "https://github.com/elroy-bot/elroy/issues"


class MissingAssistantToolCallError(Exception):
    pass


class MissingToolCallMessageError(Exception):
    pass


class MissingSystemInstructError(Exception):
    pass


class MisplacedSystemInstructError(Exception):
    pass
