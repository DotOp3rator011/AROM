import logging
import re

from django.shortcuts import render

from AROM_Logic.Analysis import analyze
from .models import Result, Feedback

logging.basicConfig(level=logging.INFO)


def index_validate(asin):
    if len(asin) != 10 or asin == "":
        return False
    return True


def index(request):
    return render(request, "sentimentanalysis/index.html")


def index_error(request, error):
    return render(request, "sentimentanalysis/index.html", {"error": error})


def get_pecentage(opinion_review_count, total_review_count):
    percentage = 0
    try:
        percentage = (opinion_review_count / total_review_count) * 100
    except:
        pass
    return round(percentage, 2)


def result(request):
    asin = request.POST.get("asin")
    try:
        valid = index_validate(asin)
        if not valid:
            error = "* Enter a valid ASIN eg: B073QVY9PQ"
            return index_error(request, error)
    except Exception as e:
        print(e)
    result = None
    try:
        result = Result.objects.filter(ASIN=asin)[0]
    except:
        pass
    if result:
        logging.info("Existing record")
        negative_percentage = get_pecentage(result.negative_reviews_count, result.total_reviews_count)
        positive_percentage = get_pecentage(result.positive_reviews_count, result.total_reviews_count)
        analysis = {
            "ASIN": asin,
            "total_reviews_count": result.total_reviews_count,
            "negative_reviews_count": result.negative_reviews_count,
            "negative_percentage": negative_percentage,
            "positive_reviews_count": result.positive_reviews_count,
            "positive_percentage": positive_percentage
        }
    else:
        logging.info("New record")
        try:
            analysis = analyze(asin)
        except:
            error = "* Enter valid ASIN eg: B073QVY9PQ"
            return index_error(request, error)
        analysis["negative_percentage"] = get_pecentage(analysis["negative_reviews_count"],
                                                        analysis["total_reviews_count"])
        analysis["positive_percentage"] = get_pecentage(analysis["positive_reviews_count"],
                                                        analysis["total_reviews_count"])
        r = Result(ASIN=analysis["ASIN"],
                   total_reviews_count=analysis["total_reviews_count"],
                   negative_reviews_count=analysis["negative_reviews_count"],
                   positive_reviews_count=analysis["positive_reviews_count"])
        r.save()
    return render(request, "sentimentanalysis/result.html", analysis)


def aboutus(request):
    return render(request, "sentimentanalysis/aboutus.html", )


def contact_validate(request):
    name = request.POST.get("name").strip()
    email = request.POST.get("email").strip()
    flag = 0
    if name == "" or not re.match(r'^[A-Za-z]*$', name):
        flag += 1
    if not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', email):
        flag += 2
    if flag:
        return [False, flag]
    return [True, flag]


def contact(request):
    validation = {"greet": "We'd love to hear from you",
                  "name": "",
                  "email": "",
                  "Message": "",
                  "Name": "",
                  "Email": "",
                  }
    try:
        valid = contact_validate(request)
        if valid[0]:
            f = Feedback(Name=request.POST.get("name").strip(),
                         Email=request.POST.get("email").strip(),
                         Message=request.POST.get("message").strip())
            f.save()
            validation["greet"] = "Thank you for your feedback " + str(request.POST.get("name"))
        elif valid[1] == 3:
            validation["name"] = "* Enter a valid name eg: Jake"
            validation["email"] = "* Enter a valid email eg: Jake@ninenine.com"
        elif valid[1] == 2:
            validation["email"] = "* Enter a Valid Email"
            validation["Name"] = request.POST.get("name").strip()
        elif valid[1] == 1:
            validation["name"] = "* Enter a Valid Name"
            validation["Email"] = request.POST.get("email").strip()
        if request.POST.get("message"):
            validation["message"] = request.POST.get("message").strip()
    except:
        pass
    return render(request, "sentimentanalysis/contact.html", validation)
