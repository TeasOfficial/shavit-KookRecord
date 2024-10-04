# shavit-KookRecord

用于自动上传 Server Record 记录通知到 KOOK 频道。

仅支持 `@shavitush/bhoptimer`。

---

### 提示：项目需要 `Python >= 3.8  SourceMod >= 1.10` 才能运行！
运行前请修改 py 文件中必要的修改项！

```python
# 初始化 Bot 信息
bot = Bot(token="123456789")
# 请在这里填写你的 KOOK BotToken
# 如果没有Token，请先到 KOOK 开发者中心创建新的应用
# https://developer.kookapp.cn/app/index

SERVEPORT = 14725 # 服务器运行时端口

CHANNELID = "6653477553425031" # 子频道ID，务必修改！
```

若修改过上方的端口，在SourcePawn中也需要修改！

```c
// 修改此处的REMOTE_SERVER，此处将于下个版本修改为ConVar形式
#define REMOTE_SERVER "http://localhost:14725"

forward void Shavit_OnReplaySaved(int client, int style, float time, int jumps, int strafes, float sync, int track, float oldtime, float perfs, float avgvel, float maxvel, int timestamp, bool isbestreplay, bool istoolong, bool iscopy, const char[] replaypath);

HTTPClient gH_Client = null;

public Plugin myinfo = {
    name = "Teas Official Databases",
    author = "MinGW",
    description = "用于自动获取SR，并上传至 KOOK",
    version = "1.0.0",
    url = "https://nekogan.com"
}
```