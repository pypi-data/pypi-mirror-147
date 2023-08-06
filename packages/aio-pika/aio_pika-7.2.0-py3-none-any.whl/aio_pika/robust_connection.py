import asyncio
from logging import getLogger
from typing import Any, Callable, Dict, Optional, Type, Union
from warnings import warn
from weakref import WeakSet

import aiormq.abc
from aiormq.connection import parse_bool, parse_int
from pamqp.common import FieldTable
from yarl import URL

from .abc import (
    AbstractChannel, AbstractRobustChannel, AbstractRobustConnection,
    TimeoutType,
)
from .connection import Connection, make_url
from .exceptions import CONNECTION_EXCEPTIONS
from .robust_channel import RobustChannel
from .tools import CallbackCollection, task


log = getLogger(__name__)


class RobustConnection(Connection, AbstractRobustConnection):
    """ Robust connection """

    CHANNEL_REOPEN_PAUSE = 1
    CHANNEL_CLASS: Type[RobustChannel] = RobustChannel
    KWARGS_TYPES = (
        ("reconnect_interval", parse_int, "5"),
        ("fail_fast", parse_bool, "1"),
    )

    def __init__(
        self, url: URL, loop: asyncio.AbstractEventLoop = None, **kwargs: Any
    ):
        super().__init__(url=url, loop=loop, **kwargs)

        self.connect_kwargs: Dict[str, Any] = {}
        self.reconnect_interval = self.kwargs["reconnect_interval"]
        self.fail_fast = self.kwargs["fail_fast"]

        self.__channels: WeakSet[AbstractChannel] = WeakSet()
        self._connect_lock = asyncio.Lock()
        self._is_closed_by_user = False
        self.reconnect_callbacks: CallbackCollection = CallbackCollection(self)

    @property
    def reconnecting(self) -> bool:
        return self._connect_lock.locked()

    def __repr__(self) -> str:
        return '<{0}: "{1}" {2} channels>'.format(
            self.__class__.__name__, str(self), len(self.__channels),
        )

    def _on_connection_close(
        self, connection: aiormq.abc.AbstractConnection,
        closing: asyncio.Future,
    ) -> None:
        if self.reconnecting:
            return

        self.connected.clear()
        del self.connection

        log.debug("Closing AMQP connection %r", connection)

        if self.closing.done():
            return

        if connection.closing.exception() is None:
            self.closing.set_result(None)
            self.close_callbacks(None)
            return

        log.info(
            "Connection to %s closed. Reconnecting after %r seconds.",
            self, self.reconnect_interval,
        )
        self.loop.call_later(
            self.reconnect_interval,
            self.reconnect,
        )

    def add_reconnect_callback(
        self, callback: Callable[["RobustConnection"], None],
        weak: bool = False,
    ) -> None:
        """ Add callback which will be called after reconnect.

        :return: None
        """
        warn(
            "This method will be removed from future release. "
            f"Use {self.__class__.__name__}.reconnect_callbacks.add instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.reconnect_callbacks.add(callback, weak=weak)

    async def __cleanup_connection(self, exc: Optional[BaseException]) -> None:
        if not hasattr(self, "connection"):
            return

        await asyncio.gather(
            self.connection.close(exc), return_exceptions=True,
        )
        del self.connection

    async def connect(
        self, timeout: TimeoutType = None, **kwargs: Any
    ) -> None:
        if self.is_closed:
            raise RuntimeError("{!r} connection closed".format(self))

        if kwargs:
            # Store connect kwargs for reconnects
            self.connect_kwargs = kwargs

        if self.reconnecting:
            raise RuntimeError(
                (
                    f"Connect method called but connection "
                    f"{self!r} is reconnecting right now."
                ), self,
            )

        async with self._connect_lock:
            while not self.closing.done():
                try:
                    await super().connect(
                        timeout=timeout, **self.connect_kwargs
                    )

                    for channel in self.__channels:
                        await channel.reopen()

                    self.fail_fast = False
                except CONNECTION_EXCEPTIONS as e:
                    if self.fail_fast:
                        raise

                    await self.__cleanup_connection(e)

                    log.warning(
                        'Connection attempt to "%s" failed: %s. '
                        "Reconnecting after %r seconds.",
                        self,
                        e,
                        self.reconnect_interval,
                    )
                except asyncio.CancelledError as e:
                    await self.__cleanup_connection(e)
                    raise
                else:
                    self.connected.set()
                    return

                log.info(
                    "Reconnect attempt failed %s. Retrying after %r seconds.",
                    self, self.reconnect_interval,
                )
                await asyncio.sleep(self.reconnect_interval)

    @task
    async def reconnect(self) -> None:
        await self.connect()
        self.reconnect_callbacks(self)

    def channel(
        self,
        channel_number: int = None,
        publisher_confirms: bool = True,
        on_return_raises: bool = False,
    ) -> AbstractRobustChannel:

        channel: AbstractRobustChannel = super().channel(
            channel_number=channel_number,
            publisher_confirms=publisher_confirms,
            on_return_raises=on_return_raises,
        )   # type: ignore

        self.__channels.add(channel)
        self.close_callbacks.add(
            lambda c, e: channel.close_callbacks(e),
        )

        return channel

    @property
    def is_closed(self) -> bool:
        """ Is this connection is closed """
        return self._is_closed_by_user or super().is_closed

    async def close(
        self, exc: Optional[aiormq.abc.ExceptionType] = asyncio.CancelledError,
    ) -> None:
        if self.is_closed:
            return

        self._is_closed_by_user = True

        if not hasattr(self, "connection"):
            return

        result = await super().close(exc)
        self.close_callbacks(exc)
        return result


async def connect_robust(
    url: Union[str, URL] = None,
    *,
    host: str = "localhost",
    port: int = 5672,
    login: str = "guest",
    password: str = "guest",
    virtualhost: str = "/",
    ssl: bool = False,
    loop: asyncio.AbstractEventLoop = None,
    ssl_options: dict = None,
    timeout: TimeoutType = None,
    client_properties: FieldTable = None,
    connection_class: Type[AbstractRobustConnection] = RobustConnection,
    **kwargs: Any
) -> AbstractRobustConnection:

    """ Make connection to the broker.

    Example:

    .. code-block:: python

        import aio_pika

        async def main():
            connection = await aio_pika.connect(
                "amqp://guest:guest@127.0.0.1/"
            )

    Connect to localhost with default credentials:

    .. code-block:: python

        import aio_pika

        async def main():
            connection = await aio_pika.connect()

    .. note::

        The available keys for ssl_options parameter are:
            * cert_reqs
            * certfile
            * keyfile
            * ssl_version

        For an information on what the ssl_options can be set to reference the
        `official Python documentation`_ .

    Set connection name for RabbitMQ admin panel:

    .. code-block:: python

        read_connection = await connect(
            client_properties={
                'connection_name': 'Read connection'
            }
        )

        write_connection = await connect(
            client_properties={
                'connection_name': 'Write connection'
            }
        )

    .. note:

        ``client_properties`` argument requires ``aiormq>=2.9``

    URL string might be contain ssl parameters e.g.
    `amqps://user:pass@host//?ca_certs=ca.pem&certfile=crt.pem&keyfile=key.pem`

    :param client_properties: add custom client capability.
    :param url:
        RFC3986_ formatted broker address. When :class:`None`
        will be used keyword arguments.
    :param host: hostname of the broker
    :param port: broker port 5672 by default
    :param login: username string. `'guest'` by default.
    :param password: password string. `'guest'` by default.
    :param virtualhost: virtualhost parameter. `'/'` by default
    :param ssl: use SSL for connection. Should be used with addition kwargs.
    :param ssl_options: A dict of values for the SSL connection.
    :param timeout: connection timeout in seconds
    :param loop:
        Event loop (:func:`asyncio.get_event_loop()` when :class:`None`)
    :param connection_class: Factory of a new connection
    :param kwargs: addition parameters which will be passed to the connection.
    :return: :class:`aio_pika.connection.Connection`

    .. _RFC3986: https://goo.gl/MzgYAs
    .. _official Python documentation: https://goo.gl/pty9xA


    """

    connection: AbstractRobustConnection = connection_class(
        make_url(
            url,
            host=host,
            port=port,
            login=login,
            password=password,
            virtualhost=virtualhost,
            ssl=ssl,
            ssl_options=ssl_options,
            **kwargs
        ),
        loop=loop,
    )

    await connection.connect(
        timeout=timeout,
        client_properties=client_properties,
        loop=loop,
    )

    return connection


__all__ = (
    "RobustConnection",
    "connect_robust",
)
