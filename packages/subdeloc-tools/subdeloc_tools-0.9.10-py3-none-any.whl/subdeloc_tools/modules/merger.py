import subprocess
import sys
import json
import os
from typing import Dict, Union, List
from subdeloc_tools.common.types.types import StreamsVar


class Merger:

    TASKS = {"demux":1, "mux":2}
    STATUSES = {"NOFILE":0, "INITIALIZED":1, "MUXXING": 2, "DEMUXXING":3}

    def __init__(self):
        self.status = 0
        self.finished = "./Finished"
        self.streams = None
        self.file = None
        self.codec_name = None
        self.filename = ""

    def get_subtitle_indexes(self) -> List[str]:
        b_indexes = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "s", "-show_entries", "stream=index", "-of", "csv=p=0", self.file])
        indexes = b_indexes.decode("utf-8").split("\n")
        indexes.pop()

        return indexes

    def get_filename(self, f: str) -> str:
        return f.split(os.sep)[-1]

    def get_streams(self) -> Union[StreamsVar, bool]:
        try:
            if self.status == self.STATUSES["INITIALIZED"]:
                return self.streams
            else:
                return False
        except Exception as e:
            print(e)
            return False
    
    def generate_subs_params(self, sfiles):
        """
        Generate arguments to insert subtitle at last position for the FFMPEG command.
        """
        try:
            params = []
            for i in sfiles:
                params = params + ["-map", "0:s:"+str(i), "-disposition:s:"+str(i), "0"]
            return params
        except Exception as e:
            print(e)
            return False

    def generate_params(self, path: str):
        """
        Generate whole arguments for the FFMPEG command.
        """
        try:
            sfiles = self.get_kept_subs()
            filename = self.filename
            newfilename = "."+os.sep+path+os.sep+filename + '.mkv'

            subparams = self.generate_subs_params(sfiles)

            ads = ["-metadata:s:s:{}".format(len(sfiles)), "language=eng", "-metadata:s:s:{}".format(len(sfiles)), "handler_name=English", "-metadata:s:s:{}".format(len(sfiles)), "title=Unlocalized", "-max_interleave_delta", "0", "-disposition:s:{}".format(len(sfiles)), "default", newfilename]
            return (subparams, ads)
        except Exception as e:
            print(e)
            return []

    def mux(self, f: str, subtitle: str, path: str = "Finished") -> bool:
        try:
            if self.status == self.STATUSES["INITIALIZED"] and os.path.isfile(subtitle) and os.path.isfile(f) and os.path.exists(path):
                params = self.generate_params(path)
                self.status = self.STATUSES["MUXXING"]
                args = ["ffmpeg", "-loglevel", "quiet", "-y", "-i", f, "-i", subtitle, "-c", "copy", "-map", "0:v", "-map", "0:a"] + params[0] + ["-map", "1"] + params[1]
                rc = subprocess.Popen(args, shell=False)
                rc.communicate()
                self.status = self.STATUSES["INITIALIZED"]
                return True
            else:
                return False
        except Exception as e:
            self.status = self.STATUSES["INITIALIZED"]
            print(e)
            return False

    def demux(self, name: str, index: int, output: str) -> Union[str, bool]:
        try:
            if self.status == self.STATUSES["INITIALIZED"]:
                self.status = self.STATUSES["DEMUXXING"]
                args = ["ffmpeg", "-loglevel", "quiet", "-i", name, "-map", "0:{}".format(index), "-c", "copy", output]
                print("Demuxxing with:", args)
                rc = subprocess.Popen(args, shell=False)
                rc.communicate()
                self.status = self.STATUSES["INITIALIZED"]

                return output
            else:
                return False
        except Exception as e:
            print(e)
            self.status = self.STATUSES["INITIALIZED"]
            return False

    def print_language_indexes(self) -> int:
        try:
            if self.status == self.STATUSES["INITIALIZED"] and self.streams:
                for i in self.streams["streams"]:
                    if i["codec_type"] == "subtitle":
                        print(i["index"], "\t|", i["tags"].get("language", "Unknown"), "\t|", i["tags"].get("title", "Unknown"))
            return 0
        except Exception as e:
            print(e)
            return -1

    def get_language_index(self, language: str, selected_index: int=0) -> int:
        try:
            if self.status == self.STATUSES["INITIALIZED"] and self.streams:
                if selected_index:
                    self.codec_name = self.streams["streams"][selected_index]["codec_name"]
                    return selected_index
                    
                index = -1
                f_sub = -1
                cn = None
                for i in self.streams["streams"]:
                    if i["codec_type"] == "subtitle":
                        if f_sub == -1:
                            cn = i["codec_name"]
                            f_sub = i["index"]
                        if "language" in i["tags"].keys():
                            if i["tags"]["language"] == language:
                                print(i["tags"]["language"], "|", i["index"])
                                index = i["index"]
                                self.codec_name = i["codec_name"]
                                return index
                if f_sub > -1:
                    self.codec_name = cn
                    return f_sub
                else:
                    return -1
            else:
                return -1
        except Exception as e:
            print(e)
            return -1

    def get_number_subs(self) -> int:
        try:
            if self.status == self.STATUSES["INITIALIZED"]:
                subs = 0
                for i in self.streams["streams"]:
                    if i["codec_type"] == "subtitle":
                        subs += 1
                return subs
            else:
                return 0
        except Exception as e:
            print(e)
            return 0

    def get_kept_subs(self) -> Union[List[int], int]:
        try:
            if self.status == self.STATUSES["INITIALIZED"]:
                subs = 0
                kept = list()
                for i in self.streams["streams"]:
                    if i["codec_type"] == "subtitle":
                        if not "Unlocalized" in i["tags"].get("title", ''):
                            kept.append(subs)
                        subs += 1
                return kept
            else:
                return 0
        except Exception as e:
            print(e)
            return 0

    def set_file(self, f: str) -> bool:
        try:
            self.filename = self.get_filename(str(f))
            self.file = f
            info = json.loads(subprocess.check_output(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", f]))
            self.streams = info
            self.status = self.STATUSES["INITIALIZED"]
            return True
        except Exception as e:
            print(e)
            return False

    def remove_file(self) -> bool:
        try:
            self.streams = None
            self.file = None
            self.status = self.STATUSES["NOFILE"]
            return True
        except Exception as e:
            print(e)
            return False