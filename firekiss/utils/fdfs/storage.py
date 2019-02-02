from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client


class FDFSStorage(Storage):
    """自定义文件存储类"""
    def __init__(self, base_conf=None, base_url=None):
        if base_conf is None:
            # 默认配置文件
            self.base_conf = settings.HDFS_CLIENT_CONF
        if base_url is None:
            # 默认文件url
            self.base_url = settings.HDFS_URL

    def _open(self, name, mode='rb'):
        """用于打开文件"""
        pass

    def _save(self, name, content):
        """用于保存文件"""
        # 创建一个fdfs client连接对象
        client = Fdfs_client(self.base_conf)

        # content 返回一个file对象
        file_content = content.read()

        # 根据文件内容上传文件
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',
        #     'Local file name': '',
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # }
        res = client.upload_by_buffer(file_content)

        if res.get('Status') != 'Upload successed.':
            # 上传失败
            raise Exception('上传文件到fdfs失败')

        # 获取返回的文件id
        filename = res.get('Remote file_id')

        return filename

    def exists(self, name):
        """判断上传的文件是否为已存在文件的引用，存在返回True"""
        # 由于我们使用fdfs，因此重写父类方法直接返回False
        return False

    def url(self, name):
        """返回文件上传后所在的路径"""
        return self.base_url+name