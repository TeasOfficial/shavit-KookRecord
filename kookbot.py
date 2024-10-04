"""

            KOOK Bot 2024/10/04
                USE khl.py
        Delevoped by OriginalSnow

"""

import asyncio
from aiohttp import web,ClientSession
from khl import Bot
from khl.card import Card, CardMessage, Module, Types, Element, Struct
import json

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

DEBUGMODE = False

# 初始化 Bot 信息
bot = Bot(token="123456789")
# 请在这里填写你的 KOOK BotToken
# 如果没有Token，请先到 KOOK 开发者中心创建新的应用
# https://developer.kookapp.cn/app/index

SERVEPORT = 8080
# 服务器运行时端口

routes = web.RouteTableDef()

@routes.post("/")
async def hello_world(request):
    if DEBUGMODE: print("您有新的美团订单，请及时查看：")
    data = await request.json()
    
    avatarurl = None

    _sjc = None
    if (float(data["time"]) - float(data["oldtime"])) == data["time"]:
        _sjc = "(新纪录)"
    elif(float(data["time"]) > float(data["oldtime"])):
        _sjc = f"(+%.3f)"%( float(data["time"]) - float(data["oldtime"]) )
    else:
        _sjc = f"(-%.3f)"%( float(data["oldtime"]) - float(data["time"]) )

    async with ClientSession() as session:
        async with session.get(f"http://mapi.gmod.ltd:54010/avatar.php?steamid=%s"%data["steamid64"]) as resp:
            avatarurl = await resp.text()


    ch = await bot.client.fetch_public_channel("6653477553425031")
    cm = CardMessage()
    c = Card(
        Module.Header(data['map']),
        Module.Divider(),
        Module.Section(
            Struct.Paragraph(
                2,
                Element.Text(f"**昵称**\n[%s](https://steamcommunity.com/profiles/%s)" % (data["name"].encode().decode(), data["steamid"].encode().decode()), type=Types.Text.KMD),
                Element.Text(f"**用时**\n%.3f %s"%(data["time"], _sjc), type=Types.Text.KMD),
                Element.Text(f"**SteamID**\n%s"%(data["steamid"]), type=Types.Text.KMD),
            ),
            Element.Image(src=avatarurl),
            mode=Types.SectionMode.RIGHT
        ),
        Module.Divider(),
        Module.Section("**详细信息**"),
        Module.Section(
            Struct.Paragraph(
                3,
                Element.Text(f"**加速次数**\n%d"%data["strafes"], type=Types.Text.KMD),
                Element.Text(f"**同步率**\n%.1f"%data["sync"], type=Types.Text.KMD),
                Element.Text(f"**跳跃次数**\n%d"%data["jumps"], type=Types.Text.KMD)
            )
        ),
        Module.Divider(),
        Module.Context(
            Element.Text(f"记录时间：%s"%(data["date"]), Types.Text.PLAIN)
        ),
        Module.Context("Powered by 吕小鱼鱼#0001"),
        color="#FAA0F5"
    )
    cm.append(c)

    if DEBUGMODE: print(json.dumps(cm))

    await ch.send(cm)
    return web.Response(body="success")

# 添加 route
app = web.Application()
app.add_routes(routes)

# 同时运行 app 和 bot
HOST,PORT = '0.0.0.0',SERVEPORT
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(
        asyncio.gather(
            web._run_app(app, host=HOST, port=PORT),
            bot.start()
        )
    )