'''
this script takes a query and downloads imgs matching the query
'''

import logging
import traceback
import os

import magic
import requests


class ImageCollector:
    '''
    takes: query string and region/city name
    does: downloads all related images from baidu
    '''

    def __init__(self, query, region, loglevel):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                            datefmt='%Y-%m-%d %I:%M:%S %p',
                            level=loglevel,
                            filename="./img2location.log")
        try:
            self.api_key = open("baidu_api.txt").readline().strip()
        except FileNotFoundError:
            logging.fatal("./baidu_api.txt not found")

        self.query = query
        self.region = region

        url = "http://api.map.baidu.com/place/v2/search?" +\
            "query={}&region={}&scope=2&output=json&ak={}".format(
                query, region, self.api_key)

        resp = requests.get(url)
        result = resp.json()

        # encapsulate results
        results = {}

        for loc in result['results']:
            name = loc['name']
            poi_id = loc['uid']
            coord = loc['location']
            addr = loc['address']

            results.update({name: [poi_id, coord, addr]})

        logging.debug("search results:\n%s", results)
        self.location_list = results

    def nearby_pois(self, coordinate):
        '''
        get POIs near the given coordinate
        '''
        lat = coordinate['lat']
        lng = coordinate['lng']
        url = "http://api.map.baidu.com/place/v2/search?" +\
            "query=银行$酒店$美食$购物$生活服务$旅游景点$丽人$休闲娱乐$运动健身$教育培训&" +\
            "location={},{}&radius=50&output=json&ak={}".format(lat,
                                                                lng,
                                                                self.api_key)

        resp = requests.get(url)
        result = resp.json()

        # encapsulate results
        results = {}

        for loc in result['results']:
            name = loc['name']
            poi_id = loc['uid']
            addr = loc['address']

            results.update({name: [poi_id, addr]})
        logging.debug("nearby_pois:\n%s", results)

        return results

    def get_img(self, poi_dict):
        '''
        download imgs for each location
        '''

        for name, poi in poi_dict.items():
            poi_id = poi[0]
            poi_addr = poi[1]
            url = "http://api.map.baidu.com/panorama/v2?" +\
                "ak={}&poiid={}&width=1024&height=512&heading=0&pitch=0&fov=90".format(self.api_key,
                                                                                       poi_id)

            img_file = "./database/search/{}---{}.jpg".format(name, poi_addr)
            logging.warning("Downloading image %s to %s", url, img_file)
            if os.path.isfile(img_file):
                logging.debug("%s exists, skipping", img_file)
                continue

            data = requests.get(url).content

            open(img_file, 'wb').write(data)

            if "jpeg" not in magic.from_file(img_file, mime=True).lower():
                logging.warning("Invalid image file, deleting %s", img_file)
                try:
                    logging.debug("File content:\n%s",
                                  open(img_file, 'r').read())
                    os.remove(img_file)
                except BaseException:
                    logging.debug("Removing invalid img: %s",
                                  traceback.format_exc())

    def main(self):
        '''
        what to run
        '''
        for name, geoinfo in self.location_list.items():
            # image of the central spot itself
            poi_dict = {name: [geoinfo[0], geoinfo[2]]}
            self.get_img(poi_dict)

            # POIs around the central spot
            coordinate = geoinfo[1]
            poi_dict = self.nearby_pois(coordinate)
            self.get_img(poi_dict)
