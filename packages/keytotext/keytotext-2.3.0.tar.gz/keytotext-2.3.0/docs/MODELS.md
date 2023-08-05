# How to add new models to Keytotext

Keytotext features a pipeline that can convert keywords to sentences.

Keytotext lib is built on top of the Transformers library by HuggingFace 

Follow these steps to add your model to keytotext:

1) Upload your model to `huggingface Hub` with these tags in the model card of your model:
```
language: <LANGUAGE YOUR MODEL SUPPORTS>
thumbnail: "Keywords to Sentences"
tags:
- keytotext
- k2t
- Keywords to Sentences
license: "MIT"
datasets:
- < DATASETS USED>
---
```

2) In your fork of this repository edit the following lines of the `keytotext/pipeline.py` file:

``` python
SUPPORTED_TASKS = {
    "<MODEL NAME>": {
        "impl": NMPipeline,
        "default": {
            "model": "<MODEL NAME>",
        },
    },
}
```

3) Create a PR request and Once your changes are merged you can use the model as

```python
from keytotext import pipeline

nlp = pipeline("<MODEL NAME>")

nlp(['India','wedding','Food'])
```