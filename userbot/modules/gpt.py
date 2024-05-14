# Copyright (C) 2019-2021 The Authors
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting the weather of a city. """

import openai
import time

from userbot import CMD_HELP
from userbot import OPENAI_API_KEY
from userbot.events import register, grp_exclude

# ===== CONSTANT =====
SYSTEM_MSG = "You are a helpful assistant that gives concise answers and responses. Use emojis. Use 🗿 emoji sometimes."
EDIT_DELAY = 0.5

@register(outgoing=True, pattern=r"^.gpt(?:\s|$)(.*)")
@grp_exclude()
async def gpt(q_event):
    """For .gpt command, do a query to openai"""
    if OPENAI_API_KEY is None:
        await q_event.edit("Please set your OPENAI_API_KEY first !\n")
        return

    textx = await q_event.get_reply_message()
    query = q_event.pattern_match[1]

    if query:
        pass
    if textx and textx.text:
        query = textx.text + "\n\n" + query

    if not query:
        await q_event.edit(
            "`Pass a query as an argument or reply to a message for AI completion!`"
        )
        return

    text: str = (q_event.pattern_match[1] or "") + "\n\n"
    await q_event.edit(text + "...")

    try:
        client = openai.OpenAI()
        stream = client.chat.completions.create(
            model="gpt-4o",
            stream=True,
            temperature=0.6,
            messages=[
                {"role": "system", "content": SYSTEM_MSG},
                {"role": "user", "content": query},
            ],
        )
        last_edit = time.time()
        last_text = text
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                text += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="")
                if time.time() >= last_edit + EDIT_DELAY and text != last_text:
                    last_edit = time.time()
                    last_text = text
                    await q_event.edit(text + "...")
    except Exception:
        await q_event.edit("There was an error")
        raise
    await q_event.edit(text)


CMD_HELP.update(
    {
        "gpt": [
            "Gpt",
            " - `.gpt [<text>]`: "
            "Send replied message or <text> to gpt-4o model."
        ]
    }
)
