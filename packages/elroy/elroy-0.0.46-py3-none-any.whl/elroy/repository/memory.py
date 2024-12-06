import logging
from typing import List, Optional, Tuple

from sqlmodel import select

from ..config.config import ChatModel, ElroyContext
from ..config.constants import MEMORY_TITLE_EXAMPLES, MEMORY_WORD_COUNT_LIMIT
from ..llm.client import query_llm, query_llm_json
from ..repository.data_models import ContextMessage, Memory

MAX_MEMORY_LENGTH = 12000  # Characters


def memory_to_fact(memory: Memory) -> str:
    return f"#{memory.name}\n{memory.text}"


def manually_record_user_memory(context: ElroyContext, text: str, name: Optional[str] = None) -> None:
    """Manually record a memory for the user.

    Args:
        context (ElroyContext): The context of the user.
        name (str): The name of the memory. Should be specific and discuss one topic.
        text (str): The text of the memory.
    """

    if not text:
        raise ValueError("Memory text cannot be empty.")

    if len(text) > MAX_MEMORY_LENGTH:
        raise ValueError(f"Memory text exceeds maximum length of {MAX_MEMORY_LENGTH} characters.")

    if not name:
        name = query_llm(
            context.config.chat_model,
            system="Given text representing a memory, your task is to come up with a short title for a memory. "
            "If the title mentions dates, it should be specific dates rather than relative ones.",
            prompt=text,
        )

    create_memory(context, name, text)


async def formulate_memory(chat_model: ChatModel, user_preferred_name: str, context_messages: List[ContextMessage]) -> Tuple[str, str]:
    from ..llm.prompts import summarize_for_memory
    from ..messaging.context import format_context_messages

    return await summarize_for_memory(
        chat_model,
        user_preferred_name,
        format_context_messages(user_preferred_name, context_messages),
    )


async def consolidate_memories(context: ElroyContext, memory1: Memory, memory2: Memory):

    if memory1.text == memory2.text:
        logging.info(f"Memories are identical, marking memory with id {memory2.id} as inactive.")
        memory2.is_active = False
        context.session.add(memory2)
        context.session.commit()
    else:

        context.io.internal_thought_msg("Consolidating memories '{}' and '{}'".format(memory1.name, memory2.name))
        response = query_llm_json(
            system=f"""Your task is to consolidate or reorganize two pieces of text.
            Each pice of text has a title and a main body. You should either combine the titles and the main bodies into a single title and main body, or create multiple title/text combinations with distinct information.
            The new bodies should not exceed {MEMORY_WORD_COUNT_LIMIT} words.
            If referring to dates and times, use use ISO 8601 format, rather than relative references. It is critical that when applicable, specific absolute dates are retained.

            If the two texts are redunant, but they together discuss distinct topics, you can create multiple new texts rather than just one.
            One hint that multiple texts are warranted is if the title has the word 'and', and can reasonably be split into two titles.
            Above all, ensure that each consolidate text has one basic topic, and that the text is coherent.

            {MEMORY_TITLE_EXAMPLES}

            Return your response in JSON format, with the following structure:
            - REASONING: an explanation of your reasoning how you chose to consolidate or reorganize the texts. This must include information about what factored into your decision about whether to output one new texts, or multiple.
            - NEW_TEXTS: Key to contain the new text or texts. This should be a list, each of which should have the following keys:
               - TITLE: the title of the consolidated memory
               - TEXT: the consolidated memory


            An example response that consolidates memories into one might look like:
            {{
                "REASONING": "I chose to consolidate the two memories into one because they both discuss the same topic.",
                "NEW_TEXTS": [
                    "TITLE": "Consolidated memory title",
                    "TEXT": "Consolidated memory text"
                ]
            }}

            An example response that might consolidate memories into multiple new ones might look like:

            {{
                "REASONING": "I chose to consolidate the two memories into multiple because they discuss distinct topics.",
                "NEW_TEXTS": [
                    {{
                        "TITLE": "Consolidated memory title 1",
                        "TEXT": "Consolidated memory text 1"
                    }},
                    {{
                        "TITLE": "Consolidated memory title 2",
                        "TEXT": "Consolidated memory text 2"
                    }}
                ]
            }}
            """,
            prompt="\n".join(
                [
                    f"Title 1: {memory1.name}",
                    f"Text 1: {memory1.text}",
                    f"Title 2: {memory2.name}",
                    f"Text 2: {memory2.text}",
                ],
            ),
            model=context.config.chat_model,
        )
        assert isinstance(response, dict), f"Memory consolidation function expected a dict, but received: {response}"

        new_texts = response["NEW_TEXTS"]  # type: ignore

        if isinstance(new_texts, dict):
            new_texts = [new_texts]

        logging.info(f"REASONING: {response['REASONING']}")

        new_ids = []
        for new_text in new_texts:
            new_name = new_text.get("TITLE")
            new_text = new_text.get("TEXT")

            assert new_name, "New memory title is empty, expected non empty string under key TITLE"
            assert new_text, "New memory text is empty, expected non empty string under key TEXT"
            new_ids.append(create_memory(context, new_name, new_text))

        logging.info(f"New memory id's = {new_ids}")

        logging.info(f"Consolidating into {len(new_texts)} new memories")
        logging.info(f"marked memory with id {memory1.id} and {memory2.id} as inactive.")

        mark_memory_inactive(context, memory1)
        mark_memory_inactive(context, memory2)


def mark_memory_inactive(context: ElroyContext, memory: Memory):
    from ..messaging.context import remove_from_context

    memory.is_active = False
    context.session.add(memory)
    context.session.commit()
    remove_from_context(context, memory)


def create_memory(context: ElroyContext, name: str, text: str) -> int:
    """Creates a new memory for the assistant.

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

    Args:
        context (ElroyContext): _description_
        name (str): The name of the memory. Should be specific and discuss one topic.
        text (str): The text of the memory.

    Returns:
        int: The database ID of the memory.
    """
    from ..messaging.context import add_to_context

    memory = Memory(user_id=context.user_id, name=name, text=text)
    context.session.add(memory)
    context.session.commit()
    context.session.refresh(memory)
    from ..repository.embeddings import upsert_embedding

    memory_id = memory.id
    assert memory_id

    upsert_embedding(context, memory)
    add_to_context(context, memory)

    return memory_id


def get_active_memories(context: ElroyContext) -> List[Memory]:
    """Fetch all active memories for the user"""
    return list(
        context.session.exec(
            select(Memory).where(
                Memory.user_id == context.user_id,
                Memory.is_active == True,
            )
        ).all()
    )
