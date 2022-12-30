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
        self.file_path = os.path.join(config.download_path, f"{file_name}.mp4")
        mask = tools.base64transform(file_name).replace(os.sep, "")
        self.audio_path = os.path.join(config.download_path, f"audio-{mask}.m4s")
        self.video_path = os.path.join(config.download_path, f"video-{mask}.m4s")

    def save_file(self, url, file_path, retry=2, timeout=1):
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
        ffmpeg_tools.ffmpeg_merge_video_audio(self.video_path, self.audio_path, self.file_path)
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
    video_name = "底层小V直播500天无人问津，一首《届不到的爱恋》送给大家"
    audio_url = "https://xy121x205x162x59xy.mcdn.bilivideo.cn:4483/upgcxcode/12/21/931772112/931772112_nb3-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1672289219&gen=playurlv2&os=mcdn&oi=30045303&trid=0000e7a6439bc81d4359bd427e2aa13c9752u&mid=0&platform=pc&upsig=4e26b31951ae7441ac324befc212f433&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&mcdnid=11000334&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&agrr=1&bw=17432&logo=A0000400"
    video_url = "https://xy121x205x162x59xy.mcdn.bilivideo.cn:4483/upgcxcode/12/21/931772112/931772112_nb3-1-30032.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1672289219&gen=playurlv2&os=mcdn&oi=30045303&trid=0000e7a6439bc81d4359bd427e2aa13c9752u&mid=0&platform=pc&upsig=10d8fd05c58bf411e4cd2c200b7d70b1&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&mcdnid=11000334&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&agrr=1&bw=26704&logo=A0000400"
    downloader = BilibiliDownloader(video_name, audio_url, video_url)
    downloader.download()
