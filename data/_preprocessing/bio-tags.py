'''### Problem formulation:
The data that should be created from a list of docs and the list of keywords are similar to the following:
- [[seq1], [seq2],...]
- [[bio_seq1],[bio_seq2],...]
*** Note: creating multiple lists in list.

Algorithm draft:
- preprocessing keyword list:
  - Creating [ ] = keywords_bio-tags
  - Accessing to each elements in the keywords list
    - split() each keyword, output: splitted_keywords_list = ['this', 'is', 'an', 'apple',...]
    - if the len(splitted_keywords_list) >= 2: label of the first elements is B, and the later is I
- preprocessing document list:
  - Creating [ ] = doc_bio-tags
  - Accessing to each element in the document list
      - split() each document, output: ['this', 'is', 'not', 'a', 'llm',...]
      - accessing to each element in the splitted tokens list:
        - if the element is also in the ``splitted_keywords_list``, then its tag is the corresponding tag in keywords_bio-tags list
        - otherwise, its tag is O
'''