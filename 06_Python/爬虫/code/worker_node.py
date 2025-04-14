# worker_node.py
import requests
import json

def collect_data():
    # 模拟采集数据
    data = {"temperature": 22.5, "humidity": 45}
    return data

def send_data_to_master(data, master_url):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(master_url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print("Data sent successfully")
        print(str(response.content, encoding = "utf-8"))
    else:
        print("Failed to send data")

if __name__ == '__main__':
    master_url = "http://172.26.120.56:5000/receive_data"
    data = collect_data()
    send_data_to_master(data, master_url)
