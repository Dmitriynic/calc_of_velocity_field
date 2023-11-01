<h2 align="center">Поле скоростей точек движущегося изображения</h2>
<p align="center">
   <img src="https://i.ibb.co/dkkQ2Q0/756778395635314.webp" height="300">
</p>
<p align="center">
   <img alt="Static Badge" src="https://img.shields.io/badge/Python-3.9.13-red">
   <img alt="Static Badge" src="https://img.shields.io/badge/PyOpenGl-3.1.7-blue">
   <img alt="Static Badge" src="https://img.shields.io/badge/License-MIT-green">
</p>

## Описание

Расчет поля скоростей точек движущегося изображения при спутниковой фотосъемке поверхности Земли.

Данная программа выполняет ряд задач:
<ul>
<li>Моделирование движения по кеплеровой орбите искусственного спутника Земли. Построение трассы ИСЗ 
и пересечения главной оптической оси бортовой оптикоэлектронной апаратуры
с её поверхностью на картографической проекции Земли а также в гринвической системе координат
с последующей визуализацией;
</li>
<li>Вычисление поля скоростей для ПЗС-линейки,
состоящей из одной или нескольих светочувствительных пластин
и его минимизация для различных углов крена и рыскания ИСЗ;</li>
<li>Нахождение закона управления углом крена, который обеспечивает
оптимальное соединение соседних кадров;</li>
<li>Поиск угла рыскания для минимизации поперечной составляющей смаза изображения;
</li>
<li>Поиск длины последовательности снимков, для которых достаточно
использовать вычисления, реализованные только для первого кадра фотосъемки.
</li>
</ul>


## Функционал

Используются следующие режимы работы программы:

<ul>
<li>

[`visual`](#)</li>
<li>

`min_field`</li>
<li>

`half_plate`</li>
<li>

`add_roll_angle`</li>

<li>

`field_sequence`</li>

<li>

`field_save`</li>
</ul>

В режиме`visual` выполняется ряд вычислений, включающих построение орбиты спутника
и поиск его положения в определенный момент времени на основе данных кеплеровой орбиты
, вычисление трассы спутинка и пересечения направления визира, отклоненного
на заданный угол крена с Землей. Затем все вышеперечисленные результаты отрисовываются
и анимируются.

<p align="center">
    <img src="https://i.ibb.co/WHbMwgG/2023-11-01-16-30-01.png" height="300">
</p>

`min_field` обеспечивает среднеквадратичную минимизацию поля скоростей для направления визира на подспутниковую точку.
При этом ПЗС-линейка в данном случае состоит из одной светочувствительной пластины.
Также происходит представление поля скоростей и его минимизации 
в графической форме.

<div align = "center">
    <figure align = "center">
        <img src="https://i.ibb.co/7nh16FG/2023-11-01-15-30-39.png" height = "400">
        <figcaption>Поле скоростей до минимизации</figcaption>
    </figure>
    <figure>
        <img src="https://i.ibb.co/c2bWHbM/2023-11-01-15-30-22.png" height="400">
        <figcaption>Поле скоростей после минимизации</figcaption>
    </figure>
</div>

`min_field_graph` дополнительно определяет зависимость максимальных значений
длин векторов поля скоростей от истинной аномалии в момент осуществления фотосъемки.

<p align = "center">
        <img src="https://i.ibb.co/1M9Z92L/2023-11-01-15-48-04.png" height = "400">
</p>

`half_plate` отрисовывает точки на поверхности Земли, которые затем преобразуются в изображение,
создаваемое ПЗС-линейкой. Оно является склейкой последовательности кадров. ИСЗ в данном случае
движется вдоль экватора, а съемка выполняется в надир. ПЗС-линейка состоит из четного числа светочувствительных
матриц, расположенных в шахматном порядке. На рисунке представлен результат работы
режима для одного и нескольих снимков.

<p align="center">
    <img src="https://i.ibb.co/2t0DFz4/2023-11-01-15-53-19.png" height="400">
</p>

`add_roll_angle` решает задачу нахождения закона управления углом крена, который обеспечивает
оптимальное соединение соседних кадров, при условии, что изначально ведется съемка надира.
Для наглядности результатов вычислений выбран произвольный угол рыскания.

<div align = "center">
    <figure align = "center">
        <img src="https://i.ibb.co/8cq9Nmb/2023-11-01-16-00-11.png" height = "500">
        <figcaption>Охват земной поверхности без использования закона управления углом крена</figcaption>
    </figure>
    <figure>
        <img src="https://i.ibb.co/FV5KFtf/2023-11-01-16-00-18.png" height="500">
        <figcaption>Охват земной поверхности с использованием закона управления углом крена</figcaption>
    </figure>
</div>

`field_sequence` выдает результат минимизации склейки последовательности снимков. Здесь
минимизация проводится для каждого снимка отдельно. Учитывается минимизация поперечной составляющей с помощью угла рыскания.

<p align="center">
    <img src="https://i.ibb.co/BgXrLnZ/2023-11-01-16-07-01.png" height="200">
</p>

`field_save` вычисляет количество последовательных кадров, для
которых достаточно рассчитать поле скоростей первого снимка.
Для того, чтобы продолжать съемку без использования новых вычислений,
необходимо, чтобы разность максимальных значений длин полученных векторов
сохраненного поля, и поля, вычисляемого в режиме работы программы `field_sequence`
не превышала одного пикселя. Также определяет зависимость максимального модуля
вектора скорости точек движущегося изображения от времени, при сохранении одного
результата минимизации для последовательности снимков.

<p align="center">
    <img src="https://i.ibb.co/NsGPFG3/2023-11-01-16-12-40.png" height="400">
</p>

Угол тангажа остается неизменным для всех режимов работы программы.

## Библиотеки
<ul>
<li>

`matplotlib`</li>
<li>

`numpy`</li>
<li>

`Pillow`</li>
<li>

`pygame`</li>

<li>

`PyOpenGL`</li>

<li>

`scipy`</li>
</ul>