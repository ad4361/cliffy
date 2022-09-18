from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc

stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

from clarifai_IGNORE import clarifai_key

YOUR_CLARIFAI_API_KEY = clarifai_key
YOUR_APPLICATION_ID = "my-first-application"
SAMPLE_URL = "https://upload.wikimedia.org/wikipedia/commons/b/bb/Table_grapes_on_white.jpg"

# This is how you authenticate.
metadata = (("authorization", f"Key {YOUR_CLARIFAI_API_KEY}"),)

request = service_pb2.PostModelOutputsRequest(
    # This is the model ID of a publicly available General model. You may use any other public or custom model ID.
    model_id="general-image-recognition",
    user_app_id=resources_pb2.UserAppIDSet(app_id=YOUR_APPLICATION_ID),
    inputs=[
        resources_pb2.Input(
            data=resources_pb2.Data(image=resources_pb2.Image(url=SAMPLE_URL))
        )
    ],
)
response = stub.PostModelOutputs(request, metadata=metadata)

if response.status.code != status_code_pb2.SUCCESS:
    print(response)
    raise Exception(f"Request failed, status code: {response.status}")

for concept in response.outputs[0].data.concepts:
    print(concept.name, concept.value)
    # ex: juicy     0.9959744811058044
    #     grape     0.9918423891067505      
    #     vine      0.9835936427116394       
    #     food      0.9823979735374451