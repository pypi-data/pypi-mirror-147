__version__ = "0.1.0"
from bottle import request, HTTPResponse, Bottle, Route

from tinyrpc.dispatch import RPCDispatcher
from tinyrpc.protocols import RPCProtocol
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
import tinyrpc
import logging

from typing import Callable, Optional, TypeVar

T = TypeVar("T")


bottle_tinyrpc_logger = logging.getLogger(__name__)


class TinyRPCPlugin(object):
    name = "tinyrpc"
    api = 2

    def __init__(self, sub_url: str, protocol: Optional[RPCProtocol] = None, dispatcher: Optional[RPCDispatcher] = None,
                 mimetype: str = "application/json", prehandler: Optional[Callable] = None, allow_origin: str = "*",
                 rpc_route_name: Optional[str] = None):
        """
        Instantiate a new TinyRPC endpoint for your Bottle application,
        as a plugin.

        :param sub_url: The sub-URL to serve the RPC from.
        :param protocol: The TinyRPC protocol to use. Default is JSON-RPC v2.
        :param dispatcher: The TinyRPC dispatcher to use. By default, a new
           dispatcher will be created.
        :param mimetype: The mimetype of the incoming and out going data
           from the endpoint. By default this is "application/json"; if
           a different TinyRPC protocol is used, the mimetype should be
           adjusted accordingly.
        :param prehandler: An arity 0 function that is invoked before
           any RPC calls are handled. If the function returns anything
           that is True-ish (like an HTTPResponse), it is returned
           instead of the RPC call being run. One major use for this
           would be to implement authentication of the endpoint
           (by checking user credentials before executing the
            method, and returning an approriate error if auth fails).
        :param allow_origin: The "Access-Control-Allow-Origin" header
            value. Default is '*'.
        :param rpc_route_name: The route name for the Bottle application
            for this RPC route.
        """
        self.sub_url = sub_url
        self.protocol = protocol or JSONRPCProtocol()
        self.dispatcher = dispatcher or RPCDispatcher()
        self.mimetype = mimetype
        self.prehandler = prehandler
        self.allow_origin = allow_origin
        self.rpc_route_name = rpc_route_name
        self.app = None

    def setup(self, app: Bottle):
        self.app = app

        access_control_headers = {
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Origin': self.allow_origin,
            'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With, Accept, Origin'
        }

        @app.route(self.sub_url, method=["OPTIONS"])
        def rpc_options_handler():
            return HTTPResponse(
                body=b"",
                headers=access_control_headers
            )

        @app.post(self.sub_url, name=self.rpc_route_name)
        def rpc_handler():
            if self.prehandler:
                prehandler_result = self.prehandler()
                if prehandler_result:
                    return prehandler_result
            try:
                payload = request.body.read()
                rpc_request = self.protocol.parse_request(payload)
            except tinyrpc.exc.RPCError as e:
                response = e.error_respond()
            else:
                response = self.dispatcher.dispatch(
                    rpc_request, getattr(self.protocol, '_caller', None)
                )
            headers = {
                "Content-Type": self.mimetype,
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }
            headers.update(access_control_headers)
            return HTTPResponse(
                body=response.serialize(),
                headers=headers
            )

    def apply(self, callback: Callable[..., T], route: Route) -> Callable[..., T]:
        return callback

    def public(self, name: Optional[str] = None):
        """
        Convenience method wrapped from the TinyRPC dispatcher's
        public method. This should be used as a decorator.

        :param name: The name to register the callable with.
        """
        return self.dispatcher.public(name=name)

    def add_subdispatch(self, dispatcher: RPCDispatcher, prefix: str = ''):
        """
        Wraps TinyRPC RPCDispatcher add_subdispatch method.
        """
        return self.dispatcher.add_subdispatch(dispatcher, prefix=prefix)

    def add_method(self, f: Callable, name: str) -> None:
        """
        Wraps the TinyRPC RPCDispatcher add_method method.
        """
        return self.dispatcher.add_method(f, name=name)

    def get_method(self, name: str) -> Callable:
        """
        Wraps the TinyRPC RPCDispatcher get_method method.
        """
        return self.dispatcher.get_method(name)

    def register_instance(self, obj: object, prefix: str = '') -> None:
        """
        Wraps the TinyRPC RPCDispatcher register_instance method.
        """
        return self.dispatcher.register_instance(obj, prefix=prefix)

