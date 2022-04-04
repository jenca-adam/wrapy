.. role:: python(code)
   :language: python
WraPy documentation (1.2.0)
===========================

What is WraPy ?
---------------

WraPy is a pythonic tool to create API wrappers in one function call.

Typical WraPy usage goes on like this::

        import wrapy
        my_wrapper = wrapy.WraPy('https://api.example.com/')

``wrapy.WraPy`` returns class!
The class instance contains data returned by API endpoint.

For example, let's say you want to get exchange rates. Then::
        
        import wrapy
        Rates = wrapy.WraPy('https://open.er-api.com/v6/latest/USD',slash=False)
        r=Rates()
        r.result #"success"
        r.rates #object
        r.rates.USD #1
        r.rates.EUR #EUR rate

Of course, the most interesting line here is ``Rates = wrapy.WraPy('https://open.er-api.com/v6/latest/USD',slash=False)``.
Let's analyze it.
``https://open.er-api.com/v6/latest/USD`` is obviously link to API.
What does ``slash=False`` mean?
WraPy automatically tries to append slash at the end of every URL requested.
This API does not support it, so you must specify it using ``slash`` argument.

