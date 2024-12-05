from typing import Any, Generator, Iterable, Literal, Optional, Union, overload

import httpx

from ...utils.logger import logger
from ...variants.variants import VariantInterface
from ..constants import PRODUCTION_BASE_URL, SSE_DONE
from ..exceptions import ServerErrorException
from ..utils import HTTPWrapper
from .interfaces import (
    ChatCompletion,
    ChatMessage,
    LogitsResponse,
    StreamingChatCompletionChunk,
)

DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant who should follow the users requests. Be brief and to the point, but also be friendly and engaging."


class ChatAPICompletions:
    """OpenAI compatible chat completions API."""

    def __init__(self, api_key: str, base_url: str = PRODUCTION_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url

        self._http = HTTPWrapper()

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
        }

    @overload
    def create(
        self,
        messages: Iterable[Union[ChatMessage, dict[str, str]]],
        model: Union[str, VariantInterface],
        *,
        stream: Literal[False] = False,
        max_completion_tokens: Optional[int] = None,
        top_p: float = 0.9,
        temperature: float = 0.6,
        stop: Optional[Union[str, list[str]]] = None,
        seed: Optional[int] = 42,
    ) -> ChatCompletion: ...

    @overload
    def create(
        self,
        messages: Iterable[Union[ChatMessage, dict[str, str]]],
        model: Union[str, VariantInterface],
        *,
        stream: Literal[True] = True,
        max_completion_tokens: Optional[int] = None,
        top_p: float = 0.9,
        temperature: float = 0.6,
        stop: Optional[Union[str, list[str]]] = None,
        seed: Optional[int] = 42,
    ) -> Generator[StreamingChatCompletionChunk, Any, Any]: ...

    def create(
        self,
        messages: Iterable[Union[ChatMessage, dict[str, str]]],
        model: Union[str, VariantInterface],
        stream: bool = False,
        max_completion_tokens: Optional[int] = 2048,
        top_p: float = 0.9,
        temperature: float = 0.6,
        stop: Optional[Union[str, list[str]]] = ["<|eot_id|>", "<|begin_of_text|>"],
        timeout: Optional[int] = 320,
        seed: Optional[int] = 42,
        __system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    ) -> Union[ChatCompletion, Generator[StreamingChatCompletionChunk, Any, Any]]:
        """Create a chat completion."""
        url = f"{self.base_url}/api/inference/v1/chat/completions"

        headers = self._get_headers()

        if __system_prompt != DEFAULT_SYSTEM_PROMPT:
            logger.warning(
                "We recommend using Goodfire's default system prompt to maximize intervention stability."
            )

        messages = [*messages]
        if __system_prompt:
            messages.insert(0, {"role": "system", "content": __system_prompt})

        payload: dict[str, Any] = {
            "messages": messages,
            "stream": stream,
            "max_completion_tokens": max_completion_tokens,
            "top_p": top_p,
            "temperature": temperature,
            "stop": stop,
            "seed": seed,
        }

        if isinstance(model, str):
            payload["model"] = model
        else:
            payload["model"] = model.base_model
            payload["controller"] = model.controller.json()

        if stream:

            def _stream_response() -> Generator[StreamingChatCompletionChunk, Any, Any]:
                try:
                    for chunk in self._http.stream(
                        "POST",
                        url,
                        headers={
                            **headers,
                            "Accept": "text/event-stream",
                            "Connection": "keep-alive",
                        },
                        json=payload,
                        timeout=timeout,
                    ):
                        chunk = chunk.decode("utf-8")

                        if chunk == SSE_DONE:
                            break

                        json_chunk = chunk.split("data: ")[1].strip()

                        yield StreamingChatCompletionChunk.model_validate_json(
                            json_chunk
                        )
                except httpx.RemoteProtocolError:
                    raise ServerErrorException()

            return _stream_response()
        else:
            response = self._http.post(
                url,
                headers={
                    **headers,
                    "Accept": "application/json",
                },
                json=payload,
                timeout=timeout,
            )

            return ChatCompletion.model_validate(response.json())


class ExperimentalChatAPI:
    """Experimental chat API."""

    def __init__(self, chat_api: "ChatAPI"):
        self.chat_api = chat_api

        self._warned_user = False

        self._http = HTTPWrapper()

    def _warn_user(self):
        if not self._warned_user:
            print("Warning: The experimental chat API is subject to change.")
            self._warned_user = True

    def logits(
        self,
        messages: Iterable[Union[ChatMessage, dict[str, str]]],
        model: Union[str, VariantInterface],
        top_k: Optional[int] = None,
        vocabulary: Optional[list[str]] = None,
    ) -> LogitsResponse:
        """Compute logits for a chat completion."""
        payload: dict[str, Any] = {
            "messages": messages,
            "k": top_k,
            "vocabulary": vocabulary,
        }

        if isinstance(model, str):
            payload["model"] = model
        else:
            payload["model"] = model.base_model
            payload["controller"] = model.controller.json()

        response = self._http.post(
            f"{self.chat_api.base_url}/api/inference/v1/chat/compute-logits",
            headers={
                **self.chat_api._get_headers(),
            },
            json=payload,
        )

        return LogitsResponse.model_validate(response.json())


class ChatAPI:
    """OpenAI compatible chat API."""

    def __init__(self, api_key: str, base_url: str = PRODUCTION_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url
        self.completions = ChatAPICompletions(api_key, base_url)
        self._experimental = ExperimentalChatAPI(self)

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
