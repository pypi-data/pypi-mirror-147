import inspect
import logging

from nameko_tracer.adapters import DefaultAdapter as TracerDefaultAdapter, HttpRequestHandlerAdapter as TracerHttpRequestHandlerAdapter

from nameko_tracer import utils

logger = logging.getLogger(__name__)


class DefaultAdapter(TracerDefaultAdapter):

    def get_call_args(self, worker_ctx):
        """ Return serialisable call arguments
        """

        entrypoint = worker_ctx.entrypoint

        # TODO: Redacted args are bypassed - nameko.utils should be fixed
        #  to use inspect.signature instead of inspect.getcallargs
        redacted = False

        method = getattr(entrypoint.container.service_cls, entrypoint.method_name)
        call_args = inspect.signature(method).bind(None, *worker_ctx.args, **worker_ctx.kwargs).arguments

        del call_args['self']

        return call_args, redacted


class HttpRequestHandlerAdapter(TracerHttpRequestHandlerAdapter):

    def get_call_args(self, worker_ctx):
        """ Transform request object to serialized dictionary
        """

        entrypoint = worker_ctx.entrypoint

        method = getattr(entrypoint.container.service_cls, entrypoint.method_name)
        call_args = inspect.signature(method).bind(None, *worker_ctx.args, **worker_ctx.kwargs).arguments

        del call_args['self']

        request = call_args.pop(next(iter(call_args)))  # Assumes that the first key in `call_args` is always `request`
        data = request.data or request.form
        call_args['request'] = {
            'url': request.url,
            'method': request.method,
            'data': utils.safe_for_serialisation(data),
            'headers': dict(self.get_headers(request.environ)),
            'env': dict(self.get_environ(request.environ)),
        }

        return call_args, False
