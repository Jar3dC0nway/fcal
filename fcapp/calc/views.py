from django.shortcuts import render

from django.http import HttpResponse

from .forms import CalculatorForm
import math


def set_blank_zero(request):
    vals = {'number', 'rate', 'present_value', 'payments', 'future_value', 'operation'}
    for v in vals:
        if request[v] == '':
            request[v] = 0
    return request


def index(request):
    vals = ['', '', '', '', '']
    if request.method == 'GET':
        form = CalculatorForm(set_blank_zero(request.GET.copy()))
        if form.is_valid():
            n = form.cleaned_data['number']
            r = form.cleaned_data['rate']
            p = form.cleaned_data['present_value']
            m = form.cleaned_data['payments']
            f = form.cleaned_data['future_value']
            o = form.cleaned_data['operation']

            if r == 0:  # Anti-/0
                r = 0.00000000001
            if m == 0:
                m = 0.00000000001
            if p == 0:
                p = 0.00000000001
            if f == 0:
                f = 0.00000000001
            if n == 0:
                n = 0.00000000001

            if o == 0:  # Number of payments
                try:
                    vals[0] = round(math.log((f * r - m) / (p * r - m), 1 + r), 1)
                except:
                    pass
            elif o == 1:  # Rate (Note, this is mathematically impossible to directly solve, so it's approximated)
                found = False
                counter = 0
                r = 0.000001
                while not found:
                    try:
                        if p != 0:  # Try present value
                            if abs(((f + (m * (((1 + r) ** n) - 1) / r)) / ((1 + r) ** n) - p) / p) < 0.0001:
                                found = True
                        elif f != 0:  # Try future value
                            if abs((p * ((1 + r) ** n) - (m * (((1 + r) ** n) - 1) / r) - f) / f) < 0.0001:
                                found = True
                        elif m != 0:  # Try payments
                            if abs(((p * ((1 + r) ** n) - f) * (r / ((1 + r) ** n - 1)) - m) / m) < 0.0001:
                                found = True
                                # Try number of payments
                        elif abs((math.log((f * r - m) / (p * r - m), 1 + r) - n) / n) < 0.0001:
                            found = True
                    except:
                        pass
                    if found:
                        r = round(r, 4)
                        break
                    r += 0.000001
                    counter += 1
                    if r > 1:
                        r = ''
                        print(counter)
                        found = True
                vals[1] = r
            elif o == 2:  # Present Value
                try:
                    vals[2] = round((f + (m * (((1 + r) ** n) - 1) / r)) / ((1 + r) ** n), 2)
                except:
                    pass
            elif o == 3:  # Payment
                try:
                    vals[3] = round((p * ((1 + r) ** n) - f) * (r / ((1 + r) ** n - 1)), 2)
                except:
                    vals[3] = 0.0
            elif o == 4:  # Future Value
                try:
                    vals[4] = round(p * ((1 + r) ** n) - (m * (((1 + r) ** n) - 1) / r), 2)
                except:
                    pass
            print(vals)

    return render(request, "index.html", {'vals': vals})
