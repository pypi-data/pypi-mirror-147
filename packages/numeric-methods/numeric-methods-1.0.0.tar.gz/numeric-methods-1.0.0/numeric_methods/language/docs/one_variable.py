HALF_METHOD_DOCS = {
    "ENGLISH": """
    This method is implementing the half division method of root searching.
    
    Algorithm:
        x = (a + b) / 2
        if function(x) < 0 then
            a = x
        else if function(x) == 0 then
            yield x
        else
            b = x
        repeat until x_(i - 1)  -  x_(i) >= epsilon

    Conditions of using:
        [Automatic] Must be truth or ArithmeticError will raise: function(a_0) * function(b_0) < 0
        [Manually] Must be truth or some kind of exception will raise: function is continuous in [a_0, b_0]
    
    Example:
        | from numeric_methods.one_variable import half_method
        |
        |
        | # x ** 5 = 2
        | for line in half_method(lambda x: x ** 5 - 2, 1, 2, 0.001):
        |     print(line)

    :param function: Lambda or defined function which must support type of number and be continuity
    :param a: Begin of the slice where root is
    :param b: End of the slice where root is
    :param epsilon: Required precision of the `function(x) = 0` root
    :return: Root of the `function(x) = 0` with indicated precision
    """,
    "RUSSIAN": """
    Данный метод реализует нахождение корня методом половинного деления. 
    
    Алгоритм:
        x = (a + b) / 2
        if function(x) < 0 then
            a = x
        else if function(x) == 0 then
            yield x
        else
            b = x
        repeat until x_(i - 1)  -  x_(i) >= epsilon

    Условия использования:
        [Автоматически] Должно быть истинной или будет вызвана ArithmeticError: function(a_0) * function(b_0) < 0
        [Вручную] Должно быть истинно или будет вызвано исключение какого-то вида: функция непрерывна на [a_0, b_0]

    Пример:
        | from numeric_methods.one_variable import half_method
        |
        |
        | # x ** 5 = 2
        | for line in half_method(lambda x: x ** 5 - 2, 1, 2, 0.001):
        |     print(line)

    :param function: Lambda or defined function which must support type of number and be continuity
    :param a: Начало отрезка, в котором находится корень
    :param b: Конец отрезка, в котором находится корень
    :param epsilon: Требуемая точность корня уравнения `function(x) = 0`
    :return: Корень уравнения `function(x) = 0` с указанной точностью
    """
}
