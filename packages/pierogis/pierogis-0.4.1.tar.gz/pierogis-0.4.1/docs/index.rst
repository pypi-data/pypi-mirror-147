pierogis
========

**image and animation processing framework**

   *"ingredients that describe image processing functions can be assembled
   into recipes and used to cook an image or animation."*

   \- a wise man

.. py:currentmodule:: pierogis.ingredients

Pixel arrays (like images) stored as a :py:class:`~pierogi.Pierogi` object can be cooked
with an :py:class:`~ingredient.Ingredient`
such as :py:class:`~sort.Sort`, :py:class:`~quantize.Quantize`,
and :py:class:`~resize.Resize`.

A :py:class:`~dish.Dish` can be made with a :py:class:`~recipe.Recipe` containing
several :py:class:`~ingredient.Ingredient` objects describing a pipeline
to be applied to a :py:class:`~pierogi.Pierogi`.

A :py:class:`~pierogis.course.Course` can be made to cook a set of
:py:class:`~dish.Dish` objects representing frames
that compile to a cooked animation.

.. py:currentmodule:: pierogis.kitchen.menu

A :doc:`rich <rich:introduction>` cli uses :py:class:`~filling.Filling`
objects to parse orders into cook tasks as a :py:class:`~pierogis.restaurant.Restaurant`.
These can be found on the :doc:`menu/index`.

In this realm, a single `pierogi` means a pixel, many `pierogi` means an image, and `pierogis` means many images.

.. toctree::
   :maxdepth: 3
   :caption: usage

   cli
   ingredients
   kitchen

.. toctree::
   :maxdepth: 3
   :caption: api

   source/modules

* :ref:`modindex`
