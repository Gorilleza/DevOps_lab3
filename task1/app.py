from flask import Flask
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# 1. Настраиваем провайдер трассировки
provider = TracerProvider()
trace.set_tracer_provider(provider)

# 2. Настраиваем экспортер (отправляем в Jaeger по gRPC)
otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# 3. Инициализируем Flask и подключаем инструментацию
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route("/")
def hello():
    return "Hello, OpenTelemetry and Jaeger!\n"

@app.route("/health")
def health():
    return "OK\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)