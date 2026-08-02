name: Build APK

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install Dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y build-essential ccache git libncursesw5 libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev liblzma-dev uuid-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev pkg-config ant openjdk-17-jdk autoconf libtool

    - name: Build with Buildozer
      uses: kannitz/buildozer-action@v10
      with:
        command: android debug

    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: package
        path: bin/*.apk
