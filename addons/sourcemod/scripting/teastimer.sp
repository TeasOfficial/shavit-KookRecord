#include <sourcemod>
#include <ripext>

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

public void OnAllPluginsLoaded(){
    PrintToServer("[Teas Official] Databases Plugin Loaded, this plugin only support Shavit Timer!!!")
    gH_Client = new HTTPClient(REMOTE_SERVER);
}

public void Shavit_OnReplaySaved(int client, int style, float time, int jumps, int strafes, float sync, int track, float oldtime, float perfs, float avgvel, float maxvel, int timestamp, bool isbestreplay, bool istoolong, bool iscopy, const char[] replaypath){
    if(style != 0 || track != 0){
        // 禁止发送非 normal 的数据
        return
    }

    // 获取当前用户 Steam 名称
    char sName[MAX_NAME_LENGTH]
    GetClientName(client, sName, sizeof(sName))

    // 获取当前用户 SteamID
    char sSteamID[32]
    GetClientAuthId(client, AuthId_Steam3, sSteamID, sizeof(sSteamID))

    // 获取当前用户 SteamID64
    char sSteamID64[32]
    GetClientAuthId(client, AuthId_SteamID64, sSteamID64, sizeof(sSteamID64))

    // 获取当前地图
    char sMap[64]
    GetCurrentMap(sMap, sizeof(sMap))
    GetMapDisplayName(sMap, sMap, sizeof(sMap))

    // 获取记录时间
    char sDate[32]
    FormatTime(sDate, sizeof(sDate), "%Y-%m-%d %H:%M:%S", GetTime())
    JSONObject _json = new JSONObject()
    
    _json.SetString("map", sMap)
    _json.SetString("name", sName)
    _json.SetString("steamid", sSteamID)
    _json.SetString("date", sDate)
    _json.SetInt("jumps", jumps)
    _json.SetInt("strafes", strafes)
    _json.SetFloat("time", time)
    _json.SetFloat("oldtime", oldtime)
    _json.SetFloat("sync", sync)
    _json.SetString("steamid64", sSteamID64)

    gH_Client.Post("", _json, Callback_OnPost)
    delete _json;
}

public void Callback_OnPost(HTTPResponse response, any value){
    if(view_as<int>(response.Status) != 200 ){
        return
    }
}