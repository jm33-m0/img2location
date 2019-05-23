# img2location

find where an image is taken

## how it works

this is a toy project, which uses resnet (mostly) to compare your input image with selected range of street view images, effectively get a possible address of the input image.

basically:

- input image looks like `./query/query-class/query.jpg`
- street views downloaded from `-q query_string -r region` is put under `database/search`
- check the log file for details

## how to make it more useful

yeah it can be pretty useful, for private detectives, or cops, or, stalkers

if you want better performance, consider the following:

- a huge street view resource, better without downloading, my toy has taken care of image caching, in case you dont know
- a GPU server maybe
- distributed searching is also worth a shot

## demo

```text
$ .venv/bin/python img2location.py -q 天安门 -r 北京 -v
[*] Requesting images from baidu map...
[*] CBIR working...

[+] query: query/query-demo/天安门.jpg

database/search/天安门---北京市东城区长安街.jpg:        0.0,    Class search
database/search/外金水桥---北京市东城区东长安街天安门内.jpg:    0.12019465118646622,    Class search
database/search/青云片兰室---天安门地区管理委员会附近.jpg:      0.23571714758872986,    Class search
database/search/天安门服务部---广场东侧路44号附近.jpg:  0.2933036684989929,     Class search
database/search/天安门-华表---北京市东城区东长安街天安门内.jpg: 0.31151291728019714,    Class search

Matching address:
0.0: 北京市东城区长安街

Matching address:
0.12019465118646622: 北京市东城区东长安街天安门内

Matching address:
0.23571714758872986: 天安门地区管理委员会附近

Matching address:
0.2933036684989929: 广场东侧路44号附近

Matching address:
0.31151291728019714: 北京市东城区东长安街天安门内
```

## acknowledgement

- [pochih/CBIR](https://github.com/pochih/CBIR)
