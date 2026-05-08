import os
import asyncio
import dns.resolver

from aiohttp import web
from pyrogram import idle

from . import app, log


# ---------------- DNS FIX ---------------- #

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']


# ---------------- HEALTH CHECK SERVER ---------------- #

async def health(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    web_app = web.Application()
    web_app.router.add_get("/", health)

    runner = web.AppRunner(web_app)
    await runner.setup()

    port = int(os.environ.get("PORT", 8080))

    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"Web server started on port {port}")


# ---------------- MAIN BOT ---------------- #

async def main():

    # Start Koyeb web server
    await start_web_server()

    # Start Telegram bot
    await app.start()

    me = await app.get_me()

    # Send startup message
    await app.send_message(
        chat_id=log,
        text=f'<b>Bot Started! @{me.username}</b>'
    )

    print(f"Bot started as @{me.username}")

    # Keep alive
    await idle()

    # Stop bot
    await app.stop()


# ---------------- START ---------------- #

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
