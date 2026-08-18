from flask import Flask, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUEST_COUNT = Counter('order_service_requests_total', 'Total requests', ['endpoint'])
REQUEST_LATENCY = Histogram('order_service_request_latency_seconds', 'Request latency', ['endpoint'])

@app.route('/')
def home():
    start = time.time()
    REQUEST_COUNT.labels(endpoint='/').inc()
    response = {"message": "Order Service Running", "version": "1.0"}
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start)
    return response

@app.route('/health')
def health():
    REQUEST_COUNT.labels(endpoint='/health').inc()
    return {"status": "healthy"}

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
