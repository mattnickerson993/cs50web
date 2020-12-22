import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def  mdto_html(string_to_test):
    """
    parses markdown content into html using regex.
    Right now it sucks. only able to replace a hash with an h1
    Works for #, bold, ul, and links.
    use this function for random page, kept entry page the same
    """
    pattern1 = re.compile(r'(#{1,6})\s*([^\n]+)')
    string_to_test= pattern1.sub(r'<h1>\2</h1>', string_to_test)
    pattern2 = re.compile(r'(\*\*|__)([-\w\s]+)(\*\*|__)')
    string_to_test = pattern2.sub(r'<strong>\2</strong>', string_to_test)
    pattern3 = re.compile(r'[*]{1}\s*([^\n]+)')
    string_to_test = pattern3.sub(r'<li>\1</li>', string_to_test)
    pattern4 = re.compile(r'\[([\w\s]+)\]\s*\(([\w/:._]+)\)')
    subbed_urls = pattern4.sub(r'<a href="\2">\1</a>', string_to_test)

    return subbed_urls