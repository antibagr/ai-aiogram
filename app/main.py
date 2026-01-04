"""Aiogram bot entrypoint with streaming responses."""

import asyncio
import logging

import aiogram
import aiogram.filters
import aiogram.types
import pydantic_ai
import pydantic_ai.models.openai

import app.settings


def build_agent(settings: app.settings.Settings) -> pydantic_ai.Agent:
    """Create a PydanticAI agent configured for streaming chat."""
    model = pydantic_ai.models.openai.OpenAIModel(
        settings.openai_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
    )
    return pydantic_ai.Agent(
        model,
        system_prompt=(
            "You are a helpful assistant. Keep responses concise and friendly."
        ),
    )


async def stream_reply(
    bot: aiogram.Bot,
    message: aiogram.types.Message,
    agent: pydantic_ai.Agent,
) -> None:
    """Stream LLM text chunks to the user using sendMessageDraft."""
    if not message.text:
        return

    collected_parts: list[str] = []

    async with agent.run_stream(message.text) as result:
        async for chunk in result.stream_text(delta=True):
            if not chunk:
                continue
            collected_parts.append(chunk)
            await bot(
                aiogram.methods.SendMessageDraft(
                    chat_id=message.chat.id,
                    text=chunk,
                )
            )

    final_text = "".join(collected_parts).strip()
    if final_text:
        await message.answer(final_text)


async def main() -> None:
    """Run the bot polling loop."""
    logging.basicConfig(level=logging.INFO)

    settings = app.settings.Settings()
    bot = aiogram.Bot(token=settings.bot_token)
    dispatcher = aiogram.Dispatcher()
    router = aiogram.Router()
    dispatcher.include_router(router)

    agent = build_agent(settings)

    @router.message(aiogram.filters.CommandStart())
    async def start_handler(message: aiogram.types.Message) -> None:
        """Describe how the bot behaves."""
        await message.answer(
            "Send me a message and I'll stream back a response powered by OpenAI. "
            "You'll see draft chunks appear as they are generated, followed by the "
            "final reply."
        )

    @router.message(aiogram.filters.Text())
    async def text_handler(message: aiogram.types.Message) -> None:
        """Handle user text messages with streaming LLM responses."""
        await stream_reply(bot, message, agent)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
