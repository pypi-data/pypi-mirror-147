# Keytotext Trainer

Keytotext now features a trainer module that can help finetune any model to convert keywords to sentences.

This features many fucntions that are described below:

- ##### Download T5 model from HuggingFace Hub 

```python
def from_pretrained(self, model_name="t5-base"):
    """
    Download Model from HF hub
    :param model_name: T5
    :return: Download the model and tokenizer
    """
```

- ##### Train the Model

```python
    def train(
            self,
            data_df: pd.DataFrame,
            source_max_token_len: int = 512,
            target_max_token_len: int = 512,
            batch_size: int = 8,
            max_epochs: int = 5,
            use_gpu: bool = True,
            outputdir: str = "outputs",
            early_stopping_patience_epochs: int = 0,  # 0 to disable early stopping feature
            test_split=0.1,
    ):
        """
        trains T5 model on custom dataset
        Args:
            data_df (pd.DataFrame): training datarame. Dataframe must have 2 column --> "keywords" and "text"
            source_max_token_len (int, optional): max token length of source text. Defaults to 512.
            target_max_token_len (int, optional): max token length of target text. Defaults to 512.
            batch_size (int, optional): batch size. Defaults to 8.
            max_epochs (int, optional): max number of epochs. Defaults to 5.
            use_gpu (bool, optional): if True, model uses gpu for training. Defaults to True.
            outputdir (str, optional): output directory to save model checkpoints. Defaults to "outputs".
            early_stopping_patience_epochs (int, optional): monitors val_loss on epoch end and stops training, if val_loss does not improve after the specied number of epochs. set 0 to disable early stopping. Defaults to 0 (disabled)
        """
```

- ##### Load Model for testing

```python
    def load_model(
            self, model_dir: str = "outputs", use_gpu: bool = False
    ):
        """
        loads a checkpoint for inferencing/prediction
        Args:
            model_dir (str, optional): path to model directory. Defaults to "outputs".
            use_gpu (bool, optional): if True, model uses gpu for inferencing/prediction. Defaults to True.
        """
```

- ##### Save model to directory

```python
    def save_model(
            self,
            model_dir="outputs"
    ):
        """
        Save model to dir
        :param model_dir:
        :return: model is saved
        """
```

- ##### Make a prediction using model

```python
    def predict(
            self,
            keywords: list,
            max_length: int = 512,
            num_return_sequences: int = 1,
            num_beams: int = 2,
            top_k: int = 50,
            top_p: float = 0.95,
            do_sample: bool = True,
            repetition_penalty: float = 2.5,
            length_penalty: float = 1.0,
            early_stopping: bool = True,
            skip_special_tokens: bool = True,
            clean_up_tokenization_spaces: bool = True,
            use_gpu: bool = True
    ):
        """
        generates prediction for K2T model
        Args:
            Keywords (list): any keywords for generating predictions
            max_length (int, optional): max token length of prediction. Defaults to 512.
            num_return_sequences (int, optional): number of predictions to be returned. Defaults to 1.
            num_beams (int, optional): number of beams. Defaults to 2.
            top_k (int, optional): Defaults to 50.
            top_p (float, optional): Defaults to 0.95.
            do_sample (bool, optional): Defaults to True.
            repetition_penalty (float, optional): Defaults to 2.5.
            length_penalty (float, optional): Defaults to 1.0.
            early_stopping (bool, optional): Defaults to True.
            skip_special_tokens (bool, optional): Defaults to True.
            clean_up_tokenization_spaces (bool, optional): Defaults to True.
            use_gpu: Defaults to True.
        Returns:
            str: returns predictions
        """
```

#### Upload to huggingface

```python
model.upload(hf_username="gagan3012", model_name="k2t-test3")
```
