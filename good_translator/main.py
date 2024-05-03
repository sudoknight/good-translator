import time
from typing import List, Tuple, Union

from deep_translator import GoogleTranslator
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

from .config import local_model
from .lang_detect import LangDetect


class GoodTranslator:

    def __init__(
        self, load_google_trans: bool = True, load_local_model: bool = True
    ) -> None:
        """
        Args:
            load_google_trans: Whether to load and use google translation model. Defaults to True.
            load_local_model: Whether to load and use offline mode for translation. Defaults to True.
        """

        self.load_google_trans = load_google_trans
        self.load_local_model = load_local_model

        print("Initialization Start")
        t = time.time()
        if load_local_model:
            # LOAD local translation model
            self.local_translate_model, self.local_tokenizer = (
                self._load_translate_local_model()
            )
            print(f"Local Model Loaded: {time.time()-t}")
            self.lang_detect_model = LangDetect()

        if load_google_trans:
            # LOAD google translation object
            self.google_translate = self._load_google_translate_model()
            print(f"Google Translation Object Loaded: {time.time()-t}")

        if not load_local_model and not load_google_trans:
            raise Exception(
                "No model was loaded. Load atleast one model from (load_google_trans, load_local_model)"
            )
        print(f"Initialization Complete {time.time()-t}")

    def _load_translate_local_model(self):
        """Loads model and tokenizer from hugging face"""

        print("Loading model: ", local_model)
        l_model = M2M100ForConditionalGeneration.from_pretrained(local_model)
        l_tokenizer = M2M100Tokenizer.from_pretrained(local_model)
        print("Loading Model Complete")
        return l_model, l_tokenizer

    def _load_google_translate_model(self):
        """Loads google Translate model"""
        print("Loading Google Tranlation object")
        gt = GoogleTranslator(source="auto", target="en")
        print("Loading Object Complete")
        return gt

    def tranlsate_by_google(self, text: str) -> Union[str | None]:
        """Translation by google

        Args:
            text: string to translate

        Returns:
            translated text or None in case of execption or null result
        """

        try:
            r = self.google_translate.translate(text=text)
            if len(r):
                return r.strip()

        except Exception as ex:
            print("Google Translation failed for: ", text, ex)

        return None

    def translate_by_model(self, src_lang, text: str) -> Union[str, None]:
        """Translation by local model.

        Args:
            src_lang: source language for the model
            text: text to translate

        Returns:
            translated text or None in case of execption or null result
        """
        try:
            self.local_tokenizer.src_lang = src_lang
            encoded_hi = self.local_tokenizer(text, return_tensors="pt")
            generated_tokens = self.local_translate_model.generate(
                **encoded_hi, forced_bos_token_id=self.local_tokenizer.get_lang_id("en")
            )
            r = self.local_tokenizer.batch_decode(
                generated_tokens, skip_special_tokens=True
            )

            if len(r):
                return r.strip()

        except Exception as ex:
            print("Local Translation Model failed for: ", text, ex)

        return None

    def translate(self, text: str) -> Union[str, None]:
        """Translates the text using google translation model and offline model.
        If one model fails, the other one is used.


        Args:
            text: text to translate

        Returns:
            tranlated text or None when no translation is performed
        """

        if text is None or not isinstance(text, str):
            print("Passed text is invalid value.")
            return None

        if len(text) < 1:
            print("Passed text has zero length.")
            return None

        if self.load_google_trans:
            res = self.tranlsate_by_google(text)
            if res:  # If not None and has valid value
                return res
            else:
                print("Got no result from Google Translation for: ", text)

        if self.load_local_model:
            lang = self.lang_detect_model._detect(text)
            res = self.translate_by_model(lang, text)
            if res:  # If not None and has valid value
                return res
            else:
                print("Got no result from Local Translation Model for: ", text)

        return None

    def batch_translate(
        self, ls_texts: List[str]
    ) -> List[Tuple[str, Union[str, None]]]:
        """Tranlates batch of texts

        Args:
            ls_texts: list of strings to translate

        Returns:
            list of tuples [ (<original_text>, <translated_text>) ]
        """

        results = []
        for text in ls_texts:
            r = self.translate(text)
            results.append((text, r))
        return results


if __name__ == "__main__":
    gt = GoodTranslator()
    print(gt)
    t = "رائعة بكل المقاييس. ___ كل شيء كان استثنائي شكرا من القلب واخص الانسة مريم لذوقها الرفيع وحسن تعاملها. ___ كل شيء."
    r = gt.translate(t)
    print(r)
