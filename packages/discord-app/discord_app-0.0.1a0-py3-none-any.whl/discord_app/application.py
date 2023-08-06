"""
    Function wrapper for discord application interaction concept using Flask.
"""

import json
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from dataclasses import asdict, dataclass, field
import logging
from typing_extensions import Self
import requests
import requests.structures
import flask
# Added "type: ignore" so mypy won't complain nacl doesn't have stub or py.typed.
import nacl.signing     # type: ignore
import nacl.encoding    # type: ignore
import nacl.exceptions

from discord_app import user  # type: ignore

from . import discord_types
from . import interaction


def asdict_ignore_none(x: List[Tuple[str, Any]]) -> Dict[str, Any]:
    def condition(k: str, v: Any) -> bool:
        return (v is not None) and\
            (v) and \
            k[0] != "_"
    return {k: v for (k, v) in x if condition(k, v)}


def _flask_response_from_interaction(
    response: interaction.InteractionResponse,
    headers: Dict[str, str] = {},
    status: int = 200
) -> flask.Response:
    return flask.Response(
        response=json.dumps(asdict(response, dict_factory=asdict_ignore_none)),
        headers=headers,
        status=status,
        mimetype="application/json"
    )


@dataclass
class InstallParams(discord_types.DiscordDataClass):
    scopes: List[str]
    permissions: str


