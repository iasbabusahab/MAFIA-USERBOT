# by unibot...Thanks @spechide
# Now will be used in MafiaBot too....
import asyncio
import datetime
from datetime import datetime

from telethon import events
from telethon.tl import functions, types
from userbot import CMD_HELP, mafiaversion
from mafiabot.utils import admin_cmd, edit_or_reply
from userbot.cmdhelp import CmdHelp
from userbot.Config import Config
from . import *

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "Mafia User"

mafia = bot.uid


global USER_AFK  # pylint:disable=E0602
global afk_time  # pylint:disable=E0602
global last_afk_message  # pylint:disable=E0602
global afk_start
global afk_end
USER_AFK = {}
afk_time = None
last_afk_message = {}
afk_start = {}


@bot.on(events.NewMessage(outgoing=True))  # pylint:disable=E0602
async def set_not_afk(event):
    if event.fwd_from:
        return
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global last_afk_message  # pylint:disable=E0602
    global afk_start
    global afk_end
    came_back = datetime.datetime.now()
    afk_end = came_back.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    current_message = event.message.message
    if ".afk" not in current_message and "yes" in USER_AFK:  # pylint:disable=E0602
        mafiabot = await bot.send_message(
            event.chat_id,
            "🔥__Back alive!__\n**No Longer afk.**\n⏱️ `Was afk for:``"
            + total_afk_time
            + "`", file=mafiapic
        )
        try:
            await bot.send_message(  # pylint:disable=E0602
                Config.MAFIABOT_LOGGER,  # pylint:disable=E0602
                "#AFKFALSE \nSet AFK mode to False\n"
                + "🔥__Back alive!__\n**No Longer afk.**\n⏱️ `Was afk for:``"
                + total_afk_time
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await bot.send_message(  # pylint:disable=E0602
                event.chat_id,
                "Please set `BOT_LOGGER` "
                + "for the proper functioning of afk functionality "
                + "Ask in @iasbabu_official to get help setting this value\n\n `{}`".format(str(e)),
                reply_to=event.message.id,
                silent=True,
            )
        await asyncio.sleep(5)
        await mafiabot.delete()
        USER_AFK = {}  # pylint:disable=E0602
        afk_time = None  # pylint:disable=E0602


@bot.on(
    events.NewMessage(  # pylint:disable=E0602
        incoming=True, func=lambda e: bool(e.mentioned or e.is_private)
    )
)
async def on_afk(event):
    if event.fwd_from:
        return
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global last_afk_message  # pylint:disable=E0602
    global afk_start
    global afk_end
    cum_back = datetime.datetime.now()
    afk_end = cum_back.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return False
    if USER_AFK and not (await event.get_sender()).bot:
        msg = None
        
        message_to_reply = (
            f"Hey!! My Legend master [{DEFAULTUSER}](tg://user?id={mafia}) is currently offline... Since when?\n**For** `{total_afk_time}`\n"
            + f"\n\n👇__The Reason Is__👇 :-\n`{reason}`"
  if reason
            else f"**Heyy!**\n__I am currently unavailable.__\n__Since when, you ask? From__ `{total_afk_time}`\nI'll be back when I feel to come🚶"
        )
        msg = await event.reply(message_to_reply, file=mafiapic)
        await asyncio.sleep(2)
        if event.chat_id in last_afk_message:  # pylint:disable=E0602
            await last_afk_message[event.chat_id].delete()  # pylint:disable=E0602
        last_afk_message[event.chat_id] = msg  # pylint:disable=E0602


@bot.on(admin_cmd(pattern=r"afk (.*)", outgoing=True))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    h1m4n5hu0p = await event.get_reply_message()
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global last_afk_message  # pylint:disable=E0602
    global afk_start
    global afk_end
    global reason
    global mafiapic
    USER_AFK = {}
    afk_time = None
    last_afk_message = {}
    afk_end = {}
    start_1 = datetime.datetime.now()
    afk_start = start_1.replace(microsecond=0)
    reason = event.pattern_match.group(1)
    mafiapic = await event.client.download_media(h1m4n5hu0p)
    if not USER_AFK:  # pylint:disable=E0602
        last_seen_status = await bot(  # pylint:disable=E0602
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            afk_time = datetime.datetime.now()  # pylint:disable=E0602
        USER_AFK = f"yes: {reason} {mafiapic}"  # pylint:disable=E0602
        if reason:
            await bot.send_message(
                event.chat_id, f"__**I'm going afk🚶**__ \n⚜️ Because `{reason}`", file=mafiapic
            )
        else:
            await bot.send_message(event.chat_id, f"**I am Going afk!**🚶", file=mafiapic)
        await asyncio.sleep(0.001)
        await event.delete()
        try:
            await bot.send_message(  # pylint:disable=E0602
                Config.MAFIABOT_LOGGER,  # pylint:disable=E0602
                f"#AFKTRUE \nSet AFK mode to True, and Reason is {reason}",file=mafiapic
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            logger.warn(str(e))  # pylint:disable=E0602


CmdHelp("afk").add_command(
  'afk', '<reply to media>/<or type a reson>', 'Marks you AFK(Away from Keyboard) with reason(if given) also shows afk time. Media also supported.'
).add()
