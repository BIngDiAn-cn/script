#utf-8
import requests
import requests_html
import sys
import os
headers={
        'Host;': 'www.mosoteach.cn',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Sec-Fetch-Mode':'navigate',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;'
                  'q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'same-origin',
        'Referer': 'https://www.mosoteach.cn/web/index.php?c=res&m=index&clazz_course_id=5C2A872D-CCB4-11E9-9C7F-98039B1848C6',

}
data={
        'clazz_course_id':'5C2A872D-CCB4-11E9-9C7F-98039B1848C6',
        'res_id':'62F4028F-5BCD-4B8A-601A-EB0E3B8E66B8',
        'watch_to':'9999',
        'duration':'9999',
        'current_watch_to':'0'
}
def login(username,password):
        user_data={
                'account_name':username,
                'user_pwd':password,
                'remember_me':'N'
        }
        session=requests_html.HTMLSession()
        login_res=session.post("https://www.mosoteach.cn/web/index.php?c=passport&m=account_login",data=user_data)
        if(login_res.json()['result_code']==1007 or login_res.json()['result_code']==1001 ):

                return None
        else:
                return login_res.cookies

def watch(cookies):
        session = requests_html.HTMLSession()
        res = session.get(
                "https://www.mosoteach.cn/web/index.php?c=res&m=index&clazz_course_id=5C2A872D-CCB4-11E9-9C7F-98039B1848C6",
                headers=headers, cookies=cookies)
        list1 = res.html.find('div.res-row-open-enable')
        print(list1)
        for resource in list1:
                if (resource.attrs['data-mime'] == "video"):
                        data['res_id'] = resource.attrs['data-value']
                        watch_res = session.post('https://www.mosoteach.cn/web/index.php?c=res&m=save_watch_to',
                                                 data=data, headers=headers,cookies=cookies)
                        print(watch_res.text)
                else:
                        session.get(resource.attrs['data-href'], headers=headers,cookies=cookies)
if __name__=="__main__":
                if len(sys.argv)==3:
                        username=sys.argv[1]
                        password=sys.argv[2]
                        cookies_flag=login(username,password)
                        if(cookies_flag==None):
                                print("*[登录失败]用户名或密码错误")
                                sys.exit()
                        print("*[登录成功]开始执行")
                        watch(cookies_flag)
                else:
                        print('*[Usage]: python3 %s <username> <password>' % os.path.basename(sys.argv[0]))
                        sys.exit()




