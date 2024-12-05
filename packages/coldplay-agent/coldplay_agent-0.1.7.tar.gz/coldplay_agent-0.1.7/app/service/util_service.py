import configparser
import os
from typing import List, Optional
import requests
from smb.SMBConnection import SMBConnection
import torch
import torch.onnx

# 从环境变量中读取 SMB 服务器配置信息
SERVER_NAME = os.getenv("SMB_SERVER_NAME")
SHARE_NAME = os.getenv("SMB_SHARE_NAME")
USERNAME = os.getenv("SMB_USERNAME")
PASSWORD = os.getenv("SMB_PASSWORD")
 
class UtilService:
    def load_coldplay_config():
        config_dest = os.path.expanduser('~/.coldplay_config.ini')
        
        if not os.path.exists(config_dest):
            print("Config file not found. Please run coldplayagent-init first.")
            return None
        
        coldplay_config = configparser.ConfigParser()
        coldplay_config.read(config_dest)
        return coldplay_config
    

    # 从环境变量中读取 SMB 服务器配置信息
    SERVER_NAME = "192.168.2.66"
    SHARE_NAME = "software"
    USERNAME = "jenkins"
    PASSWORD = "jenkins#123"

    def list_files(directory_path: str) -> List[str]:
        conn=SMBConnection(USERNAME,PASSWORD,"","",use_ntlm_v2 = True, is_direct_tcp=True)
        result = conn.connect(SERVER_NAME, 445, timeout=60*10) #smb协议默认端口445
        print(f"连接smb成功 {result}")
        files = conn.listPath(SHARE_NAME, f"/{directory_path}")
        file_list = [file.filename for file in files if file.filename not in [".", ".."]]
        
        return file_list

    def download_file(remote_path, local_path):
        conn=SMBConnection(USERNAME,PASSWORD,"","",use_ntlm_v2 = True, is_direct_tcp=True)
        result = conn.connect(SERVER_NAME, 445, timeout=60*10) #smb协议默认端口445
        print(f"连接smb成功 {result}")
        """下载文件"""
        
        with open(local_path, 'wb') as f:
            conn.retrieveFile(SHARE_NAME, remote_path, f)

        conn.close()

        return local_path
    
    def export_policy_as_onnx(model_path, onnx_model_path):
        try:
            # 1. 加载 PyTorch 模型
            # model_path = "your_model.pt"  # 替换为你的模型路径
            # model = torch.load(model_path)
            # loaded_dict = torch.load(model_path)
            model = torch.load(model_path, map_location=torch.device('cpu'))
            # state_dict = torch.load("your_model.pt", map_location=torch.device('cpu'))
            # model.load_state_dict(state_dict)  # 加载参数
            model.eval()  # 切换到评估模式

            # 2. 定义输入张量
            # 假设模型输入是一个形状为 (batch_size, channels, height, width) 的张量
            dummy_input = torch.randn(0, 0, 0, 0)  # 根据实际情况修改

            # 3. 导出为 ONNX 格式
            input_names = ["nn_input"]
            output_names = ["nn_output"]
            # onnx_model_path = "your_model.onnx"
            torch.onnx.export(
                model,                  # 要导出的模型
                dummy_input,            # 模拟输入张量
                onnx_model_path,        # 导出文件名
                verbose=True,
                input_names=input_names,  # 输入节点名称
                output_names=output_names,  # 输出节点名称
                export_params=True,     # 导出模型参数
                opset_version=13,       # ONNX opset 版本 (一般为 11 或更高)
            )
        
        except Exception as e:
            print(f"模型转化失败: {e}")

        print("Exported policy as onnx script to: ", onnx_model_path)

    def download_http_file(file_url, local_file_path):
        # MinIO 文件的完整下载地址
        # file_url = "http://your-minio-server.com/your-bucket-name/path/to/file.txt"

        # 本地保存路径
        # local_file_path = "downloads/file.txt"

        # 确保本地目录存在
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        # 下载文件
        try:
            response = requests.get(file_url, stream=True)
            response.raise_for_status()  # 检查是否有 HTTP 错误

            with open(local_file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"文件已保存到本地：{local_file_path}")
        except requests.RequestException as e:
            print(f"下载失败：{e}")
            
