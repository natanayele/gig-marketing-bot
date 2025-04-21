import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from gig_bot.handlers.marketing import forward_to_marketing
import gig_bot.config as config

@pytest.mark.asyncio
async def test_forward_valid_message():
    config.DOCUMENTATION_GROUP_ID = 1234
    config.MARKETING_GROUP_ID = 5678

    mock_msg = MagicMock()
    mock_msg.chat.id = 1234
    mock_msg.text = "/marketing Hello world!"
    mock_msg.from_user.first_name = "Tester"
    mock_msg.reply_text = AsyncMock()

    mock_update = MagicMock()
    mock_update.message = mock_msg

    mock_bot = AsyncMock()
    mock_context = MagicMock()
    mock_context.bot = mock_bot

    await forward_to_marketing(mock_update, mock_context)

    mock_bot.send_message.assert_awaited_once_with(
        chat_id=5678,
        text="[Marketing Bot]\nFrom Tester: Hello world!"
    )
    mock_msg.reply_text.assert_awaited_once_with("✅ Message forwarded to Marketing group.")

@pytest.mark.asyncio
async def test_rejects_wrong_group():
    config.DOCUMENTATION_GROUP_ID = 1234

    mock_msg = MagicMock()
    mock_msg.chat.id = 9999
    mock_msg.text = "/marketing Should not forward"
    mock_msg.reply_text = AsyncMock()

    mock_update = MagicMock()
    mock_update.message = mock_msg

    mock_context = MagicMock()

    await forward_to_marketing(mock_update, mock_context)

    mock_msg.reply_text.assert_awaited_once_with(
        "Sorry, this command is only available in the documentation group."
    )

@pytest.mark.asyncio
async def test_empty_message_handled():
    config.DOCUMENTATION_GROUP_ID = 1234

    mock_msg = MagicMock()
    mock_msg.chat.id = 1234
    mock_msg.text = "/marketing"
    mock_msg.reply_text = AsyncMock()

    mock_update = MagicMock()
    mock_update.message = mock_msg

    mock_context = MagicMock()

    await forward_to_marketing(mock_update, mock_context)

    mock_msg.reply_text.assert_awaited_once_with("Usage: /marketing <your message>")

@pytest.mark.asyncio
async def test_handler_exception_logged():
    config.DOCUMENTATION_GROUP_ID = 1234
    config.MARKETING_GROUP_ID = 5678

    mock_msg = MagicMock()
    mock_msg.chat.id = 1234
    mock_msg.text = "/marketing This will error"
    mock_msg.from_user.first_name = "Tester"
    mock_msg.reply_text = AsyncMock()

    mock_update = MagicMock()
    mock_update.message = mock_msg

    mock_bot = AsyncMock()
    mock_bot.send_message.side_effect = Exception("Simulated error")

    mock_context = MagicMock()
    mock_context.bot = mock_bot

    with patch("gig_bot.handlers.marketing.logger") as mock_logger:
        await forward_to_marketing(mock_update, mock_context)

        mock_msg.reply_text.assert_awaited_with(
            "⚠️ Something went wrong while forwarding your message."
        )
        mock_logger.exception.assert_called_once()
