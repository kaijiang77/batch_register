from pathlib import Path

class Settings():
    def __init__(self):
        #用户名称
        self.username = "example_"
        #账户密码
        self.password = "AbcdefG-12345"
        #邮箱地址
        self.email_address = "example"


        #网站注册地址及网站登录地址
        self.web_address = "https://search.asf.alaska.edu/"
        #注册邮箱网站地址
        self.email_web_address = 'https://www.snapmail.cc'
        #注册网站地址
        self.register_address = "https://urs.earthdata.nasa.gov/users/new"

        #更新序号区间
        self.update_index_range()

        #等待响应的时间
        self.wait_time = 15
    
    def update_index_range(self):
        #初始号码
        path = Path('index_recorder.txt')
        index = path.read_text()
        self.start_num = int(index)