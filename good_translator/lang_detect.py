from typing import Union

import fasttext
from .config import m2m_lang_mapping
from huggingface_hub import hf_hub_download


class LangDetect:

    def __init__(self) -> None:
        self._model = self._load_lang_detect_local_model()

    def _load_lang_detect_local_model(self):
        # Download models if not already present
        model_path = hf_hub_download(
            repo_id="facebook/fasttext-language-identification",
            filename="model.bin",
        )
        # Load the model
        model = fasttext.load_model(model_path)
        print("Lang Detect Model Loaded: ", model_path)
        return model

    def _detect(self, text: str) -> Union[str, None]:
        """Detects language of the passed text.

        Args:
            text: detect language of this passed text

        Returns:
            detected language or None
        """
        pred_label = None
        short_code = None
        try:
            r = self._model.predict(text)
            pred_label = r[0][0]
            short_code = m2m_lang_mapping[pred_label]
            return short_code
        except Exception as ex:
            print(f"Unable to Detect langauge: {text}  {ex}")

        return None

    def _clear_memory(self):
        del self._model


if __name__ == "__main__":
    ld = LangDetect()
    print(ld)
