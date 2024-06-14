# Реализация частичной перегрузки функции на Python

## Что такое перегрузка функции? (function overloading)
Перегрузка функции - это механизм, который позволяет определять функции с одним и тем же именем, но разным набором параметров.

## C++ и Python
В C++ существует встроенный механизм перегрузки функции, что по моему мнению очень удобно, однако, если мы попробуем перегрузить функцию в Python у нас ничего не полуится: функция перезапишется.
Но стоить отметить, что во встроенном модуле <a href="https://github.com/python/cpython/blob/main/Lib/functools.py"><code>functools</code></a> уже существует функция <code>singledispatch</code>, которая реализует
подобный функционал на основе первого переданного аргумента.

## Overload
Я решил реализовать подобный функционал, используя свои знания работы с ООП и аннотациями типов, получилось, как по мне крайне схоже)
