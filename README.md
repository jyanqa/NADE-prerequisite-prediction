# Learning concept prerequisite prediction in educational data

## Dataset Collection
- Fredin's thesis: the complete testset is added
- Mewsli-9
- Mooc-data
    - candidates: labels (1 if the candidates is a learning concepts, doubly annotated), k-gams information, text = a list of learning concepts
    - captions: courses_id, caption in text, pos tags
    - courses =  a list of videos = a list of captions
- University Course
    - courses: name, courses' description in text
    - general list of:  learning concepts, preqs relations, number of annotators
- LectureBank
    - text from pdf and pptx files #todo: to extract pdftotext and pptx2text
    - vocabulary.txt: a list of learning concepts
## Prerequisite prediction
- Dataset: ./data/data-university-course
- Code: ./code/task2-prerequisite-prediction
- Report: ./result/Anh-prerequisite_prediction.pdf

Abstract: The project aims to adapt a pretrained prompting and prediction system to handle the task of predicting prerequisite dependencies in educational data, representing a fundamental step towards automatic extraction and detection of prerequisites in educational texts. Diverging from previous approaches that treated this task as a network science puzzle, the author leveraged the capabilities of Large Language Models (LLMs), such as GPT-3.5 and Llama 2, and compared their performance to smaller pre-trained models, including T5 and GPT-2. Results indicate that utilizing smaller pre-trained models through fine-tuning and prompting can yield significantly improved results, surpassing not only those Large language models but also demonstrating higher predictive performance compared to prior methodologies. This underscores the potential advantages of harnessing ordinary pre-trained models over LLMs in terms of performance and computational resources, prompting intriguing considerations regarding the trade-offs between model size and depth.

