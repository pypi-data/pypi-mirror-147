from functools import reduce
from math import sqrt, gcd
from sympy.parsing.latex import parse_latex
from sympy import *
from sympy import sympify


class InputNoneError(Exception):
    pass

class TypeError(Exception):
    pass

class InvalidOperation(Exception):
    pass



def percent_of(num, percent):
    if num is None or percent is None:
        raise InputNoneError()
    return num * percent / 100


def square_root(num):
    if num is None:
        raise InputNoneError()
    elif num < 0:
        raise InvalidOperation()
    return sqrt(num)


def hcf(values):
    try:
        if values is None:
            raise InputNoneError()
        result = reduce(lambda x, y: gcd(x, y), values)
        return result
    except:
        for value in values:
            if isinstance(value, (int, float)):
                raise TypeError()
        raise Exception()


def lcm(values):
    try:
        if values is None:
            raise InputNoneError()
        result = reduce(lambda x, y: ((x * y) / gcd(x, y)), values)
        return result
    except:
        for value in values:
            if isinstance(value, (int, float)):
                raise TypeError()
        raise Exception()


def decimal_to_hex(operand):
    try:
        if operand is None:
            raise InputNoneError()
        elif isinstance(operand, int):
            raise TypeError()
        result = hex(operand).split('x')[1]
        return result
    except:
        raise Exception()


def factors_quad(values):
    try:
        if values is None:
            raise InputNoneError()
        factor1 = []
        factor2 = []
        nfactor1 = []
        nfactor2 = []
        f = values[0]
        b = values[1]
        # creating factors
        for i in range(1, int(pow(f, 1 / 2)) + 1):
            if f % i == 0:
                factor1.append(str(i))
                factor2.append(str(int(f / i)))
        # negative factors
        for i in factor1:
            i = -1 * sympify(i)
            nfactor1.append(i)
        for j in factor2:
            nfactor2.append(-1 * sympify(j))
        # checking p and q
        t1 = 0
        t2 = 0
        for i in range(len(nfactor1)):
            if int(factor1[i]) + int(factor2[i]) == b:
                t1 = factor1[i]
                t2 = factor2[i]
            if int(factor1[i]) + int(nfactor2[i]) == b:
                t1 = factor1[i]
                t2 = nfactor2[i]
            if int(nfactor1[i]) + int(factor2[i]) == b:
                t1 = nfactor1[i]
                t2 = factor2[i]
            if int(nfactor1[i]) + int(nfactor2[i]) == b:
                t1 = nfactor1[i]
                t2 = nfactor2[i]
        return factor1, factor2, nfactor1, nfactor2, t1, t2

    except:
        for value in values:
            if isinstance(value, (int, float)):
                raise TypeError()
        raise Exception()

def split_on_symbol(expr,symbol):
    try:
        if expr or symbol is None:
            raise InputNoneError()
        if symbol in exp:
            if "(" in symbol:
                result = (exp).split(symbol)
                result[1] = "(" + result[1]
            else:
                result = (exp).split(symbol)
        else:
            result = [exp, 1]
        return sympify(result[0]), sympify(result[1])
    except:
        raise Exception()

def split_on_sum(expr):
    try:
        if expr is None:
            raise InputNoneError()
        exp = str(expr)
        lis = exp.split()
        for i in range(len(lis)):
            if lis[i] == "-":
                lis[i + 1] = str(-1 * sympify(lis[i + 1]))
            else:
                lis[i] = lis[i]
        for i in lis:
            if i == "+":
                lis.remove("+")
            if i == "-":
                lis.remove("-")
        result = lis
        return result
    except:
        raise Exception()

def conjugate(expr):
    try:
        if expr is None:
            raise InputNoneError()
        exp = str(expr)
        if "+" in exp:
            exp = exp.replace("+", "-")
        elif "-" in exp:
            exp = exp.replace("-", "+")
        return sympify(exp)
    except:
        raise Exception()

