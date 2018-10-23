from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client

class FDFSStorage(Storage):
    """fast dfs 文件存储类"""
    def __init__(self):
        """初始化"""
        self.client_conf = settings.FDFS_CLIENT_CONF
        self.base_url = settings.FDFS_URL

    def _open(self,name,mode='rb'):
        pass

    def _save(self,name,content):
        """保存文件时使用"""
        #name :上传文件的名字
        #content:包含你上传文件内容的File对象

        #创建一个Fifs_client对象
        client = Fdfs_client(self.client_conf)
        #上传文件到fast dfs系统中
        res = client.upload_by_buffer(content.read())

        print('res',res)

        if res.get('Status') != 'Upload successed.':
            #上传失败
            raise Exception('上传文件到FastDFS失败')
        #获取返回的文件 ID
        filename = res.get('Remote file_id').decode()
        return filename

    def exists(self, name):
        """判断文件名是否可用"""
        return False
    def url(self,name):
        """返回访问文件的url路径"""
        return self.base_url + name