import chrome_bookmarks


def urls_in_folder(folder, url_list):
    """
    Generates the list of urls in folder.
    :param folder: Single folder of chrome_bookmarks.folders.
    :param url_list: List of urls.
    """
    for url in folder.urls:
        url_list.append(url['url'])
    for child in folder.folders:
        urls_in_folder(child, url_list)


def get_list_of_urls(bookmark_name):
    """
    Returns list of urls from bookmarks.
    :param bookmark_name: Name of the bookmark.
    """
    url_list = []
    for folder in chrome_bookmarks.folders:
        if folder.name == bookmark_name:
            urls_in_folder(folder, url_list)
    return url_list

