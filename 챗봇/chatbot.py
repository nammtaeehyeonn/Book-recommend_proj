import os
from chatbot_dic import make_reply

##########################################
# 챗봇 기능
##########################################

os.system('clear')
q = 1
print('대화를 끝내려면 ctrl + c 키를 누르세요\n')
while q != 0:
    user = input('>>> ')
    if user == '': continue
    res = make_reply(user)
    print('{:>200}'.format('<<< 챗봇'))
    print(res.rjust(20))
    print()
