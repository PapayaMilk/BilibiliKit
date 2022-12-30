import os
import shlex
import subprocess


class FFmpegServer:

    @staticmethod
    def command(cmd: str, timeout=None, show=False) -> int:
        stdout, stderr = None, None
        if not show:
            stdout, stderr = subprocess.DEVNULL, subprocess.DEVNULL
        cmd = shlex.split(cmd)
        subprocess_obj = subprocess.Popen(cmd, shell=False, stdout=stdout, stderr=stderr)
        subprocess_obj.wait(timeout)
        return subprocess_obj.returncode

    def clip(self, input_file, output_file, begin, finish=None, *, duration=None, copy=True):
        if duration is None:
            if finish is None:
                raise Exception("finish or duration is required!")
            duration = finish - begin
        if duration <= 0:
            raise Exception("begin or finish error!")
        args = ["ffmpeg", "-y", "-ss", str(round(begin, 2)), "-i", f"'{input_file}'", "-t", str(round(duration, 2))]
        if copy:
            args.extend(["-c", "copy"])
        args.append(f"'{output_file}'")
        cmd = " ".join(args)
        print(cmd)
        code = self.command(cmd)
        return code

    def framing(self, input_file, output_path, *, suffix="jpg", frame_rate=25, quality=2):
        args = ["ffmpeg", "-y", "-i", f"'{input_file}'",
                "-f", "image2", "-r", str(frame_rate), "-q:v", str(quality), os.path.join(output_path, f"%d.{suffix}")]
        cmd = " ".join(args)
        print(cmd)
        code = self.command(cmd)
        return code

    def contact(self, input_files: list, output_file: str):
        args = ["ffmpeg", "-y"]
        for input_file in input_files:
            args.extend(["-i", f"'{input_file}'"])
        args.extend(["-c", "copy", f"'{output_file}'"])
        cmd = " ".join(args)
        print(cmd)
        code = self.command(cmd)
        return code


ffmpeg = FFmpegServer()


if __name__ == "__main__":
    my_code = ffmpeg.clip("https://www.bilibili.com/video/BV1Ug411t7EP/", "test.mp4", 20, 30)
    print(my_code)