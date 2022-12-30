import json
import requests
from lxml import etree
from urllib import parse

from config import config
from schema import VideoData, DashData
from downloader import BilibiliDownloader


class BilibiliParser:
    headers = {
            "referer": "https://www.bilibili.com/",
            "origin": "https://www.bilibili.com",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "cookie": config.cookie,

        }

    def parse_url(self, text: str, area="video"):
        text = text.strip()
        url_parse = parse.urlparse(text)
        scheme = "https" if url_parse.scheme not in ("http", "https") else url_parse.scheme
        if url_parse.netloc and url_parse.netloc != "www.bilibili.com":
            raise Exception("暂不支持解析除bilibili以外网站的视频资源")
        netloc = "www.bilibili.com"
        path = f"/{area}/{url_parse.path}" if url_parse.path.startswith(("BV", "av")) else url_parse.path
        p = parse.parse_qs(url_parse.query).get("p")
        if p:
            url = f"{scheme}://{netloc}{path}?p={p[0]}"
        else:
            url = f"{scheme}://{netloc}{path}"
        return url
        

    def parse_html(self, text: str, timeout=2):
        url = self.parse_url(text)
        print(url)
        resp = requests.get(url, headers=self.headers, timeout=timeout)
        if resp.status_code != 200:
            print(f"html request error:{resp.text}")
        html = etree.HTML(resp.text)
        objs = html.xpath("//script")
        dash_data, video_data = None, None
        for ele in objs:
            if ele.text and ele.text.startswith("window.__playinfo__"):
                data = ele.text.strip("window.__playinfo__ = ")
                play_info = json.loads(data)
                dash_data = DashData(**play_info["data"]["dash"])
            elif ele.text and ele.text.startswith("window.__INITIAL_STATE__"):
                data = ele.text.strip("window.__INITIAL_STATE__ = ").split(";(")[0]
                initial_state = json.loads(data)
                video_data = VideoData(**initial_state["videoData"])
        return video_data, dash_data

    @staticmethod
    def parse_video_data(video_data: VideoData):
        p = video_data.embedPlayer.p
        bvid, aid, title = video_data.bvid, video_data.aid, video_data.title
        cid, part, duration = video_data.pages[p-1].cid, video_data.pages[p-1].part, video_data.pages[p-1].duration
        filename = title
        if p > 1:
            filename = part
        return bvid, aid, cid, filename, duration

    # @staticmethod
    # def parse_play_data(play_data):
    #     video_map, audio_map = {"base_url": [], "backup_url": []}, {"base_url": [], "backup_url": []}
    #     # print(play_data)
    #     for ele in play_data["video"]:
    #         video_map["base_url"].append(ele["baseUrl"])
    #         video_map["base_url"].append(ele["base_url"])
    #         video_map["backup_url"].extend(ele["backupUrl"])
    #         video_map["backup_url"].extend(ele["backup_url"])
    #     for ele in play_data["audio"]:
    #         audio_map["base_url"].append(ele["baseUrl"])
    #         audio_map["base_url"].append(ele["base_url"])
    #         audio_map["backup_url"].extend(ele["backupUrl"])
    #         audio_map["backup_url"].extend(ele["backup_url"])
    #     return video_map, audio_map


if __name__ == "__main__":
    av = "BV1U44y1x7Ca"
    parser = BilibiliParser()
    video_data, dash_data = parser.parse_html(av)
    bvid, aid, cid, filename, duration = parser.parse_video_data(video_data)
    downloader = BilibiliDownloader(filename, dash_data.audio[0].base_url, dash_data.video[0].base_url)
    downloader.download()
