import logging

from django.shortcuts import render

from AROM_Logic.Analysis import analyze
from .models import Result, Feedback

logging.basicConfig(level=logging.INFO)


def index(request):
    return render(request, "sentimentanalysis/index.html")


def get_pecentage(opinion_review_count, total_review_count):
    percentage = 0
    try:
        percentage = (opinion_review_count / total_review_count) * 100
    except:
        pass
    return round(percentage, 2)


def result(request):
    asin = request.POST.get("asin")
    flag = False
    try:
        result = Result.objects.filter(ASIN=asin)[0]
        if asin == result.ASIN:
            flag = True
    except:
        pass
    if flag:
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
        analysis = analyze(asin)
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


def feedback(request):
    message = ""
    try:
        f = Feedback(Name=request.POST.get("name"),
                     Email=request.POST.get("email"),
                     Message=request.POST.get("message"))
        f.save()
        message = "Thank you for your feedback " + str(request.POST.get("name"))
    except:
        pass
    return render(request, "sentimentanalysis/feedback.html", {"message": message})
