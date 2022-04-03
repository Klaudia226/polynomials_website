from flask import Flask, render_template, request

import base64
from io import BytesIO
import matplotlib.pyplot as plt
from sympy import parse_expr, lambdify, Symbol
import numpy as np

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("main.html")


@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/test/wyniki", methods=["POST", "GET"])
def wyniki():
    correct_answers = ["C", "B", "A", "A", "D"]
    user_answers = []
    points = 0
    for i in range(len(correct_answers)):
        user_answers.append(request.form.get('answer' + str(i+1)))
        if correct_answers[i] == user_answers[i]:
            points += 1
    return render_template("wyniki.html", correct_answers=correct_answers, user_answers=user_answers, points=points)


@app.route("/zadanka")
def przyklady():
    return render_template("zadanka.html")


@app.route("/autorzy")
def autorzy():
    return render_template("authors.html")

#wykresy

def formula_list(text):
    '''
    Create list of string formulas
    :return: (list) list with string formulas
    '''
    return text.split("; ")

def formula_parse(text):
    '''
    Create list of parsed formulas
    :return: (list) list of formulas to plot
    '''
    formulas = []
    error = None
    for index, i in enumerate(formula_list(text)):
        try:
            i = i.replace("^", "**").replace("e", "E").replace(",", ".")
            formulas.append(parse_expr(i))
        except:
            error = f"Zły wzór: {formula_list(text)[index]}. Pamiętaj by oddzielać wzory za pomocą \"; \""
            formulas = []
            break
    return formulas, error


def float_number(number: float):
    '''
    Check if number is float number
    :param number: (float) number to check
    :return: (bool) True - yes, False - no
    '''
    try:
        float(number)
    except:
        return False
    return True

def errors(xmin, xmax, ymin, ymax, text):
    '''
    Check if value of data to plot is correctly
    :return: (bool) True - yes, False - no
    '''
    for i in [xmin, xmax, ymin, ymax]:
        if i == "":
            return "Uzupełnij wszystkie obowiązkowe pola!"
    if float(xmin) >= float(xmax):
        return "Minimalna wartość zakresu osi X jest większa niż maksymalna!"
    elif float(ymin) >= float(ymax):
        return "Minimalna wartość zakresu osi Y jest większa niż maksymalna!"
    elif formula_parse(text)[1] != None:
        return formula_parse(text)[1]
    return None

def function_value(func, value):
    '''
    Count value of function for list of arguments
    :param func: function to count
    :param value: (list) list of arguments
    '''
    x = Symbol("x")
    lamb = lambdify(x, func, modules=['numpy'])
    if func.is_constant():
        return np.full_like(value, lamb(value))
    else:
        return lamb(value)

def plot_graph(xmin, xmax, ymin, ymax, formula, xtitle, ytitle, title, legend):
    '''
    Plot formulas on graph with specified title,
    x-axis title, y-axis title and legend
    '''
    x_value = np.linspace(float(xmin), float(xmax), 1000)
    errors = None
    try:
        plt.clf()
    except:
        pass
    for index, i in enumerate(formula_parse(formula)[0]):
        try:
            y_value = function_value(i, x_value)
            plt.plot(x_value, y_value, label=formula_list(formula)[index])
        except:
            errors = f"Źle wpisany wzór: {index + 1}: {formula_list(formula)[index]}"
    plt.xlim(float(xmin), float(xmax))
    plt.ylim(float(ymin), float(ymax))
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    plt.title(title)
    plt.grid(True)
    if legend:
        plt.legend(loc=1)
    return plt.gcf(), errors

def rysuj(xmin, xmax, ymin, ymax, formula, xtitle, ytitle, title, legend):
    fig, error = plot_graph(xmin, xmax, ymin, ymax, formula, xtitle, ytitle, title, legend)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"'data:image/png;base64,{data}'", error


@app.route("/narysuj/wykres", methods=["POST", "GET"])
def wykres():
    wzor=None
    liczba=None
    xmax=None
    ymin=None
    ymax=None
    obrazek=None
    error=None
    image = None
    if request.method == "POST":
        wzor = request.form["wzor"]
        xtitle = request.form["xtitle"]
        ytitle = request.form["ytitle"]
        title = request.form["title"]
        legend = bool(request.form.get("legenda"))
        liczba = request.form["xmin"]
        xmax = request.form["xmax"]
        ymin = request.form["ymin"]
        ymax = request.form["ymax"]
        if errors(liczba, xmax, ymin, ymax, wzor) == None:
            obrazek, error = rysuj(liczba,xmax,ymin,ymax,wzor, xtitle, ytitle, title, legend)
            image = True
        else:
            error=errors(liczba, xmax, ymin, ymax, wzor)
    return render_template("graf.html", obrazek=obrazek, error=error, image=image)

@app.route("/narysuj")
def narysuj():
    return render_template("graf.html", obrazek=None, error=None, image=None, legend=None)


