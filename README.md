# CompalGit
***
# 資料夾說明
## Gaming Server
* 放在邊緣伺服器上，運行時負責啟動SteamVR、向後台註冊接收指令、處理跟遊戲開關相關的工作，透過運行Flask跟Streaming Server與Backend溝通

## Streaming Server
* 負責在使用者要投放遊戲畫面時，接收使用者傳來的畫面，透過Flask跟Gaming Server與Backend溝通

## Controller Simulation
* 負責在PC上模擬一個XBox GamePad，運行在Gaming Server

# 備註
1. Gaming Server 以及 Streaming Server 可以放在同一台電腦上，由Game Server把遊戲畫面 推流到 Stream Server所host的 NginX Server
2. 如果不需要模擬控制器的話，例如使用的是HTC Vive Focus、Oculus Quest，則不需要開啟Controller Simulation