def parse_abs_terms(expr):
    try:
        if expr is None:
            raise InputNoneError()
        e = str(expr)
        cbr = 0
        start = []
        end = []
        abs_terms = []
        for i in range(0, len(e)):
            if e[i] == "(" and e[i - 1] == "s":
                cbr = cbr + 1
                start.append(i)
                for j in range(i + 1, len(e)):
                    if e[j] == "Abs(" and e[j - 1] == "s" or e[j] == "(":
                        cbr = cbr + 1
                    elif e[j] == ")":
                        cbr = cbr - 1
                        if cbr == 0:
                            end1 = j
                            end.append(j)
                            break
                        else:
                            end1 = 0
        start_new = []
        end_new = []
        for i in range(0, len(end)):
            for j in range(i + 1, len(end)):
                if end[i] > end[j]:
                    end_new.append(end[j])
                    start_new.append(start[j])
                    continue
                else:
                    continue
        for (l, m) in zip(start_new, end_new):
            start.remove(l)
            end.remove(m)
        for (i, j) in zip(start, end):
            bracket = e[i:j + 1]
            bracket = "Abs" + bracket + ""
            abs_terms.append(bracket)
        result = abs_terms
        return result
    except:
        raise Exception()

def parse_constant_terms(expr):
    try:
        if expr is None:
            raise InputNoneError()
        #exp = str(expr)
        ex1 =expr
        ex2 = str(ex1)
        ex = ex2.split(" ")
        terms = []
        operators = []

        for i in range(0, len(ex)):
            if "x" not in ex[i] and i > 0:
                terms.append(ex[i])
                operators.append(ex[i - 1])
                i = i + 1
            elif "x" not in ex[i]:
                terms.append(ex[i])
                i = i + 1

        con_list = []

        if len(operators) == len(terms):
            for i in range(0, len(terms)):
                con_list.append(operators[i])
                con_list.append(terms[i])
        else:
            for i in range(0, len(terms)):
                if i == (len(terms) - 1):
                    con_list.append(terms[i])
                else:
                    con_list.append(terms[i])
                    con_list.append(operators[i])

        expr = (" ").join(con_list)
        result = expr
        return result
    except:
        raise Exception()


def is_in_interval(interval,value):
    try:
        if interval is None:
            raise InputNoneError()
        if value is None:
            raise InputNoneError()
        interval = interval.replace("(", "")
        interval = interval.replace(")", "")
        interval = interval.replace("[", "")
        a = interval.split(",")
        a[0] = sympify(a[0])
        a[1] = sympify(a[1])
        if a[0] <= value < a[1]:
            result = True
        else:
            result = False
        return result
    except:
        raise Exception()

def range_ceil(lhs,rhs):
    try:
        if lhs is None:
            raise InputNoneError()
        if rhs is None:
            raise InputNoneError()
        lhs = str(lhs)
        rhs = str(rhs)
        if "ceil" in rhs:
            lhs,rhs = rhs,lhs
        rhs = sympify(rhs)
        e = lhs.split("ceil")
        exp = sympify(e[1])
        range_ceil = str(rhs - 1) + " < " + str(exp) + " <= " + str(rhs)
        left_term = rhs - 1
        right_term = rhs
        return exp, range_ceil, left_term, right_term
    except:
        Exception()

def range_floor(lhs,rhs):
        try:
            if lhs is None:
                raise InputNoneError()
            if rhs is None:
                raise InputNoneError()
            lhs = str(lhs)
            rhs = str(rhs)
            if "ceil" in rhs:
                lhs, rhs = rhs, lhs
            rhs = sympify(rhs)
            e = lhs.split("floor")
            exp = sympify(e[1])
            range_floor = str(rhs) + " <= " + str(exp) + " < " + str(rhs + 1)
            left_term = rhs
            right_term = rhs + 1
            return exp, range_floor, left_term, right_term
        except:
            raise Exception()

def create_ineq(lhs,rhs,operator):
    try:
        if lhs is None:
            raise InputNoneError()
        if rhs is None:
            raise InputNoneError()
        if operator == "<":
            result = lhs < rhs
        if operator == "<=":
            result = lhs <= rhs
        if operator == ">":
            result = lhs > rhs
        if operator == ">=":
            result = lhs >= rhs
        return result
    except:
        raise Exception()

