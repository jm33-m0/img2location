# img2location
Intented to find where an image was taken

## Get Started

This is a toy project that uses the ResNet model to compare the input image with selected range of street-view images. This allows to effectively retrieve a possible address of the input image.

**Steps**
- Input image looks like `./query/query-class/query.jpg`
- Street-views downloaded from `-q query_string -r region` is put under `database/search`
- Check the log file for details

## FAQ
**Q:** Why do you need to "query" for street views from the Baidu map? <br/>
**A:** Yeah, it doesn't make sense. If you already knew what to query, why bother using this tool?. First, I don't have a beast-like machine for ResNet computing. If I downloaded thousands of images and compared them with my input, then I'm afraid its not possible. Second, if there are some store fronts in your picture, you can use them to narrow down the query range, which reduces the time cost. Anyways, consider this as a demo.<br/>

**Q:** Baidu map doesn't have much resources to locate my picture. <br/>
**A:** Google's place photos API might be a good alternative.<br/>

**Q:** How to make it more useful? <br/>
**A:** To make it more useful even for private detectives or cops, consider the following. 
- A huge street view resource (better without downloading). The project has taken care of image caching, in case you didn't know.
- A GPU server
- Distributed searching

## Demo

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

## Acknowledgement
- [pochih/CBIR](https://github.com/pochih/CBIR)