@dataclass
class Application(discord_types.DiscordDataClass):
    """
        Wrapper class for Discord Application Interaction model.
    """
    id: discord_types.Snowflake
    name: str
    description: str
    bot_public: bool
    bot_require_code_grant: bool
    verify_key: str
    team: Optional[Any] = None
    icon: Optional[str] = None
    rpc_origins: Optional[List[str]] = None
    terms_of_service_url: Optional[str] = None
    privacy_policy_url: Optional[str] = None
    owner: Optional[user.User] = None
    guild_id: Optional[discord_types.Snowflake] = None
    primary_sku_id: Optional[discord_types.Snowflake] = None
    slug: Optional[str] = None
    cover_image: Optional[str] = None
    flags: Optional[discord_types.ApplicationFlags] = None
    tags: Optional[List[str]] = None
    install_params: Optional[InstallParams] = None
    custom_install_url: Optional[str] = None

    # These attributes are undocumented for some reason
    summary: Optional[Any] = None
    type: Optional[Any] = None
    hook: Optional[bool] = None

    _public_key: Optional[str] = None
    _client_secret: Optional[str] = None
    _bot_token: Optional[str] = None
    _endpoint: Optional[str] = None
    _command_list: Optional[Dict[str, Any]] = field(default_factory=dict)  # type: ignore[assignment]
    _logger: Optional[logging.Logger] = None
    _previously_registered_commands: Optional[List[Dict[str, Any]]] = None

    def __post_init__(self) -> None:
        if isinstance(self.owner, dict):
            self.owner = user.User(**self.owner)  # type: ignore[unreachable]
        if isinstance(self.flags, int):
            self.flags = discord_types.ApplicationFlags(self.flags)
        if isinstance(self.install_params, dict):
            self.install_params = InstallParams(**self.install_params)  # type: ignore[unreachable]

        if self._public_key is not None and self._bot_token is not None:
            # Initializing flask
            self._flask: flask.Flask = flask.Flask(self.name)
            self._logger: logging.Logger = self._flask.logger if self._logger is None else self._logger

            def _handle_command() -> flask.Response:
                """
                    Handler for incoming message.
                """
                # Request must is application/json
                if not flask.request.is_json:
                    self._logger.warning("Invalid request: Content-Type is not application/json")  # type: ignore[union-attr]
                    return _flask_response_from_interaction(
                        interaction.InteractionResponse(
                            type=discord_types.InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                            data=interaction.InteractionResponseMessage(
                                content="Invalid message: Request content type must be json"
                            )
                        ),
                        status=400
                    )

                # Request signature verification
                verifier = nacl.signing.VerifyKey(self._public_key, nacl.encoding.HexEncoder)
                verified = False
                try:
                    verifier.verify(
                        flask.request.headers["X-Signature-Timestamp"].encode("utf-8") + flask.request.data,
                        nacl.encoding.HexEncoder.decode(flask.request.headers["X-Signature-Ed25519"])
                    )
                    verified = True
                except nacl.exceptions.BadSignatureError:
                    return _flask_response_from_interaction(
                        interaction.InteractionResponse(
                            type=discord_types.InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                            data=interaction.InteractionResponseMessage(
                                content="Invalid message: Failed to test signature"
                            )
                        ),
                        status=401
                    )
                if not verified:
                    self._logger.info("Message verification failed.")  # type: ignore[union-attr]
                    # Mandated 401 response by Discord, when signature mismatch
                    response = _flask_response_from_interaction(
                        interaction.InteractionResponse(
                            type=discord_types.InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                            data=interaction.InteractionResponseMessage(
                                content="Invalid message: Invalid signature"
                            )
                        ),
                        status=401
                    )
                    return response

                # Handle request
                try:
                    request_data = interaction.InteractionRequest(_app=self, **flask.request.json)  # type: ignore[arg-type]
                except TypeError as e:
                    # TypeError is raised when missing attributes
                    self._logger.warning(str(e))  # type: ignore[union-attr]
                    return _flask_response_from_interaction(
                        interaction.InteractionResponse(
                            type=discord_types.InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                            data=interaction.InteractionResponseMessage(
                                content="Invalid message: missing attributes"
                            )
                        ),
                        status=400
                    )

                if request_data.type == discord_types.InteractionType.PING:
                    self._logger.info("Ping event detected.")  # type: ignore[union-attr]
                    return _flask_response_from_interaction(
                        interaction.InteractionResponse(type=discord_types.InteractionCallbackType.PONG)
                    )

                elif request_data.type == discord_types.InteractionType.APPLICATION_COMMAND:
                    if request_data.data.name in self._command_list:  # type: ignore[union-attr, operator]
                        self._logger.info(  # type: ignore[union-attr]
                            "'%s' function is called using command '%s'.",
                            self._command_list[request_data.data.name]["function"].__name__,  # type: ignore[union-attr, index]
                            request_data.data.name  # type: ignore[union-attr]
                        )
                        command_response: interaction.InteractionResponse = \
                            self._command_list[request_data.data.name]["function"](request_data)  # type: ignore[union-attr, index]
                        return _flask_response_from_interaction(command_response)
                    self._logger.warning(  # type: ignore[union-attr]
                        "Handler for command '%s' is not found.",
                        request_data.data.name  # type: ignore[union-attr]
                    )
                    return _flask_response_from_interaction(
                        interaction.InteractionResponse(
                            type=discord_types.InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
                            data=interaction.InteractionResponseMessage(
                                content="No such command"
                            )
                        ),
                        status=404
                    )

                elif request_data.type == discord_types.InteractionType.MESSAGE_COMPONENT:
                    # TODO: implement here
                    return _flask_response_from_interaction(
                        interaction.InteractionResponse(
                            type=discord_types.InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                            data=interaction.InteractionResponseMessage(
                                content="Function not implemented"
                            )
                        ),
                        status=501
                    )
                elif request_data.type == discord_types.InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE:
                    # TODO: implement here
                    return _flask_response_from_interaction(
                        interaction.InteractionResponse(
                            type=discord_types.InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                            data=interaction.InteractionResponseMessage(
                                content="Function not implemented"
                            )
                        ),
                        status=501
                    )
                elif request_data.type == discord_types.InteractionType.MODAL_SUBMIT:
                    # TODO: implement here
                    return _flask_response_from_interaction(
                        interaction.InteractionResponse(
                            type=discord_types.InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                            data=interaction.InteractionResponseMessage(
                                content="Function not implemented"
                            )
                        ),
                        status=501
                    )
                else:
                    # Unrecognized message type
                    self._logger.warning(  # type: ignore[union-attr]
                        "Invalid request: Unknown type: %s",
                        str(request_data.type)
                    )
                    return _flask_response_from_interaction(
                        interaction.InteractionResponse(
                            type=discord_types.InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                            data=interaction.InteractionResponseMessage(
                                content="Invalid interaction type"
                            )
                        ),
                        status=400
                    )

            self._handle_command = _handle_command

            # Register command router
            self._flask.route(
                self._endpoint if self._endpoint else "/",
                methods=["POST"]
            )(_handle_command)
            (self._previously_registered_commands, _) = self.call_api(  # type: ignore[misc]
                "GET",
                f"/applications/{self.id}/commands"
            )

    @property
    def _is_authorized(self) -> bool:
        return bool(self._bot_token and self._public_key)

    def call_api(
        self,
        method: str,
        path: str,
        headers: Union[requests.structures.CaseInsensitiveDict[Any], dict[str, str], None] = None,
        data: Optional[bytes] = None,
        json: Optional[object] = None,
        use_bot_token: bool = True
    ) -> Optional[Tuple[Any, requests.Response]]:
        if headers is None:
            headers = requests.structures.CaseInsensitiveDict()
        if isinstance(headers, dict):
            headers = requests.structures.CaseInsensitiveDict(headers)
        if "Authorization" not in headers:
            if use_bot_token:
                headers["Authorization"] = f"Bot {self._bot_token}"
        kwargs: Dict[str, Any] = {
            "method": method,
            "url": f"https://discord.com/api/v8{path}",
            "headers": headers
        }
        if data and json:
            raise RuntimeError("body and json are specified at the same time")
        if data:
            kwargs["data"] = data
        if json:
            kwargs["json"] = json
            if "Content-Type" not in kwargs["headers"]:
                kwargs["headers"]["Content-Type"] = "application/json"
        response = requests.request(**kwargs)
        response.raise_for_status()
        if response.status_code == 204:
            # 204 No Content
            return None, response
        if "Content-Type" in response.headers and response.headers["Content-Type"].lower() == "application/json":
            return response.json(), response  # type: ignore[no-any-return]
        else:
            raise RuntimeError(f"Server responded with unexpected content type: {response.headers['Content-Type']}")

    def application_command(self, options: interaction.ApplicationCommand, register_on_change: bool = True) -> Callable[[Any], Any]:
        """
            Define the following function as command handler.
            The command spec, , is defined as "option" parameter.

            This decorator can also register the new spec if change has been detected.
            Set "register_on_change" to False to disable it.

            Usage example:

            ```
            @app.application_command(command_spec, register_on_change=False)
            def my_command(discord_request):
                # Do things
                ...
            ```
        """
        if not self._is_authorized:
            raise RuntimeError("Unable to register a command that you have no control of. (Missing public_key and bot_token)")

        def decorator(
            function: Callable[[interaction.InteractionRequest], interaction.InteractionResponse]
        ) -> Callable[[interaction.InteractionRequest], interaction.InteractionResponse]:
            self._command_list[options.name] = {  # type: ignore[index]
                "function": function,
                "options": options
            }

            same_command_spec = False
            prev_option = next(
                (command for command in self._previously_registered_commands  # type: ignore[union-attr]
                    if command['name'] == options.name),
                None
            )
            if prev_option is not None:
                # Is a registered command, detect if command spec has changed.
                prev_option = interaction.ApplicationCommand(**prev_option)
                new_options = interaction.ApplicationCommand(**(
                    asdict(prev_option, dict_factory=asdict_ignore_none) |
                    asdict(options, dict_factory=asdict_ignore_none)))
                same_command_spec = (new_options == prev_option)
            if not same_command_spec:
                if prev_option is None:
                    self._logger.info("Registering new command %s", options.name)  # type: ignore[union-attr]
                    (_, response) = self.call_api(  # type: ignore[misc]
                        method="POST",
                        path=f"/applications/{self.id}/commands",
                        headers={"Content-Type": "application/json"},
                        json=asdict(options, dict_factory=asdict_ignore_none)
                    )
                    self._logger.info(f"Registration retruned with status code {response.status_code}")  # type: ignore[union-attr]
                else:
                    self._logger.info("Command specification has changed: %s", options.name)  # type: ignore[union-attr]
                    self._logger.debug("Before %s", repr(prev_option))  # type: ignore[union-attr]
                    self._logger.debug("After %s", repr(options))  # type: ignore[union-attr]
                    if register_on_change:
                        self._logger.info("Registering command %s", options.name)  # type: ignore[union-attr]
                        (_, response) = self.call_api(  # type: ignore[misc]
                            method="PATCH",
                            path=f"/applications/{self.id}/commands/{prev_option.id}",
                            headers={"Content-Type": "application/json"},
                            json=asdict(options, dict_factory=asdict_ignore_none)
                        )
                        self._logger.info(f"Registration retruned with status code {response.status_code}")  # type: ignore[union-attr]
            return function
        return decorator

    def run(self, *args: Any, **kwargs: Any) -> None:
        """
            Starts web server for incoming requests.
        """
        return self._flask.run(*args, **kwargs)

    @classmethod
    def from_basic_data(
        cls,
        id: discord_types.Snowflake,
        public_key: str,
        bot_token: str,
        endpoint: str = "/"
    ) -> Self:  # type: ignore[valid-type]
        appinfo_response = requests.request(
            "GET",
            "https://discord.com/api/v8/oauth2/applications/@me",
            headers={
                "Authorization": f"Bot {bot_token}"
            }
        )
        appinfo_response.raise_for_status()
        app_obj = appinfo_response.json()
        if app_obj['id'] == id:
            return cls(
                _bot_token=bot_token,
                _public_key=public_key,
                _endpoint=endpoint,
                **app_obj
            )
        raise ValueError(f"Discord responded with different application ID \"{app_obj['id']}\". Expected: \"{id}\"")


PartialApplication = Application
