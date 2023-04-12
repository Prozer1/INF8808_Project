


def extract_title(title):
    title = title.strip()
    title = title.replace(" ", "")
    if title[-1].isdigit():
        return title[:-2]
    return title