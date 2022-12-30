from pydantic import BaseModel, Field, PositiveInt, HttpUrl
from typing import List


class VideoOwner(BaseModel):
    mid: PositiveInt = Field(description="up主id")
    name: str = Field(description="up主名称")
    face: HttpUrl = Field(description="up主头像url")


class VideoDimension(BaseModel):
    width: PositiveInt
    height: PositiveInt
    rotate: int


class VideoPage(BaseModel):
    cid: PositiveInt = Field(description="cv号")
    page: PositiveInt = Field(description="p")
    part: str = Field(description="p的视频名称")
    duration: PositiveInt = Field(description="p的视频时长")
    dimension: VideoDimension = Field(description="视频分辨率信息")
    first_frame: HttpUrl = Field(description="首帧图片的url")


class EmbedPlayer(BaseModel):
    p: PositiveInt = Field(description="当前视频分p号")
    aid: PositiveInt = Field(description="av号")
    bvid: str = Field(description="BV, 以`BV`开头的字符串")
    cid: PositiveInt = Field(description="cv号")


class VideoData(BaseModel):
    bvid: str = Field(description="BV, 以`BV`开头的字符串")
    aid: PositiveInt = Field(description="av号")
    cid: PositiveInt = Field(description="cv号")
    videos: PositiveInt = Field(description="p数")
    tid: PositiveInt = Field(description="tag id")
    tname: str = Field(description="tag名称")
    pic: HttpUrl = Field(description="封面url")
    title: str = Field(description="发布标题")
    pubdate: PositiveInt = Field(description="发布时间")
    desc: str = Field(description="简介")
    duration: PositiveInt = Field(description="视频时长")
    owner: VideoOwner = Field(description="up主信息")
    stat: dict = Field(description="包含观看数、收藏数、分享数信息；暂不解析")
    dimension: VideoDimension = Field(description="视频分辨率信息")
    pages: List[VideoPage] = Field(description="所有分p列表信息")
    embedPlayer: EmbedPlayer = Field(description="包含当前视频分p号")

    @property
    def get_barrage(self):
        return f'https://comment.bilibili.com/{self.cid}.xml'


class PlayList(BaseModel):
    id: PositiveInt
    baseUrl: str
    base_url: str
    backupUrl: List[str]
    backup_url: List[str]
    bandwidth: PositiveInt
    mimeType: str
    mime_type: str
    codecs: str
    width: int
    height: int
    frameRate: str
    frame_rate: str
    codecid: int


class DashData(BaseModel):
    duration: PositiveInt
    video: List[PlayList]
    audio: List[PlayList]

