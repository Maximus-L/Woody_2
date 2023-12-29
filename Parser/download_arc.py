# -*- coding: utf-8 -*-

import Parser.Urls


def download_arc(name, url, dest_path) -> str | None:
    if name == 'MSP':
        try:
            file_name = Parser.Urls.url_download_long_file(url,
                                                           destination_path=dest_path)
            return file_name
        except Exception as e:
            return None
