import os



# class interFace():
#     # 获取目录地址
#     def get_path_dir(self):
#         path_dir = os.path.dirname(os.path.dirname(__file__)).replace('\\', '/')
#         return path_dir
#
#     # 接口地址
#     def get_interface_url(self):
#         interface_url = 'http://192.168.221.25:8380'
#         return interface_url
#
#     # 获取用户名密码
#     def get_user_pas(self):
#         # 用户名
#         username = 'admin'
#         # 密码
#         password = '1234'
#         data = {'username':username,'password':password}
#         return data

path_dir = os.path.dirname(os.path.dirname(__file__)).replace('\\', '/')

# swag的地址
interface_url = 'http://192.168.221.25:8380'



