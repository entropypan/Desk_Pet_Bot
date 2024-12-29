# Desk Pet Bot

<img src="assets/sosorry.png" height="800">

## Table of Contents

-   [專案介紹](#專案介紹)
-   [硬體介紹](#硬體介紹)
-   [準備](#準備)
-   [功能和程式](#功能和程式)
-   [參考資料](#參考資料)

## 專案介紹
以樹梅派為基礎做一個小型的動物形 bot，可以藉由做出手勢或說話跟此桌面寵物互動。

### 專案緣由
有些人對真實動物的皮毛會過敏，又或者是家人不同意、擔心照顧麻煩、住處規定禁止等理由，因而不能養許多熱門的寵物，因此設計此桌面寵物來滿足這部分人的需求。本次採用了 AI 手勢辨識和語音聲控，讓跟寵物間的互動更加真實。

## 硬體介紹
### 材料清單
* Rasberry Pi 4 x 1
* Rasberry Pi Camera Module x 1
* Rasberry Pi Screen Module x 1
* 麥克風 x 1
* 音響組 x 1
* ...

### 硬體組成
/解釋組合

## 準備
首先，確保樹梅派4B能正常運作，且具備Raspbian Buster OS，並確保Python版本為3

### 安裝Open-CV和Mediapipe
用下列指令將CONF_SWAPSIZE = 100變更為CONF_SWAPSIZE=2048
```bash
sudo nano /etc/dphys-swapfile
```

安裝、解壓，其中最後一步會執行一個多小時，請耐心等待
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