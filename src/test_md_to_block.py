import unittest
from markdown_conversion import markdown_to_blocks, block_to_block_type

class TestMdToBlocks(unittest.TestCase):

    def test_block_count(self):
        text = '''# This is a heading
    
This is a paragraph of text. It has some **bold** and *italic* words inside of it.
    
* This is the first list item in a list block
* This is a list item
* This is another list item'''
        blocks = markdown_to_blocks(text)
        target_length = 3
        paragraph_two = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        self.assertEqual(len(blocks), target_length)
        self.assertEqual(blocks[1], paragraph_two)

    def test_quote_block_type(self):
        text = '''>This
>is not
>a quote'''
        block_type = block_to_block_type(text)
        target_type ='quote'
        self.assertEqual(block_type, target_type)

    def test_all_types(self):
        text = '''# This is a level 1 heading

## A level 2 heading

* An unordered
* list

1. A list
2. with
3. three items

>Some random
>quote.

```git
git status
git add
git commit
```

And finally just a paragraph'''

        blocks = markdown_to_blocks(text)
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        targets = ['heading1', 'heading2', 'ul', 'ol', 'quote', 'code', 'paragraph']

        for i in range( len(targets) ):
            self.assertEqual( block_types[i], targets[i] )


if __name__ == '__main__':
    unittest.main()