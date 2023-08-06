import pkgutil


def load_wordlist(file_name: str) -> list[str]:
    text = pkgutil.get_data(__name__, "data/" + file_name).decode()
    word_list = text.splitlines()
    return word_list
