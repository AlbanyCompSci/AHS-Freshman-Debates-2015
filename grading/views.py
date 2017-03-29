from django.shortcuts import render
from django.views import generic
from group_manager import models as gModels
from itertools import groupby

# Create your views here.


class ScoreingSheetsView(generic.View):
    def get(self, request, *args, **kwargs):
        #data = []
        qs = gModels.Debate.objects.filter(isPresenting=True).select_related(
            "schedule__location", "schedule__topic",
            "group__teacher").order_by("schedule__date", "schedule__period",
                                       "schedule__location__location")
        """for i in range(qs.count() - 1):
            if qs[i] != qs[i + i]:
                continue
            g1 = qs[i].group.average()
            g2 = qs[i + 1].group.average()
            data.append({
                "date": qs[i].schedule.date.strftime("%A"),
                "period": qs[i].schedule.period,
                "location": qs[i].schedule.location.__str__(),
                "topic": qs[i].schedule.topic.__str__(),
                "winner": qs[i].group.__str__()
                if g1 > g2 else qs[i + 1].group.__str__(),
                "loser": qs[i + 1].group.__str__()
                if g1 > g2 else qs[i].group.__str__(),
                "winnerS": g1 if g1 > g2 else g2,
                "lowerS": g2 if g1 > g2 else g1
            })"""
        locations = sorted(
            list(set(i.schedule.location.location for i in qs)))
        """dates = [
            i.strftime("%A") for i in sorted({k.schedule.date
                                              for k in qs})
        ]
        return render(request, "grading/score_sheet_view.html",
                      {"qs": qs,
                       "locations": locations,
                       "dates": dates})"""
        data = dict()
        for i, sub in groupby(
                qs, key=(lambda x: x.schedule.date)):  # date split
            data[i.strftime("%A")] = list(sub)

        for key in data:  # split by period
            temp = data[key]
            data[key] = dict()
            for i, sub in groupby(temp, key=(lambda x: x.schedule.period)):
                data[key][i] = list(sub)
               
        for key in data:  # split by schedule
            for keyp in data[key]:
                temp = list(data[key][keyp])
                data[key][keyp] = []
                for i, sub in groupby(temp, key=(lambda x: x.schedule.pk)):
                    sub = list(sub)
                    """if len(sub) != 2:
                        raise Exception("Fuck group" + str(sub[0].group))
                    else:"""
                    g1 = sub[0].group
                    g2 = sub[1].group
                    s1 = g1.average()
                    s2 = g2.average()

                    data[key][keyp].append({
                        "winner": g1 if s1 > s2 else g2,
                        "loser": g2 if s1 > s2 else g1,
                        "winnerS": s1 if s1 > s2 else s2,
                        "loserS": s2 if s1 > s2 else s1,
                        "topic": sub[0].schedule.topic
                    })

        # kill me now
        # no fuck you don't give me syntax errors on my sucicide comments it's 3 AM fuck you

        return render(request, "grading/score_sheet.html",
                      {"datum": data,
                       "locations": locations})
