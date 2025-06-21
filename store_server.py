from concurrent import futures
import grpc
import store_service_pb2
import store_service_pb2_grpc
import sqlite3
import json

DB_FILE = 'store_results.db'

# Create tables if not exist
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT,
            features TEXT,
            predicted_label TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS regression (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT,
            features TEXT,
            predicted_value REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_classification(model_name, features, predicted_label):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO classification (model_name, features, predicted_label) VALUES (?, ?, ?)",
        (model_name, json.dumps(features), predicted_label)
    )
    conn.commit()
    conn.close()

def save_regression(model_name, features, predicted_value):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO regression (model_name, features, predicted_value) VALUES (?, ?, ?)",
        (model_name, json.dumps(features), predicted_value)
    )
    conn.commit()
    conn.close()

class StoreServiceServicer(store_service_pb2_grpc.StoreServiceServicer):
    def SaveRegress(self, request, context):
        print(f"[Regress] Model: {request.model_name}, Features: {request.features}, Prediction: {request.predicted_value}")
        save_regression(request.model_name, list(request.features), request.predicted_value)
        return store_service_pb2.SaveResponse(success=True, message="Regression result saved to DB.")

    def SaveClassify(self, request, context):
        print(f"[Classify] Model: {request.model_name}, Features: {request.features}, Label: {request.predicted_label}")
        save_classification(request.model_name, list(request.features), request.predicted_label)
        return store_service_pb2.SaveResponse(success=True, message="Classification result saved to DB.")

def serve():
    init_db()  # Initialize DB tables
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_service_pb2_grpc.add_StoreServiceServicer_to_server(StoreServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("🚀 gRPC StoreService running on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
