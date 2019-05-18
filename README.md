# img2location

find where an image is taken

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
