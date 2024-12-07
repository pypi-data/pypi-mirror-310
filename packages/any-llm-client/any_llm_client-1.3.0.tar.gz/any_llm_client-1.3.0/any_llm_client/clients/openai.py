import contextlib
import dataclasses
import os
import types
import typing
from http import HTTPStatus

import annotated_types
import niquests
import pydantic
import typing_extensions

from any_llm_client.core import (
    LLMClient,
    LLMConfig,
    LLMError,
    Message,
    MessageRole,
    OutOfTokensOrSymbolsError,
    UserMessage,
)
from any_llm_client.http import HttpClient, HttpStatusError
from any_llm_client.retry import RequestRetryConfig
from any_llm_client.sse import parse_sse_events


OPENAI_AUTH_TOKEN_ENV_NAME: typing.Final = "ANY_LLM_CLIENT_OPENAI_AUTH_TOKEN"


class OpenAIConfig(LLMConfig):
    if typing.TYPE_CHECKING:
        url: str
    else:
        url: pydantic.HttpUrl
    auth_token: str | None = pydantic.Field(default_factory=lambda: os.environ.get(OPENAI_AUTH_TOKEN_ENV_NAME))
    model_name: str
    force_user_assistant_message_alternation: bool = False
    "Gemma 2 doesn't support {role: system, text: ...} message, and requires alternated messages"
    api_type: typing.Literal["openai"] = "openai"


class ChatCompletionsMessage(pydantic.BaseModel):
    role: MessageRole
    content: str


class ChatCompletionsRequest(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="allow")
    stream: bool
    model: str
    messages: list[ChatCompletionsMessage]
    temperature: float = 0.2


class OneStreamingChoiceDelta(pydantic.BaseModel):
    role: typing.Literal[MessageRole.assistant] | None = None
    content: str | None = None


class OneStreamingChoice(pydantic.BaseModel):
    delta: OneStreamingChoiceDelta


class ChatCompletionsStreamingEvent(pydantic.BaseModel):
    choices: typing.Annotated[list[OneStreamingChoice], annotated_types.MinLen(1)]


class OneNotStreamingChoice(pydantic.BaseModel):
    message: ChatCompletionsMessage


class ChatCompletionsNotStreamingResponse(pydantic.BaseModel):
    choices: typing.Annotated[list[OneNotStreamingChoice], annotated_types.MinLen(1)]


def _make_user_assistant_alternate_messages(
    messages: typing.Iterable[ChatCompletionsMessage],
) -> typing.Iterable[ChatCompletionsMessage]:
    current_message_role = MessageRole.user
    current_message_content_chunks = []

    for one_message in messages:
        if not one_message.content.strip():
            continue

        if (
            one_message.role in {MessageRole.system, MessageRole.user} and current_message_role == MessageRole.user
        ) or one_message.role == current_message_role == MessageRole.assistant:
            current_message_content_chunks.append(one_message.content)
        else:
            if current_message_content_chunks:
                yield ChatCompletionsMessage(
                    role=current_message_role, content="\n\n".join(current_message_content_chunks)
                )
            current_message_content_chunks = [one_message.content]
            current_message_role = one_message.role

    if current_message_content_chunks:
        yield ChatCompletionsMessage(role=current_message_role, content="\n\n".join(current_message_content_chunks))


def _handle_status_error(error: HttpStatusError) -> typing.NoReturn:
    if (
        error.status_code == HTTPStatus.BAD_REQUEST and b"Please reduce the length of the messages" in error.content
    ):  # vLLM
        raise OutOfTokensOrSymbolsError(response_content=error.content)
    raise LLMError(response_content=error.content)


@dataclasses.dataclass(slots=True, init=False)
class OpenAIClient(LLMClient):
    config: OpenAIConfig
    http_client: HttpClient
    request_retry: RequestRetryConfig

    def __init__(
        self,
        config: OpenAIConfig,
        *,
        request_retry: RequestRetryConfig | None = None,
        **niquests_kwargs: typing.Any,  # noqa: ANN401
    ) -> None:
        self.config = config
        self.http_client = HttpClient(
            request_retry=request_retry or RequestRetryConfig(), niquests_kwargs=niquests_kwargs
        )

    def _build_request(self, payload: dict[str, typing.Any]) -> niquests.Request:
        return niquests.Request(
            method="POST",
            url=str(self.config.url),
            json=payload,
            headers={"Authorization": f"Bearer {self.config.auth_token}"} if self.config.auth_token else None,
        )

    def _prepare_messages(self, messages: str | list[Message]) -> list[ChatCompletionsMessage]:
        messages = [UserMessage(messages)] if isinstance(messages, str) else messages
        initial_messages: typing.Final = (
            ChatCompletionsMessage(role=one_message.role, content=one_message.text) for one_message in messages
        )
        return (
            list(_make_user_assistant_alternate_messages(initial_messages))
            if self.config.force_user_assistant_message_alternation
            else list(initial_messages)
        )

    async def request_llm_message(
        self, messages: str | list[Message], *, temperature: float = 0.2, extra: dict[str, typing.Any] | None = None
    ) -> str:
        payload: typing.Final = ChatCompletionsRequest(
            stream=False,
            model=self.config.model_name,
            messages=self._prepare_messages(messages),
            temperature=temperature,
            **extra or {},
        ).model_dump(mode="json")
        try:
            response: typing.Final = await self.http_client.request(self._build_request(payload))
        except HttpStatusError as exception:
            _handle_status_error(exception)
        return ChatCompletionsNotStreamingResponse.model_validate_json(response).choices[0].message.content

    async def _iter_partial_responses(self, response: typing.AsyncIterable[bytes]) -> typing.AsyncIterable[str]:
        text_chunks: typing.Final = []
        async for one_event in parse_sse_events(response):
            if one_event.data == "[DONE]":
                break
            validated_response = ChatCompletionsStreamingEvent.model_validate_json(one_event.data)
            if not (one_chunk := validated_response.choices[0].delta.content):
                continue
            text_chunks.append(one_chunk)
            yield "".join(text_chunks)

    @contextlib.asynccontextmanager
    async def stream_llm_partial_messages(
        self, messages: str | list[Message], *, temperature: float = 0.2, extra: dict[str, typing.Any] | None = None
    ) -> typing.AsyncIterator[typing.AsyncIterable[str]]:
        payload: typing.Final = ChatCompletionsRequest(
            stream=True,
            model=self.config.model_name,
            messages=self._prepare_messages(messages),
            temperature=temperature,
            **extra or {},
        ).model_dump(mode="json")
        try:
            async with self.http_client.stream(request=self._build_request(payload)) as response:
                yield self._iter_partial_responses(response)
        except HttpStatusError as exception:
            _handle_status_error(exception)

    async def __aenter__(self) -> typing_extensions.Self:
        await self.http_client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        await self.http_client.__aexit__(exc_type=exc_type, exc_value=exc_value, traceback=traceback)
