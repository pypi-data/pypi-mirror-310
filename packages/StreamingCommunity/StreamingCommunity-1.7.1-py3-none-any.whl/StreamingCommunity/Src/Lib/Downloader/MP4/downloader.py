# 09.06.24

import os
import sys
import logging


# External libraries
import httpx
from tqdm import tqdm


# Internal utilities
from StreamingCommunity.Src.Util.headers import get_headers
from StreamingCommunity.Src.Util.color import Colors
from StreamingCommunity.Src.Util.console import console, Panel
from StreamingCommunity.Src.Util._jsonConfig import config_manager
from StreamingCommunity.Src.Util.os import internet_manager


# Logic class
from ...FFmpeg import print_duration_table


# Config
GET_ONLY_LINK = config_manager.get_bool('M3U8_PARSER', 'get_only_link')
TQDM_USE_LARGE_BAR = config_manager.get_int('M3U8_DOWNLOAD', 'tqdm_use_large_bar')
REQUEST_VERIFY = config_manager.get_float('REQUESTS', 'verify_ssl')
REQUEST_TIMEOUT = config_manager.get_float('REQUESTS', 'timeout')



def MP4_downloader(url: str, path: str, referer: str = None, headers_: str = None):

    """
    Downloads an MP4 video from a given URL using the specified referer header.

    Parameter:
        - url (str): The URL of the MP4 video to download.
        - path (str): The local path where the downloaded MP4 file will be saved.
        - referer (str): The referer header value to include in the HTTP request headers.
    """
    if GET_ONLY_LINK:
        return {'path': path, 'url': url}

    headers = None

    if "http" not in str(url).lower().strip() or "https" not in str(url).lower().strip():
        logging.error(f"Invalid url: {url}")
        sys.exit(0)
    
    if referer != None:
        headers = {'Referer': referer, 'user-agent': get_headers()}
    if headers == None:
        headers = {'user-agent': get_headers()}
    else:
        headers = headers_
    
    # Make request to get content of video
    with httpx.Client(verify=REQUEST_VERIFY, timeout=REQUEST_TIMEOUT) as client:
        with client.stream("GET", url, headers=headers, timeout=REQUEST_TIMEOUT) as response:
            total = int(response.headers.get('content-length', 0))

            if total != 0:

                # Create bar format
                if TQDM_USE_LARGE_BAR:
                    bar_format = (f"{Colors.YELLOW}[MP4] {Colors.WHITE}({Colors.CYAN}video{Colors.WHITE}): "
                                f"{Colors.RED}{{percentage:.2f}}% {Colors.MAGENTA}{{bar}} {Colors.WHITE}[ "
                                f"{Colors.YELLOW}{{n_fmt}}{Colors.WHITE} / {Colors.RED}{{total_fmt}} {Colors.WHITE}] "
                                f"{Colors.YELLOW}{{elapsed}} {Colors.WHITE}< {Colors.CYAN}{{remaining}} {Colors.WHITE}| "
                                f"{Colors.YELLOW}{{rate_fmt}}{{postfix}} {Colors.WHITE}]")
                else:
                    bar_format = (f"{Colors.YELLOW}Proc{Colors.WHITE}: {Colors.RED}{{percentage:.2f}}% "
                                f"{Colors.WHITE}| {Colors.CYAN}{{remaining}}{{postfix}} {Colors.WHITE}]")

                # Create progress bar
                progress_bar = tqdm(
                    total=total,
                    ascii='░▒█',
                    bar_format=bar_format,
                    unit_scale=True,
                    unit_divisor=1024,
                    mininterval=0.05
                )

                # Download file
                with open(path, 'wb') as file, progress_bar as bar:
                    for chunk in response.iter_bytes(chunk_size=1024):
                        if chunk:
                            size = file.write(chunk)
                            bar.update(size)

            else:
                console.print("[red]Cant find any stream.")

        # Get summary
        if total != 0:
            console.print(Panel(
                f"[bold green]Download completed![/bold green]\n"
                f"[cyan]File size: [bold red]{internet_manager.format_file_size(os.path.getsize(path))}[/bold red]\n"
                f"[cyan]Duration: [bold]{print_duration_table(path, description=False, return_string=True)}[/bold]", 
                title=f"{os.path.basename(path.replace('.mp4', ''))}", 
                border_style="green"
            ))
