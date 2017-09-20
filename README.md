# Blot Copy and Paste Detector

This is a detect tool for blot images in pdf file.

## Requirements
```
pdfimages
(A command line tool for pdf extraction.)
```


## Install

```
(git clone or download zip, whatever)
$ sudo pip insatall -r requirements.txt
```

## Usage
```
It's pretty simple.

Detect images in pdf directly, then run run.py.

usage: run.py [-h] -f FILE [-s SVM] [-o [OUTPUT]] [-d]
optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Specify the pdf file you want to extract from.
  -s SVM, --svm SVM     Specify the SVM you want to apply for text remove.
  -o [OUTPUT], --output [OUTPUT]
                        Specify the image extraction,pure and detect output
                        path.
  -d, --display         Print final result as a pop window at same time.

```
```
Detect with given image, run detect.py.
usage: detect.py [-h] -i IMAGE [-s SVM] [-o [OUTPUT]] [-d]
optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE, --image IMAGE
                          Specify the image file you want to detect.
  -s SVM, --svm SVM     Specify the SVM you want to apply for text remove.
  -o [OUTPUT], --output [OUTPUT]
                          Specify the image extraction,pure and detect output
                          path.
  -d, --display         Print final result as a pop window at same time.
```
```
If you just want to clean up a blot image, run remove_text.py.

usage: remove_text.py [-h] -i IMAGE [-s SVM] [-o [OUTPUT]] [-d]
optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE, --image IMAGE
                        Specify the image file you want to detect.
  -s SVM, --svm SVM     Specify the SVM you want to apply for text remove.
  -o [OUTPUT], --output [OUTPUT]
                        Specify the image extraction,pure and detect output
                        path.
  -d, --display         Print final result as a pop window at same time.

```
```
Note that if you want to improve result of text removing or you want to remove
particular things for your own use, you can train SVM by using LBP_SVM.py.

```
## Examples
```
$ python run.py -d -f ./demo/demo1.pdf -o ./result
```
result:
![alt tag](https://github.com/HaojieYuan/blot_cp_detector/blob/master/demo_result/detectdemo1-000.png)
```
$ python detect.py -d -i ./demo/demo2.ppm -o ./result
```
result:
![alt tag](https://github.com/HaojieYuan/blot_cp_detector/blob/master/demo_result/detectdemo2.png)
```
$ python remove_text.py -d -i ./demo/demo3.jpg -o ./result
```
result:
![alt tag](https://github.com/HaojieYuan/blot_cp_detector/blob/master/demo_result/puredemo3.png)
```
# Contact me
```
email address:  haojie.d.yuan@gmail.com
```
