import unittest

from extractors import extract_markdown_images, extract_markdown_links

class TestExtractImagesLinks(unittest.TestCase):

    def test_exct_only_imgs(self):
        text = "Text and image: ![image](link to image)"
        result_img = extract_markdown_images(text)
        result_link = extract_markdown_links(text)
        target_img = [('image', 'link to image')]
        target_link = []
        self.assertEqual(result_img, target_img)
        self.assertEqual(result_link, target_link)

    def test_exct_only_links(self):
        text = "Text and link: [link text](link)"
        result_img = extract_markdown_images(text)
        result_link = extract_markdown_links(text)
        target_link = [('link text', 'link')]
        target_img = []
        self.assertEqual(result_img, target_img)
        self.assertEqual(result_link, target_link)

    def test_exct_neither(self):
        text = "Just text [ and random ] characters ( )"
        result_img = extract_markdown_images(text)
        result_link = extract_markdown_links(text)
        target_link = []
        target_img = []
        self.assertEqual(result_img, target_img)
        self.assertEqual(result_link, target_link)

    def test_exct_both(self):
        text = "[both](link) link and image ![image](link to image) in this one"
        result_img = extract_markdown_images(text)
        result_link = extract_markdown_links(text)
        target_img = [('image', 'link to image')]
        target_link = [('both', 'link')]
        self.assertEqual(result_img, target_img)
        self.assertEqual(result_link, target_link)

    def test_exct_multiples_of_both(self):
        text = "![funny image](link to image1) [Here](boot.dev) you can learn all kinds of [funny](wikipedia.com/funny) things ![serious image](link to image2)"
        result_img = extract_markdown_images(text)
        result_link = extract_markdown_links(text)
        target_img = [('funny image', 'link to image1'), ('serious image', 'link to image2')]
        target_link = [('Here', 'boot.dev'), ('funny', 'wikipedia.com/funny')]
        self.assertEqual(result_img, target_img)
        self.assertEqual(result_link, target_link)


if __name__ == '__main__':
     unittest.main()