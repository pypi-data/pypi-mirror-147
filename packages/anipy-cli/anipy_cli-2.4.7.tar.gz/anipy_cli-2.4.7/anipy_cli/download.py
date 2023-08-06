import requests
import shutil
import sys
from tqdm import tqdm
from requests.adapters import HTTPAdapter, Retry
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlsplit
from better_ffmpeg_progress import FfmpegProcess

from .misc import response_err, error, keyboard_inter
from .colors import colors
from . import config


class download:
    """
    Download Class.
    A entry with all fields is required.
    """

    def __init__(self, entry, ffmpeg=False) -> None:
        self.entry = entry
        self.ffmpeg = ffmpeg
        self.headers = {"referer": self.entry.embed_url}

    def download(self):
        self.show_folder = config.download_folder_path / f"{self.entry.show_name}"
        config.download_folder_path.mkdir(exist_ok=True)
        self.show_folder.mkdir(exist_ok=True)
        self.session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        print("-" * 20)
        print(
            f"{colors.CYAN}Downloading:{colors.RED} {self.entry.show_name} EP: {self.entry.ep} - {self.entry.quality} {colors.END}"
        )

        if "m3u8" in self.entry.stream_url:
            print(f"{colors.CYAN}Type:{colors.RED} m3u8")
            if self.ffmpeg or config.ffmpeg_hls:
                print(f"{colors.CYAN}Downloader:{colors.RED} ffmpeg")
                self.ffmpeg_dl()
                return

            print(f"{colors.CYAN}Downloader:{colors.RED} internal")
            self.multithread_m3u8_dl()
        elif "mp4" in self.entry.stream_url:
            print(f"{colors.CYAN}Type:{colors.RED} mp4")
            self.mp4_dl(self.entry.stream_url)

    def ffmpeg_dl(self):
        config.user_files_path.mkdir(exist_ok=True)
        config.ffmpeg_log_path.mkdir(exist_ok=True)
        fname = f"{self.entry.show_name}_{self.entry.ep}.mp4"
        dl_path = self.show_folder / fname
        ffmpeg_process = FfmpegProcess(
            [
                "ffmpeg",
                "-headers",
                f"referer:{self.entry.embed_url}",
                "-i",
                self.entry.stream_url,
                "-vcodec",
                "copy",
                "-acodec",
                "copy",
                "-scodec",
                "mov_text",
                "-c",
                "copy",
                str(dl_path),
            ]
        )

        try:
            ffmpeg_process.run(
                ffmpeg_output_file=str(
                    config.ffmpeg_log_path / fname.replace("mp4", "log")
                )
            )
            print(f"{colors.CYAN}Download finished.")
        except KeyboardInterrupt:
            error("interrupted deleting partially downloaded file")
            fname.unlink()

    def mp4_dl(self, dl_link):
        """

        :param dl_link:
        :type dl_link:
        :return:
        :rtype:
        """
        r = self.session.get(dl_link, headers=self.headers, stream=True)
        response_err(r, dl_link)
        total = int(r.headers.get("content-length", 0))
        fname = self.show_folder / f"{self.entry.show_name}_{self.entry.ep}.mp4"
        try:
            with fname.open("wb") as out_file, tqdm(
                desc=self.entry.show_name,
                total=total,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in r.iter_content(chunk_size=1024):
                    size = out_file.write(data)
                    bar.update(size)
        except KeyboardInterrupt:
            error("interrupted deleting partially downloaded file")
            fname.unlink()

        print(f"{colors.CYAN}Download finished.")

    def get_ts_links(self):
        """
        Gets all ts links
        from a m3u8 playlist.
        M3u8 link must have gone trough
        videourl().quality() to work
        properly.

        :return:
        :rtype:
        """
        r = requests.get(self.entry.stream_url, headers=self.headers)
        self.ts_link_names = [x for x in r.text.split("\n")]
        self.ts_link_names = [x for x in self.ts_link_names if not x.startswith("#")]

        if "fc24fc6eef71638a72a9b19699526dcb" in self.entry.stream_url:
            self.ts_links = self.ts_link_names
            self.ts_link_names = [urlsplit(x).path for x in self.ts_link_names]
            self.ts_link_names = [x.split("/")[-1] for x in self.ts_link_names]
        else:
            self.ts_links = [
                urljoin(self.entry.stream_url, x.strip()) for x in self.ts_link_names
            ]

        self.link_count = len(self.ts_links)

    def download_ts(self, ts_link, fname):
        """

        :param ts_link:
        :type ts_link:
        :param fname:
        :type fname:
        :return:
        :rtype:
        """
        try:
            r = self.session.get(ts_link, headers=self.headers)
        except:
            self.counter += 1
            return

        file_path = self.temp_folder / fname

        print(
            f"{colors.CYAN}Downloading Parts: {colors.RED}({self.counter}/{self.link_count}) {colors.END}",
            end="\r",
        )

        with open(file_path, "wb") as file:
            for data in r.iter_content(chunk_size=1024):
                file.write(data)
        self.counter += 1

    def multithread_m3u8_dl(self):
        """
        Multithread download
        function for m3u8 links.
        - Creates show and temp folder
        - Starts ThreadPoolExecutor instance
          and downloads all ts links
        - Merges ts files
        - Delets temp folder

        :return:
        :rtype:
        TODO: Update this downloader
        """
        self.get_ts_links()
        self.temp_folder = self.show_folder / f"{self.entry.ep}_temp"
        self.temp_folder.mkdir(exist_ok=True)
        self.counter = 0

        try:
            with ThreadPoolExecutor(60) as pool:
                pool.map(self.download_ts, self.ts_links, self.ts_link_names)
        except KeyboardInterrupt:
            shutil.rmtree(self.temp_folder)
            keyboard_inter()
            sys.exit()

        print(f"\n{colors.CYAN}Parts Downloaded")
        self.merge_files()
        print(f"\n{colors.CYAN}Parts Merged")
        shutil.rmtree(self.temp_folder)

    def merge_files(self):
        """
        Merge downloded ts files
        into one ts file.

        :return:
        :rtype:
        """
        out_file = self.show_folder / f"{self.entry.show_name}_{self.entry.ep}.ts"
        try:
            with open(out_file, "wb") as f:
                self.counter = 1
                for i in self.ts_link_names:
                    print(
                        f"{colors.CYAN}Merging Parts: {colors.RED} ({self.counter}/{self.link_count}) {colors.END}",
                        end="\r",
                    )
                    try:
                        if i != "":
                            with open(self.temp_folder / i, "rb") as t:
                                f.write(t.read())
                        else:
                            pass
                    except FileNotFoundError:
                        pass

                    self.counter += 1

        except PermissionError:
            error(f"could not create file due to permissions: {out_file}")
