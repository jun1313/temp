from bs4 import BeautifulSoup     
from selenium import webdriver
import time
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

path = "/Users/jun-mac/py_temp/chromedriver.exec"
driver = webdriver.Chrome(path)
driver.get("https://naver.com")

query_txt = input('1.크롤링할 키워드는 무엇입니까?(예:여행):')
txt_in = input('2.결과에서 반드시 포함할 단어를 입력하시오(예:가격,국내):')
txt_out = input('3.결과에서 제외할 단어를 선택하시오:(예:해외)')
start = input('4.조회 시작일자:')#뷰 이동후 조회?
end = input('4.조회 종료일자:')#뷰 이동후 조회?
nums = int(input('5.크롤링할 건수를 몇개 입니까?:'))
f_name = input('6.파일을 저장할 폴더명을 쓰시오(예:/Users/jun-mac/final/final2.txt):')
#검색
driver.find_element(By.ID,'query').click()
element =driver.find_element(By.ID,'query')
element.send_keys(query_txt)
#키워드 추가 제외
#element.send_keys(query_txt+' +'+txt_in+' -'+txt_out)
driver.find_element(By.CLASS_NAME, 'btn_search').click()
time.sleep(3)
driver.find_element(By.LINK_TEXT, 'VIEW').click()
time.sleep(10)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
#content_list = soup.find('ul',class_='lst_total _list_base')
root =driver.find_element(By.CLASS_NAME, '_list')
#print(root.text)
content_list=soup.find('ul', class_="lst_total")
contents=content_list.find_all('li', class_="bx _svp_item")

no = 1
num =[ ]
address=[ ]
nickname=[ ]
date=[]
texts=[]
count=0
#txt저장
orig_stdout = sys.stdout
f = open(f_name , 'a' , encoding='UTF-8')
sys.stdout = f
time.sleep(1)

#결과값 개수 카운트
for i in contents:
    count+=1
for i in contents:
    #번호
    num.append(no)
    print('총',count,'건 중',no,'번째 블로그 데이터를 수집합니다======')
    no += 1
    #주소
    address_temp=i.find('a','api_txt_lines')['href']
    address.append(address_temp)
    print('1.블로그 주소:',address_temp)
    #닉네임
    try:
        nickname_temp=i.find('span','source_txt name').get_text()
        nickname.append(nickname_temp)
        print('2.작성자 닉네임:',nickname_temp.strip())
    except:
        nickname_temp=i.find('a','sub_txt').get_text()
        nickname.append(nickname_temp)
        print('2.작성자 닉네임:',nickname_temp.strip())
    #작성일자
    try:
        date_temp=i.find('span','source_txt date').get_text()
        date.append(date_temp)
        print('3.작성 일자:',date_temp)
    except:
        date_temp=i.find('span','sub_time').get_text()
        date.append(date_temp)
        print('3.작성 일자:',date_temp)
    #블로그 내용
    texts_temp=i.find('div','api_txt_lines dsc_txt').get_text()
    texts.append(texts_temp)
    print('4.블로그 내용:',texts_temp)
    print('')
    if no==nums+1:
        break
        
sys.stdout = orig_stdout
f.close()

xls_temp = pd.DataFrame()

xls_temp['블로그주소']=address
xls_temp['닉네임']=nickname
xls_temp['작성일자']=date
xls_temp['블로그 내용']=texts

xls_temp.to_excel(f_name+'test.xls',index=False)
