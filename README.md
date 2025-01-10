# Desk Pet Bot

<img src="/assets/photo.jpg">

## 目錄

-   [專案介紹](#專案介紹)
-   [硬體介紹](#硬體介紹)
-   [準備](#準備)
-   [功能和程式](#功能和程式)
-   [參考資料](#參考資料)

## 專案介紹
原本想以樹梅派為基礎做一個小型的動物形 bot，可以藉由做出手勢或說話跟此桌面寵物互動。
後因製作時產生不明問題(如圖)導致一段時間空窗期，簡化成桌面管家機器人。
<img src="problem.png">

## 硬體介紹
### 材料清單
* Rasberry Pi 4 x 1
* Rasberry Pi Camera Module x 1
* Rasberry Pi Screen Module x 1
* 音響組 x 1
* 自製管家外觀

### 硬體組成
<img src="hard.png">

## 準備
首先，具備Raspbian Buster OS之樹梅派4B，並確保內含Python版本為3

### 安裝Open-CV和Mediapipe
用下列指令將CONF_SWAPSIZE = 100變更為CONF_SWAPSIZE=2048
```bash
sudo nano /etc/dphys-swapfile
```

安裝+解壓，其中最後一步會執行一個多小時，請耐心等待
```bash
sudo apt-get install build-essential cmake pkg-config

sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev

sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev

sudo apt-get install libxvidcore-dev libx264-dev

sudo apt-get install libgtk2.0-dev libgtk-3-dev

sudo apt-get install libatlas-base-dev gfortran

sudo pip3 install numpy

wget -O opencv.zip https://github.com/opencv/opencv/archive/4.4.0.zip

wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.4.0.zip

unzip opencv.zip

unzip opencv_contrib.zip

cd ~/opencv-4.4.0/

mkdir build

cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \ -D CMAKE_INSTALL_PREFIX=/usr/local \ -D INSTALL_PYTHON_EXAMPLES=ON \ -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-4.4.0/modules \ -D BUILD_EXAMPLES=ON ..

make -j $(nproc)
```

安裝Mediapipe
```bash
sudo pip3 install mediapipe-rpi4

sudo pip3 install gtts

sudo apt install mpg321

sudo pip3 install numpy --upgrade --ignore-installed
```

## 功能和程式
/介紹手勢和程式

## 參考資料
/參考資料堆