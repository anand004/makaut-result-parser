import requests
import urllib3
from tabulate import tabulate
from bs4 import BeautifulSoup
from wbut.models import Result, BasicDetails, College, SemesterOverview
import time
import urllib3
from io import BytesIO
import logging

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)

# This Function downloads the result from makaut website
def downloadResult(usn,sem,cookie,token):
    headers = {
        'Host': 'makaut1.ucanapply.com',
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Content-Length": "112",
        "Sec-Fetch-Dest": "document",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Sec-Fetch-Dest": "document",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Origin": "https://makaut1.ucanapply.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Referer": "https://makaut1.ucanapply.com/smartexam/public/result-details",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cookie": cookie
    }
    url = "https://makaut1.ucanapply.com/smartexam/public/download-pdf-result"
    semester = "SM0" + sem
    downloadData = {
        "_token": token,
        "ROLLNO": usn,
        "SEMCODE": semester,
        "examtype": "result-details",
        "downloadFileName": usn + "_marksheet"
    }
    r = requests.post(url, data=downloadData, headers=headers, verify=False)
    f = BytesIO(r.content)
    return f
    # filename = usn+"-"+sem+".pdf"
    # filepath = "wbut/static/pdf/"
    # file = open(filepath+filename, "wb")
    # file.write(r.content)
    # file.close()


def parseResult(usn, sem, cookie, token):
    headers = {
        'Host': 'makaut1.ucanapply.com',
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Content-Length": "112",
        "X-CSRF-TOKEN": token,
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Sec-Fetch-Dest": "document",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Origin": "https://makaut1.ucanapply.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Referer": "https://makaut1.ucanapply.com/smartexam/public/result-details",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cookie": cookie
    }
    semester = "SM0" + sem
    data = {
        "_token": token,
        "ROLLNO": usn,
        "SEMCODE": semester,
        "examtype": "result-details"
    }

    url = "https://makaut1.ucanapply.com/smartexam/public//get-result-details"
    r = requests.post(url, data=data, headers=headers, verify=False)

    try:
        data = r.json()["html"]
        soup = BeautifulSoup(data, 'html5lib')
        table = soup.findAll('table')
        result = table[3]
        basicdetails = table[1]
        detailsrow = basicdetails.findAll("tr")
        basic_details = detailsrow[1].findAll('td')
        name = basic_details[0].find('span').get_text()
        roll_no = basic_details[1].find('span').get_text()
        reg_no = detailsrow[2].find('td').find('span').get_text()
        result_details_table = table[5]
        if int(sem) % 2 == 0:
            sgpa = result_details_table.findAll('tr')[1].find('td').find('strong').get_text()
            sgpa = sgpa[-6:]
            ygpa = result_details_table.findAll('tr')[2].find('td').find('strong').get_text()
            ygpa = ygpa[-4:]
            college_name = result_details_table.findAll('tr')[4].find('td').get_text()
            college_name = college_name[24:]
            status = result_details_table.findAll('tr')[3].find('td').get_text()
            status = status[-1:]
        else:
            sgpa = result_details_table.findAll('tr')[0].find('td').find('strong').get_text()
            sgpa = sgpa[-4:]
            ygpa = ""
            college_name = result_details_table.findAll('tr')[4].find('td').get_text()
            college_name = college_name[24:]
            status = result_details_table.findAll('tr')[3].find('td').get_text()
            status = status[-1:]

        # print(basic_details)
        get_details = BasicDetails.objects.filter(roll_no=roll_no)
        if get_details.count() <= 0:
            details_to_save = BasicDetails(name=name, reg_no=reg_no, roll_no=roll_no, college=college_name)
            details_to_save.save()
            semester_overview = SemesterOverview(basicDetails=details_to_save, semester=sem, ygpa=ygpa, cgpa=sgpa, status=status)
            semester_overview.save()
        else:
            get_details = get_details.first()
            semester_overview = SemesterOverview(basicDetails=get_details, semester=sem, ygpa=ygpa, cgpa=sgpa, status=status)
            semester_overview.save()
        rows = result.findAll("tr")
        get_details = BasicDetails.objects.filter(roll_no=roll_no).first()
        for i in range(1,len(rows)-1):
            cell = rows[i].findAll('td')
            subject_code = cell[0].get_text()
            subject_name = cell[1].get_text()
            letter_grade = cell[2].get_text()
            points = cell[3].get_text()
            credit = cell[4].get_text()
            credit_points = cell[5].get_text()
            result_to_save = Result(basicDetails = get_details,subject_code=subject_code, subject_name=subject_name,letter_grade=letter_grade,points=points,credit=credit,credit_points=credit_points,semester=semester_overview.semester)
            result_to_save.save()
    except Exception as ex:
        print(ex)


def parseIndexPage(usn, sem):
    try:
        url = "https://makaut1.ucanapply.com/smartexam/public/result-details"
        r = requests.get(url, verify=False, timeout=2)
        cookie = r.headers.get("Set-Cookie").split(";")
        xsrf_token = cookie[0]
        makaut_cookie = cookie[4][9:]
        cookie = xsrf_token + ";" + makaut_cookie
        soup = BeautifulSoup(r.content, 'html5lib')
        token = soup.find('input', {'name': '_token'}).get('value')
        return cookie, token
    except Exception:
        logger.info(TimeoutError)
        raise TimeoutError


def parseCollegeList():
    url = "https://makautwb.ac.in/page.php?id=363"
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.findAll('table')
    collegeList = table[-1].findAll('tr')
    for i in range(1, len(collegeList)):
        collegeDetails = collegeList[i].findAll('td')
        collegeName = collegeDetails[2].get_text().replace('\n', '').replace('\t', '')
        collegeCode = collegeDetails[1].get_text().replace('\n', '').replace('\t', '')
        data = College(collegeCode=int(collegeCode), collegeName=collegeName)
        data.save()

