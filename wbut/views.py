from django.shortcuts import render
from wbut.parser import parseIndexPage, parseResult, parseCollegeList, downloadResult
from django.shortcuts import redirect
from django.http import HttpResponse
from wbut.semesterYear import getSemYear
from wbut.models import Result, BasicDetails, College, SemesterOverview
import urllib3
from os import path
import logging

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)


def resultOverview(request):
    if request.method == "POST":
        try:
            roll_no = request.POST['usn']
            sem = request.POST['sem']
            result_overview = SemesterOverview.objects.filter(semester=sem).filter(basicDetails_id=roll_no)
            if result_overview.count() <= 0:
                cookie, token = parseIndexPage(roll_no, sem)
                parseResult(roll_no, sem, cookie, token)
            basic_details = BasicDetails.objects.get(roll_no=roll_no)
            results = SemesterOverview.objects.filter(basicDetails=basic_details).order_by('-semester')
            semesterYear = []
            year = int(roll_no[6:8])
            for result in results:
                semester = int(result.semester)
                semYear = getSemYear(year, semester)
                semesterYear.append(semYear)
            mylist = zip(results, semesterYear)
            mylist2 = zip(results, semesterYear)
            context = {"results": mylist, "details": basic_details, "semesters": semesterYear, "results2": mylist2}
            return render(request, "wbut/result_overview.html", context)
        except TimeoutError as e:
            logger.info("TimeOut Error has Ocuured")
            try:
                basic_details = BasicDetails.objects.get(roll_no=roll_no)
                results = SemesterOverview.objects.filter(basicDetails=basic_details).order_by('-semester')
                semesterYear = []
                year = int(roll_no[6:8])
                for result in results:
                    semester = int(result.semester)
                    semYear = getSemYear(year, semester)
                    semesterYear.append(semYear)
                mylist = zip(results, semesterYear)
                mylist2 = zip(results, semesterYear)
                context = {"results": mylist, "details": basic_details, "semesters": semesterYear, "results2": mylist2}
                return render(request, "wbut/result_overview.html", context)
            except:
                return render(request, "wbut/error.html")
        except Exception as ex:
            logger.error(ex)
            return render(request, "wbut/error.html")
    else:
        return redirect("wbut:home")


# This renders the first page of the website
def index(request):
    return render(request, "wbut/index.html")


def viewResult(request, roll_no, semester):
    result = Result.objects.filter(basicDetails_id=roll_no).filter(semester=semester)
    total_credits = 0
    total_credit_points = 0
    for eachResult in result:
        total_credits += eachResult.credit
        total_credit_points += eachResult.credit_points
    basic_details = BasicDetails.objects.get(roll_no=roll_no)
    overview = SemesterOverview.objects.filter(basicDetails_id=roll_no).get(semester=semester)
    context = {"results": result, "details": basic_details, "overview": overview,
               "total_credits": total_credits, "total_credit_points": total_credit_points}
    return render(request, "wbut/result_page.html", context)


def collegeList(request):
    # parseCollegeList()
    colleges = College.objects.all()
    coll = {"colleges": colleges}
    return render(request, "wbut/colleges.html", coll)


def viewClassRank(request, roll_no, semester):
    try:
        roll_no = roll_no[:-3]
        overview = SemesterOverview.objects.filter(basicDetails__roll_no__contains=roll_no).filter(
            semester=semester).order_by('-cgpa')
        for over in overview:
            print(over.basicDetails.name)
        context = {'results': overview, 'semester': semester}
        return render(request, "wbut/class_result.html", context)
    except Exception as e:
        logger.error(e)
        return render(request, "wbut/error.html")


def export(request,roll_no, semester):
    filename = roll_no + "-" + semester + ".pdf"
    cookie, token = parseIndexPage(roll_no, semester)
    f = downloadResult(roll_no, semester, cookie, token)
    response = HttpResponse(f.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    response['Content-Type'] = 'application/pdf; charset=utf-16'
    return response


def contactUs(request):
    return render(request,"wbut/contact-us.html")


def privacyPolicy(request):
    return render(request,"wbut/privacy-policy.html")


def aboutUs(request):
    return render(request,"wbut/about-us.html")

