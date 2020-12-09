import pytest 
import numpy as np
import graddog as gd
from graddog.trace import Trace, Variable
from graddog.functions import sin, arcsin, sinh, cos, arccos, cosh, tan, arctan, tanh, exp, log, sigmoid, sqrt

def test_sin():
    value = 0.5
    x = Variable('x', value)
    a = sin(value)
    b = arcsin(value)
    c = sinh(value)
    assert a == pytest.approx(np.sin(value))
    assert b == pytest.approx(np.arcsin(value))
    assert c == pytest.approx(np.sinh(value))
    g = sin(x)
    h = arcsin(x)
    i = sinh(x)
    assert g.val == pytest.approx(np.sin(value))
    assert h.val == pytest.approx(np.arcsin(value))
    assert i.val == pytest.approx(np.sinh(value))

def test_cos():
    value = 0.5
    x = Variable('x', value)
    a = cos(value)
    b = arccos(value)
    c = cosh(value)
    assert a == pytest.approx(np.cos(value))
    assert b == pytest.approx(np.arccos(value))
    assert c == pytest.approx(np.cosh(value))
    g = cos(x)
    h = arccos(x)
    i = cosh(x)
    assert g.val == pytest.approx(np.cos(value))
    assert h.val == pytest.approx(np.arccos(value))
    assert i.val == pytest.approx(np.cosh(value))

def test_tan():
    value = 0.5
    x = Variable('x', value)
    a = tan(value)
    b = arctan(value)
    c = tanh(value)
    assert a == pytest.approx(np.tan(value))
    assert b == pytest.approx(np.arctan(value))
    assert c == pytest.approx(np.tanh(value))
    g = tan(x)
    h = arctan(x)
    i = tanh(x)
    assert g.val == pytest.approx(np.tan(value))
    assert h.val == pytest.approx(np.arctan(value))
    assert i.val == pytest.approx(np.tanh(value))

def test_sigmoid():
    value = 0.5
    x = Variable('x', value)
    g = sigmoid(x)
    a = sigmoid(value)
    assert a == pytest.approx(1/(1 + np.exp(-value)))
    assert g.val == pytest.approx(1/(1 + np.exp(-value)))

def test_sqrt():
    value = 9
    x = Variable('x', value)
    a = sqrt(value)
    assert a == pytest.approx(np.sqrt(value))
    g = sqrt(x)
    assert g.val == pytest.approx(np.sqrt(value))
        
def test_log_base2():
    x = Variable('x', 32)
    base = 2
    f = log(x, base=base)
    assert f._val == pytest.approx(5)
    assert f._der['v1'] == 1/(x._val * np.log(base))
    
def test_exp_base2():
    x = Variable('x', 5)
    base = 2
    f = exp(x, base=base)
    assert f._val == pytest.approx(32)
    assert f._der['v1'] == (base**x._val)*np.log(base)

def test_log():
    value = 4
    x = Variable('x', value)
    f = log(x)
    a = log(value)
    assert a == pytest.approx(np.log(value))
    assert f._val == np.log(value)
    assert f._der['v1'] == pytest.approx(0.25)

def test_exp():
    value = 67
    x = Variable('x', value)
    f = exp(x)
    a = exp(value)
    assert a == pytest.approx(np.exp(value))
    assert f._val == pytest.approx(np.exp(value), rel=1e-5)
    assert f._der['v1'] == f._val

def test_composition_val():
    value = np.pi/6
    x = Variable('x', value)
    c = cos(x)
    s = sin(x)
    t = tan(x)
    e = exp(x)
    f = c * t + e
    g = c + s
    assert isinstance(f, Trace)
    assert f._val == np.cos(value)*np.tan(value) + np.exp(value)

def test_basic_der():
    # Decorator function maker that can be used to create function variables
    def fm(f):
        def fun(x):
            return f(x) 
        return fun  
      
    value = 0.5
    assert gd.trace(fm(sin), value) == np.cos(value)
    assert gd.trace(fm(cos), value) == -np.sin(value)
    assert gd.trace(fm(tan), value) == 1/(np.cos(value)*np.cos(value))

def test_composition_der():
    def f(x):
        return cos(x)*tan(x) + exp(x)
    value = 0.5
    der = gd.trace(f, value)
    assert der[0] == -1*np.sin(value)*np.tan(value) + 1/np.cos(value) + np.exp(value)

def test_string_input():
    with pytest.raises(ValueError):
        f = sin('test')
    with pytest.raises(ValueError):
        f = cos('test')
    with pytest.raises(ValueError):
        f = tan('test')
    with pytest.raises(ValueError):
        f = sinh('test')
    with pytest.raises(ValueError):
        f = cosh('test')
    with pytest.raises(ValueError):
        f = tanh('test')
    with pytest.raises(ValueError):
        f = arcsin('test')
    with pytest.raises(ValueError):
        f = arccos('test')
    with pytest.raises(ValueError):
        f = arctan('test')
    with pytest.raises(ValueError):
        f = sqrt('test')
    with pytest.raises(ValueError):
        f = sigmoid('test')
    with pytest.raises(ValueError):
        f = log('test')
    with pytest.raises(ValueError):
        f = exp('test')

def test_arc_domains():
    x = Variable('x', 2)
    y = 2
    with pytest.raises(ValueError):
        f = arcsin(x)
    with pytest.raises(ValueError):
        f = arccos(x)
    with pytest.raises(ValueError):
        f = arcsin(y)
    with pytest.raises(ValueError):
        f = arccos(y)
