import grpc
import store_service_pb2
import store_service_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = store_service_pb2_grpc.StoreServiceStub(channel)

    # Test SaveRegress
    response = stub.SaveRegress(store_service_pb2.RegressRequest(
        model_name="iris_regression_model",
        features=[5.1, 3.5, 1.4],
        predicted_value=0.2095
    ))
    print("Regress response:", response.message)

    # Test SaveClassify
    response = stub.SaveClassify(store_service_pb2.ClassifyRequest(
        model_name="iris_classifier_model",
        features=[5.1, 3.5, 1.4, 0.2],
        predicted_label="setosa"
    ))
    print("Classify response:", response.message)

if __name__ == '__main__':
    run()
