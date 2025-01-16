Customizing Extensions
======================

* scPantheon supports customizing extensions following certain formats.
* To insert your own method in scPantheon software, you can write a script in default extensions path:
    * In Windows:
    * In linux: ``.local/share/scpantheon/0.6.0.0/extensions``
    * In MacOS:
* Steps:

  1. Create a directory under the default path

  .. code-block:: bash
    :caption: eg: ``Clustering_with_Scanpy`` as your extensions name  

      mkdir Clustering_with_Scanpy
      touch Clustering_with_Scanpy/module.py

  2. In ``module.py`` just created, import modules:

  .. code-block:: python

      # import necessary modules
      from bokeh.layouts import row, column
      from scpantheon.widgets import Widgets
      from scpantheon.buttons import Widget_type, make_widget
      from bokeh.io import curdoc
      import tabs as tb
      import data as dt
      # import other modules required here
      import scanpy as sc
      import base64

  3. Create class ``Widget_Ext(Widget)``
   
    .. note:: Don't change the name of the class.

    .. automodule:: Clustering_with_Scanpy.module
        :members:
        :undoc-members:
        :show-inheritance:
        
    * ``__init__``

    .. code-block:: python

        def __init__(self,
            name: str | None = 'generic columns',
        ):
            super().__init__(name)
            self.init_extension()
            super().init_tab()
      
    .. note:: You don't need to change anything in this ``__init__`` function.
    
    * ``init_extension``

    In this function, customize the initial tab in the visualization of your method by defining widgets and arranging it into a layout.
    scPantheon is based on bokeh, however, you don't need to learn bokeh from scratch.
    Instead, you can use some basic bokeh widgets we've encapsulated in :ref:`buttons` module.

    First, create widgets with

    .. py:function:: make_widget(widget_type: Widget_type, func = None, **kwargs)
        
        :param widget_type: defines which kind of widget to create by format: ``Widget_type.type``
        :param func: callback function if needed
        :param \**kwargs: parameter dictionary with parameter name as keys and parameter value as value
    
    .. note:: 
        .. line-block::
            ``widget_type`` are limited and ``**kwargs`` are also limited according to widget_type. 
            They are listed in the following table.
            Widget_types like ``Widget_type.div`` that doesn't respond to callback functions are remarked as ``None`` in column **func**.
            **necessary_param** lists parameters necessary to the widget_type. Without any one of them, the widget malfunctions.
            **core_param** lists other useful parameters.
            **all_param** lists all parameters allowed. Any parameters other than all_param will be automatically omitted by scPantheon. 

    +-----------------------------------+----------+-----------------+------------+-----------+
    | widget_type                       | func     | necessary_param | core_param | all_param |
    +===================================+==========+=================+============+===========+
    | ``Widget_type.div``               | ``None`` | column 3        | column 4   |           |
    +-----------------------------------+----------+-----------------+------------+-----------+
    | ``Widget_type.text``              | ``None`` | ...             |            |           |
    +-----------------------------------+----------+-----------------+------------+-----------+
    | ``Widget_type.button``            | allowed  | ...             |            |           |
    +-----------------------------------+----------+-----------------+------------+-----------+
    | ``Widget_type.select``            | allowed  | ...             |            |           |
    +-----------------------------------+----------+-----------------+------------+-----------+
    | ``Widget_type.autocompleteInput`` | allowed  | ...             |            |           |
    +-----------------------------------+----------+-----------------+------------+-----------+
    | ``Widget_type.checkBoxGroup``     | allowed  | ...             |            |           |
    +-----------------------------------+----------+-----------------+------------+-----------+
    | ``Widget_type.radioButtonGroup``  | allowed  | ...             |            |           |
    +-----------------------------------+----------+-----------------+------------+-----------+
    | ``Widget_type.slider``            | allowed  | ...             |            |           |
    +-----------------------------------+----------+-----------------+------------+-----------+
    | ``Widget_type.rangeSlider``       | allowed  | ...             |            |           |
    +-----------------------------------+----------+-----------------+------------+-----------+

    .. note:: To see detailed examples of all widget_types, please refer to ..
        To learn more about original bokeh widgets, please refer to ..

    .. code-block:: python
        :caption: example in Clustering_with_Scanpy

        #customize you widgets
        sc_cluster_step1_arg = {'label': 'Step1: Run PCA', 'button_type': 'success'}
        sc_cluster_step1 = make_widget(Widget_type.button, lambda : self.pca(), **sc_cluster_step1_arg)
        cl_input1_arg = {'title': 'Neighbor Num:', 'value': '10'}
        cl_input1 = make_widget(Widget_type.text, **cl_input1_arg)
        cl_input2_arg = {'title':'Principal Component Num:', 'value': '40'}
        cl_input2 = make_widget(Widget_type.text, **cl_input2_arg)
        cl_input3_arg = {'title':'Resolution:', 'value': '1'}
        cl_input3 = make_widget(Widget_type.text, **cl_input3_arg)
        sc_cluster_step2_arg = {'label': 'Step2: Clustering with Neighborhood Graph', 'button_type': 'success'}
        sc_cluster_step2 = make_widget(
            Widget_type.button,
            lambda: self.neighborhood_graph(cl_input1.value, cl_input2.value, cl_input3.value),
            **sc_cluster_step2_arg
            )
        
    .. code-block:: python

        widgets_dict = {          
            'sc_cluster_step1': sc_cluster_step1,
            'cl_input1': cl_input1,
            'cl_input2': cl_input2,
            'cl_input3': cl_input3,
            'sc_cluster_step2': sc_cluster_step2
        }
        self.widgets_dict = {**self.widgets_dict, **widgets_dict}

    * callback functions
    