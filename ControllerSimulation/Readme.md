# Controller Simulation
***
`print_udp_signal` : 用來顯示電腦收到的UDP鍵盤控制訊號封包，Debug用

`SendKeyboardSignal` : 用UDP封包來發送鍵盤訊號到另一台電腦，可以參考這個方式，但用不同語言實作

`vJoyClient` : 用來接收鍵盤訊號並連接vJoy SDK，包裝成XBOX控制器Driver

`x360ce` : XBOX GamePad Simulator，可以從[官網](https://www.x360ce.com/ "x360ce官網")下載，裡面已設定好Gunjack的配置

***
# 使用說明

## SendKeyboardSignal 環境設定(Python)
1. 安裝Python 3
2. 安裝PIP
3. 安裝相關套件(系統提示缺少什麼就用pip 安裝)

## vJoyClient 開發(C++)
1. 去vJoy官網下載最新的 Feeder SDK [Download](https://sourceforge.net/projects/vjoystick/files/Beta%202.x/SDK/)[教學](http://vjoystick.sourceforge.net/site/index.php/dev216/system-architecture/81-news/87-writing-a-feeder-application2) []
2. 用VS開一個新專案
3. Build
4. Run

## 當要在電腦上模擬Xbox 控制器的時候
1. 安裝vJoy，[官網](https://sourceforge.net/projects/vjoystick/ "vjoy官網")
2. 設定Config vJoy (依照SendKeyboardSignal 會用到的Buttons數量修改)，並點選啟動
3. 下載x360ce，首次運行程式會提示你去安裝xinput的dll，點選create讓他去跑
![Hint](https://truth.bahamut.com.tw/s01/201602/a70f4d24f287c24ba13524b82aca3920.PNG?w=1000)
4. 設定x360ce按鍵配置，依照vJoy Receiver的訊號，設定控制器的每個按鈕要對應哪個訊號 [教學](https://forum.gamer.com.tw/C.php?bsn=173&snA=10325)
5. 執行vJoyClient.exe
6. 執行x360ce (縮小視窗在背景運行可以減少資源消耗)

#備註
1. 在執行SteamVR時，如果遇到滑鼠鍵盤不正常動作時(卡鍵)，把x360ce關掉試試看，通常是原因
