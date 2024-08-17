from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import requests              
import time
from settings import Settings
import pandas as pd
from pathlib import Path
from tkinter import messagebox


class Batch_Register():

    def __init__(self) -> None:
        """初始化各种设置"""
        self.st = Settings()
    
    def run(self):
        """开始程序的主循环"""
        #用以储存数据
        df = pd.DataFrame(columns=['Username','Password','E_mail'])
        
        num = int(input("请输入需要创建用户的数量: "))

        if self.st.start_num + num > 100000:
            print('序号超出上限')
            return
        
        #利用try，expect方式，在程序中断时能够保持数据
        try:
            for i in range(self.st.start_num,self.st.start_num + num):
                #启动浏览器，如果未设置环境变量应设置路径
                driver = webdriver.Chrome()

                #获取带序号的用户名及邮箱地址
                username,email = self._get_inf(self.st.username,self.st.email_address,i)

                #注册网站进行注册
                self._register(username,self.st.password,email,driver)

                #检验是否需要人工验证注册
                self._check_register(driver)

                #进行邮箱确认
                self._email_confirm(email,driver)

                #登录网站并点击确认
                self._web_confirm(driver,username,self.st.password)

                #存储账号、密码及邮箱信息
                df = self._save_inf(username,self.st.password,email,df)

                #退出浏览器
                driver.quit()
        except:
            pass
        
        #将新得到的序号添加至序号区间的末尾
        self._save_index_range(len(df))

        #当数据存在时保存账号数据
        if len(df):
            df.to_csv(f"user_accounts{self.st.start_num}-{self.st.start_num + len(df) -1}.csv",index=False)

    def _get_inf(self,username,email,index):
        username = username + str(index).zfill(5)
        e_mail = email + str(index) + '@snapmail.cc'
        print(e_mail)
        return username,e_mail

    def _register(self,username,password,email,driver):
        """完成注册"""
        wait = WebDriverWait(driver,15)
        
        #在注册界面完成各项操作，注意无法通过人机验证，需人工完成
        driver.get(self.st.register_address)

        #输入用户名，密码，邮箱
        wait.until(EC.presence_of_element_located((By.ID,"user_uid"))).send_keys(username)
        driver.find_element(By.ID,"user_password").send_keys(password)
        driver.find_element(By.ID,"user_password_confirmation").send_keys(password)

        #输入姓、名
        driver.find_element(By.ID,"user_first_name").send_keys('jiang')
        driver.find_element(By.ID,"user_last_name").send_keys('kai')

        #输入电子邮箱
        driver.find_element(By.ID,"user_email_address").send_keys(email)

        #输入国家
        input_country = driver.find_element(By.ID,"user_country")
        input_country.find_element(By.XPATH,"//option[@value='China']").click()

        #输入隶属机构
        input_affiliation = driver.find_element(By.ID,"user_affiliation")
        input_affiliation.find_element(By.XPATH,"//option[@value='Education']").click()
        
        #输入研究领域
        input_study_area = driver.find_element(By.ID,"user_study_area")
        input_study_area.find_element(By.XPATH,"//option[@value='Land Processes']").click()

        #输入用户类别
        input_user_type = driver.find_element(By.ID,'user_user_type')
        input_user_type.find_element(By.XPATH,"//option[@value='Science Team']").click()

        #点击登录按钮
        driver.find_element(By.ID,'register_user').submit()

    def _check_register(self,driver):
        """查验登录页面是否存在人工检测"""
        wait = WebDriverWait(driver,15)

        try:
            wait.until(EC.presence_of_element_located((By.ID,"user_password"))).send_keys(self.st.password)
            driver.find_element(By.ID,"user_password_confirmation").send_keys(self.st.password)
            driver.find_element(By.ID,'register_user').location_once_scrolled_into_view

            #等待用户完成人工确认
            self._check_url_change(driver)

        except:
            pass
    
    def _email_confirm(self,email,driver):
        """返回注册邮箱中的确认链接"""
        
        #为使得邮箱有足够时间接收邮件，等待一段时间
        time.sleep(5)

        #获取最新得到的邮件一封,获取失败则重复获取，直至成功
        confirm_email_address = self.st.email_web_address + '/emailList/' + email + "?count=1"
        while True:
            req = requests.get(confirm_email_address)
            if req.status_code == 200:
                #读取邮件内容，为json格式
                email_text = json.loads(req.text)

                #从邮件中提取注册链接地址
                try:
                    soup = BeautifulSoup(email_text[0]['html'],'html.parser')

                #如果邮件内容不正确，则等待一段时间重新获取邮件
                except:
                    time.sleep(1)
                    continue

                #获取注册链接
                links = soup.find_all('a')
                link = links[2].get('href')
                driver.get(link)

                break

            else:
                print('再次获取邮件')
            
    def _web_confirm(self,driver,username,password):
        """在邮箱确认完成后，需要登录并完成确认"""
        wait = WebDriverWait(driver,15)

        #返回登录界面
        driver.back()

        #在登录界面输入用户名，密码完成登录
        wait.until(EC.presence_of_element_located((By.ID,'username'))).send_keys(username)
        driver.find_element(By.ID,'password').send_keys(password)
        driver.find_element(By.NAME,'commit').submit()

        #返回网站主页面，以便完成确认
        driver.get(self.st.web_address)

        #返回首页点击login
        wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/app-root/mat-sidenav-container/mat-sidenav-content/div/app-header/div/div/div[2]/app-dataset-header/div/div/div/app-header-buttons/div/mat-icon[5]"))).click()

        #对新弹出的确认界面进行确认操作
        driver.switch_to.window(driver.window_handles[-1])

        wait.until(EC.presence_of_element_located((By.ID,'agreement'))).click()
        
        element = driver.find_element(By.NAME,'authorize')
        ActionChains(driver).move_to_element(element).click().perform()
          
    def _save_inf(self,username,password,email,df):
        """保留本次注册所使用的用户名、密码、电子邮箱"""
        temp_df = pd.DataFrame({"Username":[username],"Password":[password],'E_mail':[email]})
        print(temp_df)
        df =  pd.concat([df.copy(),temp_df],ignore_index=True)
        return df

    def _save_index_range(self,len):
        #存储最新序号
        path = Path('index_recorder.txt')
        index = path.read_text()
        index = int(index) + len
        path.write_text(str(index))

    def _check_url_change(self,driver):
        """通过确认url是否发生改变的方式确认用户是否完成操作"""

        current_url = driver.current_url

        messagebox.showinfo('提示','请完成人工确认')

        while current_url == driver.current_url:
            #等待用户完成操作
            time.sleep(0.5)

if __name__ == "__main__":
    br = Batch_Register()
    br.run()

