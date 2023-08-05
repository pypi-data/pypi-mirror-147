def tg_html_format(string: str) -> str:
    """
    Format a string as Telegram HTML.

    The following characters will be considered control characters:
    - ``\uE01B``: start bold
    - ``\uE00B``: end bold
    - ``\uE011``: start italic
    - ``\uE001``: end italic
    - ``\uE012``: start underline
    - ``\uE002``: end underline
    - ``\uE015``: start strike
    - ``\uE005``: end strike
    - ``\uE01F``: start spoiler
    - ``\uE00F``: end spoiler
    - ``\uE01C``: start single-line code
    - ``\uE00C``: end single-line code
    - ``\uE01D``: start multi-line code
    - ``\uE00D``: end multi-line code

    :param string: The string to format.
    :return: The formatted string.

    .. warning:: For now, this is a Telethon implementation detail.

    .. todo:: This may cause denial of service attacks from users!
    """

    string = string.replace("&", "&amp;")
    string = string.replace("<", "&lt;")
    string = string.replace(">", "&gt;")
    string = string.replace("\uE01B", "<b>")
    string = string.replace("\uE00B", "</b>")
    string = string.replace("\uE011", "<i>")
    string = string.replace("\uE001", "</i>")
    string = string.replace("\uE015", "<s>")
    string = string.replace("\uE005", "</s>")
    string = string.replace("\uE01F", "<tg-spoiler>")
    string = string.replace("\uE00F", "</tg-spoiler>")
    string = string.replace("\uE012", "<u>")
    string = string.replace("\uE002", "</u>")
    string = string.replace("\uE01C", "<code>")
    string = string.replace("\uE00C", "</code>")
    string = string.replace("\uE01D", "<pre>")
    string = string.replace("\uE00D", "</pre>")
    return string
