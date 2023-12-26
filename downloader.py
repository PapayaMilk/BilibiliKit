import os
import requests

import tools
# from ffmpeg import ffmpeg
from config import config


class BilibiliDownloader:
    headers = {
        "referer": "https://www.bilibili.com/",
        "origin": "https://www.bilibili.com",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "cookie": config.cookie,
    }

    def __init__(self, file_name, audio_url, video_url) -> None:
        self.audio_url = audio_url
        self.video_url = video_url
        if os.sep in file_name:
            file_name = file_name.replace(os.sep, "·")
        if "|" in file_name:
            file_name = file_name.replace("|", "丨")
        self.file_path = os.path.join(config.download_path, f"{file_name}.mp4")
        num = 1
        while os.path.exists(self.file_path):
            self.file_path = os.path.join(config.download_path, f"{file_name}({num}).mp4")
            num += 1
        mask = tools.base64transform(file_name).replace(os.sep, "")
        self.audio_path = os.path.join(config.download_path, f"audio-{mask}.m4s")
        self.video_path = os.path.join(config.download_path, f"video-{mask}.m4s")

    def save_file(self, url, file_path, retry=2, timeout=5):
        num, flag = 0, 0
        while num < retry:
            resp = requests.get(url, headers=self.headers, timeout=timeout, stream=True)
            if resp.status_code == 200:
                content_size = int(resp.headers['content-length'])
                chunk_size = round(content_size/100)
                count = 0
                with open(file_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            count += len(chunk)
                flag = 1
                break
            print(resp)
            num += 1
        return flag

    def transform_mp4(self):
        from moviepy.editor import ffmpeg_tools
        ffmpeg_tools.ffmpeg_merge_video_audio(self.video_path, self.audio_path, self.file_path, logger=None)
        # ffmpeg.contact([self.audio_path, self.video_path], self.file_path)

    def clear_file(self, *args):
        for file_path in args:
            os.remove(file_path)

    def download(self):
        flag1 = self.save_file(self.audio_url, self.audio_path)
        flag2 = self.save_file(self.video_url, self.video_path)
        if flag1 and flag2:
            self.transform_mp4()
            self.clear_file(self.audio_path, self.video_path)



if __name__ == "__main__":
    video_name = "北京遇上西雅图"
    audio_url = "https://xy122x226x162x102xy.mcdn.bilivideo.cn:4483/upgcxcode/26/32/29973226/29973226_p1-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1672379084&gen=playurlv2&os=mcdn&oi=30046011&trid=0000caf60e6257bc44b78c0e92b6127d10edp&mid=0&platform=pc&upsig=360a13a3ab9e72cae6347950468f8cb4&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&mcdnid=9002999&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&agrr=1&bw=24209&logo=A0000100"
    video_url = "https://xy122x226x162x102xy.mcdn.bilivideo.cn:4483/upgcxcode/26/32/29973226/29973226_p1-1-30032.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1672379084&gen=playurlv2&os=mcdn&oi=30046011&trid=0000caf60e6257bc44b78c0e92b6127d10edp&mid=0&platform=pc&upsig=a13a8874ed91c145fce844d0541a4231&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&mcdnid=9002999&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&agrr=1&bw=107033&logo=A0000100"
    downloader = BilibiliDownloader(video_name, audio_url, video_url)
    downloader.download()
    'https://www.bilibili.com/video/BV1us411Z7YZ/?spm_id_from=333.337.search-card.all.click'
    'https://www.bilibili.com/video/BV1us411Z7YZ?p=2&vd_source=2d7ec5aa9b72707640a64a0ffa75089f'
