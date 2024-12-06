from typing import Annotated

from typing_extensions import Doc

from emp_agents.models.protocol import SkillSet, tool_method

from .actions import make_poll, make_tweet, make_tweet_with_image, reply_to_tweet


class TwitterSkill(SkillSet):
    """
    Skill for interacting with Twitter API
    """

    @tool_method
    @staticmethod
    async def make_tweet(
        content: Annotated[str, Doc("The content of the tweet to be made.")]
    ) -> str:
        """Make a tweet"""
        return await make_tweet(content)

    @tool_method
    @staticmethod
    async def make_tweet_with_image(
        content: Annotated[str, Doc("The content of the tweet to be made.")]
    ) -> str:
        """Make a tweet with an image"""
        return await make_tweet_with_image(content)

    @tool_method
    @staticmethod
    async def make_poll(
        content: Annotated[str, Doc("The content of the tweet to be made.")]
    ) -> str:
        """Make a poll"""
        return await make_poll(content)

    @tool_method
    @staticmethod
    async def reply_to_tweet(
        tweet_id: Annotated[int, Doc("The ID of the tweet to reply to.")],
        content: Annotated[str, Doc("The content of the tweet to be made.")],
    ) -> str:
        """Reply to a tweet"""
        return await reply_to_tweet(tweet_id, content)
