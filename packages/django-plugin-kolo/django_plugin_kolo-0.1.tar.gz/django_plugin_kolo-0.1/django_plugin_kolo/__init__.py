import djp


@djp.hookimpl
def middleware():
    return [djp.Before("kolo.middleware.KoloMiddleware")]
