import unittest
import json
#
# class Test(unittest.TestCase):
#     def test_1(self):
#         for i in range(0,10):
#             if i == 1:
#                 self.assertEqual(i,1)
#                 a = 1
#                 break
#             else:
#                 pass
#         if a != 1:
#             self.assertEqual(3,4)
#         print("test_case_start")
#
# # st = unittest.TestSuite()
# # st.addTest(Test('test_1'))
# # runner.run(st)
# if __name__ == '__main__':
#     unittest.main()

fp = open('a.txt','w',encoding='utf8')
fp.write(json.dumps({'1':'成功','2':'失败'},ensure_ascii=False))
fp.close()