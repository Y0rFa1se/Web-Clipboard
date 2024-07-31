import markdown
import re

def text2md(text):
    return markdown.markdown(text)

def filter(md_content):
    # Regex to find markdown links and images with file:// schema
    link_pattern = r'\[([^\[]+)\]\((file:\/\/\/[^\)]+)\)'
    image_pattern = r'!\[([^\[]*)\]\((file:\/\/\/[^\)]+)\)'
    html_link_pattern = r'<a\s+href="file:\/\/\/[^"]+">([^<]+)<\/a>'
    html_image_pattern = r'<img\s+src="file:\/\/\/[^"]+"[^>]*>'

    # Replace local file links and images with a placeholder or empty string
    if (re.search(link_pattern, md_content) or
        re.search(image_pattern, md_content) or
        re.search(html_link_pattern, md_content) or
        re.search(html_image_pattern, md_content)):
        return False

    return True


if __name__ == "__main__":
    md_content = """
    This is a [local file](file:///C:/Users/Example/file.txt) link.
    This is an ![local image](file:///C:/Users/Example/image.png).
    This is an <a href="file:///C:/Users/Example/file.txt">HTML local file link</a>.
    This is an <img src="file:///C:/Users/Example/image.png" alt="HTML local image">
    hihi
    ![](https://example.com/image.png)
    """

    print(filter(md_content))
