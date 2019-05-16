# pylint: disable=line-too-long
'''
this script takes a query and downloads imgs matching the query
'''

import logging
import os
import sys

import magic
import requests


LOGLEVEL = logging.WARN
try:
    if sys.argv[3] == "-v":
        LOGLEVEL = logging.DEBUG
except IndexError:
    print("usage:", sys.argv[0], "<query> <region> -v")

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p',
                    level=LOGLEVEL,
                    filename="./baidu.log")
try:
    API_KEY = open("baidu_api.txt").readline().strip()
except FileNotFoundError:
    logging.error("./baidu_api.txt not found")


def get_region_locations(query, region):
    '''
    query: anything
    region: province/city

    returns: a list of locations matching your query
    '''
    url = "http://api.map.baidu.com/place/v2/search?query={}&region={}&scope=2&output=json&ak={}".format(
        query, region, API_KEY)

    resp = requests.get(url)
    result = resp.json()

    # encapsulate results
    results = {}

    for loc in result['results']:
        name = loc['name']
        poi_id = loc['uid']
        coord = loc['location']

        results.update({name: [poi_id, coord]})

    return results


def nearby_pois(coordinate):
    '''
    get POIs near the given coordinate
    '''
    lat = coordinate['lat']
    lng = coordinate['lng']
    url = "http://api.map.baidu.com/place/v2/search?query=银行$酒店$美食$购物$生活服务$旅游景点$丽人$休闲娱乐$运动健身$教育培训&location={},{}&radius=100&output=json&ak={}".format(
        lat, lng, API_KEY)

    resp = requests.get(url)
    result = resp.json()

    # encapsulate results
    results = {}

    for loc in result['results']:
        name = loc['name']
        poi_id = loc['uid']

        results.update({name: poi_id})

    return results


def get_img(poi_dict):
    '''
    download imgs for each location
    '''

    for name, poi_id in poi_dict.items():
        url = "http://api.map.baidu.com/panorama/v2?ak={}&poiid={}&width=1024&height=512&heading=0&pitch=0&fov=90".format(
            API_KEY, poi_id)

        img_file = "./database/search/{}.jpg".format(name)
        logging.debug("Downloading image %s to %s", url, img_file)

        data = requests.get(url).content

        open(img_file, 'wb').write(data)

        if "jpeg" not in magic.from_file(img_file, mime=True).lower():
            logging.warning("Invalid image file, deleting %s", img_file)
            try:
                os.remove(img_file)
            except BaseException:
                pass


def main():
    '''
    what to run
    '''
    locs = get_region_locations(sys.argv[1], sys.argv[2])

    for name, geoinfo in locs.items():
        # image of the central spot itself
        poi_dict = {name: geoinfo[0]}
        get_img(poi_dict)

        # POIs around the central spot
        coordinate = geoinfo[1]
        poi_dict = nearby_pois(coordinate)
        get_img(poi_dict)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
