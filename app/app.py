import uuid
import uvicorn

from fastapi import FastAPI, HTTPException
from mangum import Mangum

from app.routes import helloworld_router
from app.monitoring import logging_config
from app.middlewares.correlation_id_middleware import CorrelationIdMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from app.handlers.exception_handler import exception_handler
from app.handlers.http_exception_handler import http_exception_handler

###############################################################################
#   Application object                                                        #
###############################################################################

app = FastAPI()

###############################################################################
#   Logging configuration                                                     #
###############################################################################

logging_config.configure_logging(level='DEBUG', service='Helloworld', instance=str(uuid.uuid4()))

###############################################################################
#   Error handlers configuration                                              #
###############################################################################

app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

###############################################################################
#   Middlewares configuration                                                 #
###############################################################################

# Tip : middleware order : CorrelationIdMiddleware > LoggingMiddleware -> reverse order
app.add_middleware(LoggingMiddleware)
app.add_middleware(CorrelationIdMiddleware)

###############################################################################
#   Routers configuration                                                     #
###############################################################################

app.include_router(helloworld_router.router, prefix='/hello', tags=['hello'])

###############################################################################
#   Handler for AWS Lambda                                                    #
###############################################################################

handler = Mangum(app)

###############################################################################
#   Run the self contained application                                        #
###############################################################################

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)