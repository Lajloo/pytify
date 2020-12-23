import chrome_bookmarks


def urls_in_folder(folder, url_list):
    for url in folder.urls:
        url_list.append(url['url'])
    for child in folder.folders:
        urls_in_folder(child, url_list)


def get_list_of_urls(bookmark_name):
    """Returns list of urls from bookmarks."""
    url_list = []
    for folder in chrome_bookmarks.folders:
        if folder.name == bookmark_name:
            urls_in_folder(folder, url_list)
    return url_list

