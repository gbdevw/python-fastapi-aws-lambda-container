import uuid

from starlette.middleware.base import BaseHTTPMiddleware

class CorrelationIdMiddleware (BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)

    # Add or use the provided correlation ID (request header : x-correlation-id)
    async def dispatch (self, request, call_next):

        # Add or reuse correlation id
        request.state.correlation_id = request.headers.get("x-correlation-id", str(uuid.uuid4()))

        # Next middleware
        response = await call_next(request)

        # Add correlation id header to response
        response.headers["x-correlation-id"] = request.state.correlation_id

        # Return response
        return response