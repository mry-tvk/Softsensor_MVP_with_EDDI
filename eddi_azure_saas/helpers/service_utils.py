import requests
import json
from pprint import pprint
import time

class RestEDDI:
    def __init__(self, subscription_key, endpoint="https://ms-azua-api.azurewebsites.net", api_version="v2.3"):
        self.endpoint = endpoint
        self.api_version = api_version
        self.headers = {"api-key": subscription_key}

        self.exec_op_url_format = endpoint + "/saas-api/{operation_name}?api-version=" + api_version
        self.get_op_url_format = endpoint + "/saas-api/operations/{operation_name}/{operation_id}?api-version=" + api_version
        self.get_output_url_format = endpoint + "/saas-api/{output_name}/{output_id}?api-version=" + api_version
        self.exec_successor_op_url_format = endpoint + "/saas-api/{output_name}/{output_id}/{operation_name}?api-version=" + api_version        

    def get_request(self, url, headers):
        response = requests.get(url, headers=headers)
        return response.json()

    def post_request(self, url, headers, data):
        response = requests.post(url, headers=headers, json=data)
        print(response)

        if response.status_code == 200:
            operation_id = response.json()["operationId"]
            
        print(response.status_code)
        pprint(operation_id)
        return operation_id

    def wait_for_operation_to_complete(self, operation_id, operation_name="train"):
        url = self.get_op_url_format.format(operation_name=operation_name, operation_id=operation_id)
        start = time.time()
        while True:
            response = requests.get(url, headers=self.headers)
            # print(response.json())
            try:
                if response.status_code == 200:
                    if response.json()["status"] == "Completed" or  response.json()["status"] == "Failed":
                        print("Operation status: " + response.json()["status"])
                        print(operation_name + " running time: " + str(time.time() - start) + " seconds")
                        return response.json()["status"]
                    # else if response.json()["status"] == "Running":
                    time.sleep(10)
            except:
                print(operation_name + " running time: " + str(time.time() - start) + " seconds")

    def get_model_url(self, model_id):
        model_url = self.get_output_url_format.format(output_name="models", output_id=model_id)
        response = self.get_request(model_url, self.headers)
        pprint(response)
        return model_url

    def get_train_url(self):
        return  self.endpoint + "/saas-api/train?api-version=" + self.api_version
    
    def get_batch_inference_url(self, model_id):
        batch_inference_url = self.exec_successor_op_url_format.format(output_name = "models", output_id = model_id, operation_name = "batchinference")
        return batch_inference_url
    
    def get_deployment_url(self, model_id):
        deployment_url = self.exec_successor_op_url_format.format(output_name = "models", output_id = model_id, operation_name = "deploy")
        return deployment_url

    def get_endpoint_url(self, provisioned_endpoint_id):
        endpoint_url = self.get_output_url_format.format(output_name="endpoints", output_id=provisioned_endpoint_id)

        response = requests.get(endpoint_url, headers = self.headers)
        if response.status_code == 200:
            scoring_url = response.json()["scoring_uri"]
            primary_key = response.json()["primary_key"]
        pprint(scoring_url)
        return scoring_url, primary_key

    def train_model(self, train_input):
        url = self.get_train_url()
        operation_id = self.post_request(url, self.headers, train_input)
        return operation_id

    def batch_inference(self, model_id, batch_inference_input):
        url = self.get_batch_inference_url(model_id)
        operation_id = self.post_request(url, self.headers, batch_inference_input)
        return operation_id

    def deploy_model(self, model_id, deployment_input):
        url = self.get_deployment_url(model_id)
        operation_id = self.post_request(url, self.headers, deployment_input)
        return url, operation_id


def train_eddi(train_input, rest_api, wait_for_completion=True):
    # train model
    operation_id = rest_api.train_model(train_input)
    if wait_for_completion:
        status = rest_api.wait_for_operation_to_complete(operation_id, operation_name="train")
        if status == "Completed":
            model_id = operation_id
            model_url = rest_api.get_model_url(model_id)
            print(model_url)
    return operation_id

def batchinference_eddi(inference_input, model_id, rest_api, wait_for_completion=True):
    operation_id = rest_api.batch_inference(model_id, inference_input)
    if wait_for_completion:
        status = rest_api.wait_for_operation_to_complete(operation_id, operation_name="batchinference")
        print(status)
        # if status == "Completed":
        #     return operation_id
    return operation_id
    
def deploy_eddi(dns_name_label, model_id, rest_api, wait_for_completion=True):
    # deployment_input = {"dns_name_label":"unique-name"}
    deployment_input = {"dns_name_label":dns_name_label}
    url, deploy_operation_id = rest_api.deploy_model(model_id, deployment_input)
    scoring_url, primary_key = rest_api.get_endpoint_url(provisioned_endpoint_id=deploy_operation_id)

    if wait_for_completion:
        status = rest_api.wait_for_operation_to_complete(deploy_operation_id, operation_name="deploy")
        print(status)
        # if status == "Completed":
        #     scoring_url, primary_key = rest_api.get_endpoint_url(provisioned_endpoint_id=deploy_operation_id)
        #     return deploy_operation_id, scoring_url, primary_key
    return deploy_operation_id, scoring_url, primary_key