import markdown
import re

def text2md(text):
    return markdown.markdown(text) 

def filter(md_content):
    link_pattern = r'\[([^\[]+)\]\((file:\/\/\/[^\)]+)\)'
    image_pattern = r'!\[([^\[]*)\]\((file:\/\/\/[^\)]+)\)'
    html_link_pattern = r'<a\s+href="file:\/\/\/[^"]+">([^<]+)<\/a>'
    html_image_pattern = r'<img\s+src="file:\/\/\/[^"]+"[^>]*>'

    has_local_links_or_images = (
        re.search(link_pattern, md_content) or
        re.search(image_pattern, md_content) or
        re.search(html_link_pattern, md_content) or
        re.search(html_image_pattern, md_content)
    )

    return not has_local_links_or_images

if __name__ == "__main__":
    md_content = """

    | asfd | asf |
    | --- | --- |
    | asf | asfd |
    
    ~~asdf~~

    asf[^1]

    [^1]: asf

    ```python
    def hello():
        print("Hello, World!")
    ```

    This is a [local file](file:///C:/Users/Example/file.txt) link.
    This is an ![local image](file:///C:/Users/Example/image.png).
    This is an <a href="file:///C:/Users/Example/file.txt">HTML local file link</a>.
    This is an <img src="file:///C:/Users/Example/image.png" alt="HTML local image">
    hihi
    ![](https://example.com/image.png)
    """

    # Convert markdown to HTML
    html_content = text2md(md_content)
    print(html_content)

    # Check if the content passes the filter
    print(filter(md_content))  # Should print False

