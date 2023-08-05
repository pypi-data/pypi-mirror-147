<h1 align="center">keytotext</h1>

[![pypi Version](https://img.shields.io/pypi/v/keytotext.svg?logo=pypi&logoColor=white)](https://pypi.org/project/keytotext/)
[![Downloads](https://static.pepy.tech/personalized-badge/keytotext?period=total&units=none&left_color=grey&right_color=orange&left_text=Pip%20Downloads)](https://pepy.tech/project/keytotext)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gagan3012/keytotext/blob/master/notebooks/K2T.ipynb)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/gagan3012/keytotext/UI/app.py)
[![API Call](https://img.shields.io/badge/-FastAPI-red?logo=fastapi&labelColor=white)](https://github.com/gagan3012/keytotext#api)
[![Docker Call](https://img.shields.io/badge/-Docker%20Image-blue?logo=docker&labelColor=white)](https://hub.docker.com/r/gagan30/keytotext)
[![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97-Models%20on%20Hub-yellow)](https://huggingface.co/models?filter=keytotext)
[![Documentation Status](https://readthedocs.org/projects/keytotext/badge/?version=latest)](https://keytotext.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)



![keytotext](https://socialify.git.ci/gagan3012/keytotext/image?description=1&forks=1&language=1&owner=1&stargazers=1&theme=Light)


Idea is to build a model which will take keywords as inputs and generate sentences as outputs.

Potential use case can include: 
- Marketing 
- Search Engine Optimization
- Topic generation etc.
- Fine tuning of topic modeling models 

## Model:

Keytotext is based on the Amazing T5 Model: [![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97-Models%20on%20Hub-yellow)](https://huggingface.co/models?filter=keytotext)

- `k2t`: [Model](https://huggingface.co/gagan3012/k2t)
- `k2t-tiny`: [Model](https://huggingface.co/gagan3012/k2t-tiny)
- `k2t-base`: [Model](https://huggingface.co/gagan3012/k2t-base)
- `mrm8488/t5-base-finetuned-common_gen` (by Manuel Romero): [Model](https://huggingface.co/mrm8488/t5-base-finetuned-common_gen)

Training Notebooks can be found in the [`Training Notebooks`](https://github.com/gagan3012/keytotext/tree/master/notebooks) Folder

**Note**: To add your own model to keytotext Please read [`Models Documentation`](https://github.com/gagan3012/keytotext/blob/master/docs/MODELS.md)

## Usage:

Example usage: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gagan3012/keytotext/blob/master/notebooks/K2T.ipynb)

Example Notebooks can be found in the [`Notebooks`](https://github.com/gagan3012/keytotext/tree/master/examples) Folder

```shell script
pip install keytotext
```

![carbon (3)](https://user-images.githubusercontent.com/49101362/116220679-90e64180-a755-11eb-9246-82d93d924a6c.png)

## Trainer:

Keytotext now has a trainer class than be used to train and finetune any T5 based model on new data. Trainer docs here: [`Docs`](https://github.com/gagan3012/keytotext/blob/master/docs/TRAINER.md)

Trainer example here: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gagan3012/keytotext/blob/master/notebooks/Trainer.ipynb)

```python
from keytotext import trainer
```

![carbon (6)](https://user-images.githubusercontent.com/49101362/125130656-5989fe80-e0cf-11eb-8c07-c659767911b4.png)

## UI:

UI: [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/gagan3012/keytotext/UI/app.py)

```shell script
pip install streamlit-tags
```
This uses a custom streamlit component built by me: [GitHub](https://github.com/gagan3012/streamlit-tags)

![image](https://user-images.githubusercontent.com/49101362/116162205-fc042980-a6fd-11eb-892e-8f6902f193f4.png)

## API:

API: [![API Call](https://img.shields.io/badge/-Open%20with%20FastAPI-red?logo=fastapi&labelColor=white)](http://localhost:8000/api?data=[%22India%22,%22Capital%22,%22New%20Delhi%22])
[![Docker Call](https://img.shields.io/badge/-Docker%20Image-blue?logo=docker&labelColor=white)](https://hub.docker.com/r/gagan30/keytotext)

The API is hosted in the Docker container and it can be run quickly.
Follow instructions below to get started

```shell script
docker pull gagan30/keytotext

docker run -dp 8000:8000 gagan30/keytotext
```

This will start the api at port 8000 visit the url below to get the results as below:
```
http://localhost:8000/api?data=["India","Capital","New Delhi"]
```

![k2t_json](https://user-images.githubusercontent.com/49101362/117046515-c56e7600-acde-11eb-8a20-7e1ab5f0de02.png)

Note: The Hosted API is only available on demand
## BibTex:

To quote keytotext please use this citation

```bibtex
@misc{bhatia, 
      title={keytotext},
      url={https://github.com/gagan3012/keytotext}, 
      journal={GitHub}, 
      author={Bhatia, Gagan}
}
```

# References 
- https://github.com/Shivanandroy/simpleT5 (Shivanand Roy)
- https://github.com/patil-suraj/question_generation (Suraj Patil)
- https://github.com/MathewAlexander/T5_nlg (Mathew Alexander)


## Articles about keytotext:

- https://towardsdatascience.com/data-to-text-generation-with-t5-building-a-simple-yet-advanced-nlg-model-b5cce5a6df45 (Mathew Alexander)
- Amazing Video by [1LittleCoder](https://twitter.com/1littlecoder) here: https://www.youtube.com/watch?v=I0iBzP-SxFY about keytotext
- https://medium.com/mlearning-ai/generating-sentences-from-keywords-using-transformers-in-nlp-e89f4de5cf6b (Prakhar Mishra)
