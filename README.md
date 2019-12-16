# pyseeta: python api for [SeetaFaceEngine](https://github.com/seetaface/SeetaFaceEngine.git)

[![Build Status](https://travis-ci.org/gaojunying/pyseeta.svg?branch=master)](https://travis-ci.org/gaojunying/pyseeta)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/gaojunying/pyseeta/blob/master/LICENSE)

## for detection
<img src="images/chloecalmon_det.jpg" width = '70%'/>

## for alignment
<img src="images/chloecalmon_align.jpg" width = '70%'/>

## for identification
<div align='center'>
    <img src="images/single_id.jpg" width = "300"/>
    <img src="images/double_id.jpg" width = "400"/>
</div>

## Installation

1. Download [pyseeta](https://github.com/gaojunying/pyseeta.git)

```bash
git clone https://github.com/gaojunying/pyseeta.git
```

2. Download [SeetaFaceEngine](https://github.com/gaojunying/SeetaFaceEngine.git)

```bash
git submodule update --init --recursive
```

3. Build `SeetaFaceEngine` dynamic library.

> on unix

```bash
cd SeetaFaceEngine/
mkdir Release; cd Release
cmake ..
make  
```

> on windows

```bash
cd SeetaFaceEngine/
mkdir Release; cd Release
cmake -G "Visual Studio 14 2015 Win64" ..
cmake --build . --config Release
```

4. installation

```bash
python setup.py install
```

5. run examples

```bash
python examples/{test_opencv.py or test_pillow.py}
```

## Uninstallation

```bash
pip uninstall pyseeta
```

### Thanks
- [@TuXiaokang](http://github.com/TuXiaokang/pyseeta.git)