def Intersection(values):
    try:
        if values is None:
            raise InputNoneError()
        result = reduce((lambda x, y: Intersection(x, y)), values)
        return result
    except:
        raise Exception()
def create_log(expr,base):
    try:
        if expr is None:
            raise InputNoneError()
        if base == None:
            base = 10
        else:
            base = base
        result = "\log _{" + str(base) + "}(" + expr + ")"
        result = parse_latex(result)
        return result
    except:
        raise Exception()

def solve_log(expr):
    try:
        if expr is None:
            raise InputNoneError()
        exp = str(expr)
        e = exp
        cbr = 0
        start = []
        end = []
        log_terms = []
        for i in range(0, len(e)):
            if e[i] == "(" and e[i - 1] == "g":
                cbr = cbr + 1
                start.append(i)
                for j in range(i + 1, len(e)):
                    if e[j] == "log(" and e[j - 1] == "g" or e[j] == "(":
                        cbr = cbr + 1
                    elif e[j] == ")":
                        cbr = cbr - 1
                        if cbr == 0:
                            end1 = j
                            end.append(j)
                            break
                        else:
                            end1 = 0
        start_new = []
        end_new = []
        for i in range(0, len(end)):
            for j in range(i + 1, len(end)):
                if end[i] > end[j]:
                    end_new.append(end[j])
                    start_new.append(start[j])
                    continue
                else:
                    continue
        for (l, m) in zip(start_new, end_new):
            start.remove(l)
            end.remove(m)
        for (i, j) in zip(start, end):
            bracket = e[i:j + 1]
            bracket = "log" + bracket + ""
            log_terms.append(bracket)
        values = log_terms
        solution_log = []
        new_values = []
        for i in range(0, len(values)):
            new_value = simplify(values[i])
            statement = values[i] + "=" + str(new_value)
            new_values.append(new_value)
            solution_log.append(statement)
        new = []
        new = []
        for value in new_values:
            x = re.search("[a-zA-Z]", values[i])
            if x == None:
                value = str(value)
                new.append(value)
            else:
                value = str(value)
                new.append(value)
        for (i, j) in zip(log_terms, new):
            exp = exp.replace(i, j)
        return parse_expr(exp), solution_log, new_values[0]

    except:
        raise Exception()

def Newton_method(expr):
    try:
        if expr is None:
            raise InputNoneError()
        def evaluate_sym_exp(expr, value):
            """Evaluating the symbolic function"""
            return expr.subs(list(expr.free_symbols)[0], value)

        def newtons_method(fn):
            """
            Newtons Method
            The function takes a symbolic expression as the input and gives one root of the function as output
            """
            n = 0
            x = 1
            while n < 10:
                fn_val = evaluate_sym_exp(fn, x)
                dif_fn_val = evaluate_sym_exp(diff(fn), x)
                x = x - (fn_val / dif_fn_val)
                n = n + 1
            x1 = round(x, 4)
            return x1
        result = newtons_method(exp)
        return result
    except:
        raise Exception()


def synthetic_division(coef,root):
    try:
        if coef or root is None:
            raise InputNoneError()
        """
          Synthetic Division
          It takes one of the roots of n-degree polynomial and outputs a polynomial of n-1 degree
          """
        quotient = []
        val = coef[0]
        for i, j in enumerate(coef):
            if i == 0:
                quotient.append(coef[i])
            else:
                val = val * root + coef[i]
                quotient.append(val)
        quotient.pop()
        return (quotient)
    except:
        raise Exception()

def find_coeffs(expr):
    try:
        if expr  is None:
            raise InputNoneError()
        cof = []
        y1 = exp
        deg = degree(y1)
        while deg >= 0:
            cof1 = y1.coeff("x", deg)
            cof.append(cof1)
            deg = deg - 1

        return cof
    except:
        raise Exception()

def generate_expr(coef,symbol):
    try:
        if coef is None:
            raise InputNoneError()
        if symbol is None:
            symbol = "x"
        else:
            symbol = symbol
        sym_fun = 0
        symbol = Symbol(symbol)
        for i, val in enumerate(coef):
            sym_fun = sym_fun + coef[-1 - i] * symbol ** i
        return sym_fun
    except:
        raise Exception()
