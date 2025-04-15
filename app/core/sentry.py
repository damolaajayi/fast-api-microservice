import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware


sentry_sdk.init(
    dsn="https://<your-public-key>@o0.ingest.sentry.io/<your-project-id>",
    traces_sample_rate=1.0,
    environment="production",
    release="fastapi-app@1.0.0",
)