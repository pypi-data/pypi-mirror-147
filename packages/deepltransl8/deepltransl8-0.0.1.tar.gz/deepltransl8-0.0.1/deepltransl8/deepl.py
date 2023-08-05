import aiohttp
import langs
from typing import TypeVar, List
import errors


__base__ = "https://www2.deepl.com/"
Translation = TypeVar("Translation")


class DeepLTranslator:
    def __init__(self, *, session: aiohttp.ClientSession):
        """Initialize.

        Parameters
        ----------
        session : aiohttp.ClientSession
            The temporary session to use.
            This session will be closed automatically after request.
        """
        self.session = session

    async def translate(
        self, /, src: langs.Language, dst: langs.Language, *, text: str
    ) -> Translation:
        """Translate a text.

        Your ClientSession will be closed automatically.

        Parameters
        ----------
        src : Language
            The source language.
        dst : Language
            The target language.
        text : str
            The text to translate.

        Returns
        -------
        Translation
            The translated text.
        """
        if not isinstance(src, langs.Language):
            raise errors.InvalidLanguageException(
                "Invalid source language. Must be of type Language."
            )
        if not isinstance(dst, langs.Language):
            raise errors.InvalidLanguageException(
                "Invalid target language. Must be of type Language."
            )
        if not isinstance(text, str):
            raise errors.ReadTheDocsException(
                f"Invalid text type {type(text)}. Must be of type str."
            )
        chunks = [text[i : i + 5000] for i in range(0, len(text), 5000)]
        translations = []
        for chunk in chunks:
            async with self.session.post(
                f"{__base__}jsonrpc",
                params={"method": "LMT_handle_jobs"},
                json={
                    "jsonrpc": "2.0",
                    "method": "LMT_handle_jobs",
                    "params": {
                        "jobs": [
                            {
                                "kind": "default",
                                "sentences": [{"text": chunk, "id": 0, "prefix": ""}],
                                "raw_en_context_before": [],
                                "raw_en_context_after": [],
                                "preferred_num_beams": 1,
                            },
                        ],
                        "lang": {
                            "preference": {"weight": {}, "default": "default"},
                            "source_lang_computed": src.value,
                            "target_lang": dst.value,
                        },
                        "priority": 1,
                        "commonJobParams": {"browserType": 1, "formality": None},
                        "timestamp": 1650235671926,
                    },
                    "id": 69030005,
                },
            ) as resp:
                try:
                    resp_json: dict = await resp.json()
                except:
                    raise errors.InvalidResponseException(
                        "Invalid response from DeepL. Please try again."
                    )
                result = resp_json.get("result", {})
                _translations = result.get("translations", [{}])
                for _translation in _translations:
                    beams = _translation.get("beams", [{}])
                    for beam in beams:
                        sentences = beam.get("sentences", [{}])
                        for sentence in sentences:
                            translations.append(sentence.get("text", ""))
        await self.session.close()
        return "".join(translations)
