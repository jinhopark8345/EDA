
# About [FUNSD Dataset](https://guillaumejaume.github.io/FUNSD/)
FUNSD stands for **Form Understanding in Noisy Scanned Documents**.

It is a dataset for Text Detection, Optical Character Recognition, Spatial Layout Analysis and Form Understanding.

- FUNSD dataset has roughly 150/50 train/test samples. 
- each sample has it's own annotation data in following json format.
```json
{
    "form": [
            ...

            {
                "box": [656, 742, 680, 836],
                "text": "00070353",
                "label": "other",
                "words": [
                    {"box": [656, 742, 680, 836], "text": "00070353"}
                ],
                "linking": [],
                "id": 8
            },
            {
                "text": "Manuscript Review Form",
                "box": [96, 67, 253, 84],
                "linking": [],
                "label": "other",
                "words": [
                    {"text": "Manuscript", "box": [96, 67, 163, 84]},
                    {"text": "Review", "box": [169, 68, 212, 83]},
                    {"text": "Form", "box": [218, 68, 253, 83]}
                ],
                "id": 9
            },

            ...
    ]

}
```
- Each element of form is an entity.
- Each entity has words that has single or multiple of text_boxes

### Visualize one sample

![sample2](../../assets/funsd_vis_sample/716552.jpeg)
*Above image is a visualized sample of FUNSD dataset*


From above image,

 - Red boxes : The words(texts) in each of red boxes are the words of one entity
 - Red arrows : links between entities
 - Red numbers : entity indices in FUNSD dataset (orders of them)
 - Green boxes : Each word has its own box
 - Green numbers : orders of words in each entity

Entities are like "NEW ITEM", "DESCRIPTION", "VICEROY Rich Lights" in the image below. (They are in red boxes)
Entities are consist of single/multiple words like "DESCRIPTION", "NEW ITEM" and "VICEROY Rich Lights"

### Find other visualized samples
You can find other visualized samples [here](https://drive.google.com/file/d/1M3z-KKxx4JdGBb7TQIHyRyiL2KtGDAZ2/view?usp=drive_link) 

### If you want to visualize yourself,

```bash
# (optional) prepare dataset
python3 tools/prepare_funsd_dataset.py

# Run FUNSD visualizer
python3 tools/vis_funsd.py
```
