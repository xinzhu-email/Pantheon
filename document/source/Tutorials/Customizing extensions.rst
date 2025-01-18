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
        :param \**kwargs: keyword arguments
    
    .. note:: 
        1. ``widget_type`` are limited and ``**kwargs`` are also limited according to widget_type. They are listed in the following table.
        2. Widget_types like ``Widget_type.div`` that doesn't respond to callback functions are remarked as ``None`` in column **func**.
        3. **necessary_param** lists parameters necessary to the widget_type. Without any one of them, the widget malfunctions.
        4. **core_param** lists other useful parameters.
        5. **all_param** lists all parameters allowed. Any parameters other than all_param will be automatically omitted by scPantheon. 

    .. list-table:: 
        :header-rows: 1

        * - widget_type
          - func
          - necessary_param
          - core_param
          - all_param
        * - ``Widget_type.div``
          - ``None``
          - ``'text'``
          - ``'disable_math'``
          - .. line-block:: 
                ``'align'``, ``'aspect_ratio'``, ``'background'``, ``'css_classes'``, ``'default_size'``, ``'disable_math'``,\ 
                ``'disabled'``, ``'height'``, ``'height_policy'``, ``'js_event_callbacks'``, ``'js_property_callbacks'``, ``'margin'``,\ 
                ``'max_height'``, ``'max_width'``, ``'min_height'``, ``'min_width'``, ``'name'``, ``'render_as_text'``, ``'sizing_mode'``,\ 
                ``'style'``, ``'subscribed_events'``, ``'syncable'``, ``'tags'``, ``'text'``, ``'visible'``, ``'width'``, ``'width_policy'``

        * - ``Widget_type.text``
          - ``None``
          - /
          - ``'title'``, ``'value'``
          - .. line-block::
                ``'align'``, ``'aspect_ratio'``, ``'background'``, ``'css_classes'``, ``'default_size'``, ``'disabled'``, ``'height'``,\ 
                ``'height_policy'``, ``'js_event_callbacks'``, ``'js_property_callbacks'``, ``'margin'``, ``'max_height'``, ``'max_length'``,\ 
                ``'max_width'``, ``'min_height'``, ``'min_width'``, ``'name'``, ``'placeholder'``, ``'sizing_mode'``, ``'subscribed_events'``,\ 
                ``'syncable'``, ``'tags'``, ``'title'``, ``'value'``, ``'value_input'``, ``'visible'``, ``'width'``, ``'width_policy'``\ 

        * - ``Widget_type.button``
          - allowed
          - /
          - ``'label'``
          - .. line-block::
                ``'align'``, ``'aspect_ratio'``, ``'background'``, ``'button_type'``, ``'css_classes'``, ``'default_size'``,\ 
                ``'disabled'``, ``'height'``, ``'height_policy'``, ``'icon'``, ``'js_event_callbacks'``, ``'js_property_callbacks'``,\ 
                ``'label'``, ``'margin'``, ``'max_height'``, ``'max_width'``, ``'min_height'``, ``'min_width'``, ``'name'``,\  
                ``'sizing_mode'``, ``'subscribed_events'``, ``'syncable'``, ``'tags'``, ``'visible'``, ``'width'``, ``'width_policy'``\ 
            
        * - ``Widget_type.select``
          - allowed
          - ``'options'``, ``'value'``
          - ``'title'``
          - .. line-block::
                ``'align'``, ``'aspect_ratio'``, ``'background'``, ``'css_classes'``, ``'default_size'``, ``'disabled'``, ``'tags'``,\ 
                ``'height'``, ``'height_policy'``, ``'js_event_callbacks'``, ``'js_property_callbacks'``, ``'margin'``,\ 
                ``'max_height'``, ``'max_width'``, ``'min_height'``, ``'min_width'``, ``'name'``, ``'options'``, ``'sizing_mode'``,\  
                ``'subscribed_events'``, ``'syncable'``, ``'title'``, ``'value'``, ``'visible'``, ``'width'``, ``'width_policy'``\ 

        * - ``Widget_type.autocompleteInput``
          - allowed
          - ``'completions'``
          - .. line-block::
                ``'min_characters'``, ``'value'``,\ 
                ``'case_sensitive'``, ``'title'``\ 
          - .. line-block::
                ``'align'``, ``'aspect_ratio'``, ``'background'``, ``'case_sensitive'``, ``'completions'``, ``'css_classes'``,\ 
                ``'default_size'``, ``'disabled'``, ``'height'``, ``'height_policy'``, ``'js_event_callbacks'``,\ 
                ``'js_property_callbacks'``, ``'margin'``, ``'max_height'``, ``'max_length'``, ``'max_width'``, ``'min_characters'``,\  
                ``'min_height'``, ``'min_width'``, ``'name'``, ``'placeholder'``, ``'restrict'``, ``'sizing_mode'``, ``'subscribed_events'``,\  
                ``'syncable'``, ``'tags'``, ``'title'``, ``'value'``, ``'value_input'``, ``'visible'``, ``'width'``, ``'width_policy'``\ 

        * - ``Widget_type.checkBoxGroup``
          - allowed
          - ``'labels'``
          - ``'active'``
          - .. line-block::
                ``'active'``, ``'align'``, ``'aspect_ratio'``, ``'background'``, ``'css_classes'``, ``'default_size'``, ``'disabled'``,\ 
                ``'height'``, ``'height_policy'``, ``'inline'``, ``'js_event_callbacks'``, ``'js_property_callbacks'``, ``'labels'``,\ 
                ``'margin'``, ``'max_height'``, ``'max_width'``, ``'min_height'``, ``'min_width'``, ``'name'``, ``'sizing_mode'``,\ 
                ``'subscribed_events'``, ``'syncable'``, ``'tags'``, ``'visible'``, ``'width'``, ``'width_policy'``\ 

        * - ``Widget_type.radioButtonGroup``
          - allowed
          - ``'labels'``
          - ``'active'``
          - .. line-block::
                ``'active'``, ``'align'``, ``'aspect_ratio'``, ``'background'``, ``'button_type'``, ``'css_classes'``, ``'default_size'``,\ 
                ``'disabled'``, ``'height'``, ``'height_policy'``, ``'js_event_callbacks'``, ``'js_property_callbacks'``, ``'labels'``,\ 
                ``'margin'``, ``'max_height'``, ``'max_width'``, ``'min_height'``, ``'min_width'``, ``'name'``, ``'orientation'``,\ 
                ``'sizing_mode'``, ``'subscribed_events'``, ``'syncable'``, ``'tags'``, ``'visible'``, ``'width'``, ``'width_policy'``\ 

        * - ``Widget_type.slider``
          - allowed
          - .. line-block::
              ``'start'``, ``'end'``,\ 
              ``'value'``, ``'step'``\ 
          - .. line-block::
              ``'title'``, ``'format'``,\ 
              ``'orientation'``, \ 
              ``'show_value'``, ``'bar_color'``\ 
          - .. line-block::
              ``'align'``, ``'aspect_ratio'``, ``'background'``, ``'bar_color'``, ``'css_classes'``, ``'default_size'``, ``'width_policy'``\ 
              ``'direction'``, ``'disabled'``, ``'end'``, ``'format'``, ``'height'``, ``'height_policy'``, ``'js_event_callbacks'``,\ 
              ``'js_property_callbacks'``, ``'margin'``, ``'max_height'``, ``'max_width'``, ``'min_height'``, ``'min_width'``,\ 
              ``'name'``, ``'orientation'``, ``'show_value'``, ``'sizing_mode'``, ``'start'``, ``'step'``, ``'subscribed_events'``,\ 
              ``'syncable'``, ``'tags'``, ``'title'``, ``'tooltips'``, ``'value'``, ``'value_throttled'``, ``'visible'``, ``'width'``,\ 

        * - ``Widget_type.rangeSlider``
          - allowed
          - .. line-block::
              ``'start'``, ``'end'``,\ 
              ``'value'``, ``'step'``\ 
          - .. line-block::
              ``'title'``, ``'format'``,\ 
              ``'orientation'``, \ 
              ``'show_value'``, ``'bar_color'``\ 
          - .. line-block::
              ``'align'``, ``'aspect_ratio'``, ``'background'``, ``'bar_color'``, ``'css_classes'``, ``'default_size'``, ``'width_policy'``\ 
              ``'direction'``, ``'disabled'``, ``'end'``, ``'format'``, ``'height'``, ``'height_policy'``, ``'js_event_callbacks'``,\ 
              ``'js_property_callbacks'``, ``'margin'``, ``'max_height'``, ``'max_width'``, ``'min_height'``, ``'min_width'``,\ 
              ``'name'``, ``'orientation'``, ``'show_value'``, ``'sizing_mode'``, ``'start'``, ``'step'``, ``'subscribed_events'``,\ 
              ``'syncable'``, ``'tags'``, ``'title'``, ``'tooltips'``, ``'value'``, ``'value_throttled'``, ``'visible'``, ``'width'``,\         

    .. note:: To see detailed examples of all widget_types, please refer to ..
        To learn more about original bokeh widgets, please refer to ..

    .. code-block:: python
        :caption: example in Clustering_with_Scanpy

        def init_extension(self): # don't modify this
            #customize you widgets
            sc_cluster_step1_arg = {'label': 'Step1: Run PCA', 'button_type': 'success'}
            sc_cluster_step1 = make_widget(Widget_type.button, lambda : self.pca(), **sc_cluster_step1_arg)
            cl_input1 = make_widget(Widget_type.text, title = 'Neighbor Num:', value = '10')
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

    Then, add customized widgets into ``self.widgets_dict`` in ``init_extension``.

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
     
    .. note::
        1. Callback functions are designed to be asynchronous for safety. Don't modify the framework, but feel free to add parameters.
        2. scPantheon supports global data ``dt.adata`` with ``dt.adata.obsm`` of type pandas Dataframe. You can change it to other data types if necessary. 
        3. Remember to change it back or format newly generated obsms back to pandas Dataframe type by ``dt.init_data(dt.adata, obsm_name)``.  
        4. Call ``super().update_tab(new_obsm, new_map, new_group)`` to update layout. This function also formats ``new_obsm`` back to pandas Dataframe type.

    .. tip::
        .. line-block::
            For more information of parameters in ``dt.init_data``, please refer to :py:func:`~scpantheon.data.init_data`
            For more information of parameters in ``update_tab``, please refer to :func:`scpantheon.widgets.update_tab`

    .. code-block:: python
        :caption: callback example 1: ``pca``

        def pca(self):
            tb.mute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
            def next_pca(self):

                # Define callback function for customized widgets here. 
                # If more parameters are needed, add them in "def pca(self)" and "def next_pca(self)"
                # Use scPantheon global data instance "dt.adata" for functions that require anndata inputs.
                sc.tl.pca(dt.adata, svd_solver='arpack')

                # A new map(coordinate system) 'X_pca' is generated in anndata.obsm. 
                # It's necessary to call dt.init_data with the key of the generated obsm ('X_pca').
                # It formats the obsm into pd.Dataframe, which supports clustering operations in scPantheon.
                dt.init_data(dt.adata, 'X_pca')

                # If you want to display other widgets in callback functions, it's also feasible to add customed widgets here.
                sc.pl.pca_variance_ratio(dt.adata, log=True)
                img = open('figures/pca_variance_ratio.png','rb')
                img_base64 = base64.b64encode(img.read()).decode("ascii")
                pca_img = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(img_base64))
                widgets_dict = {'pca_img': pca_img}
                self.widgets_dict = {**self.widgets_dict, **widgets_dict}
                
                # Update visualization. Only change the parameters.
                super().update_tab(new_map = 'X_pca' )
                tb.unmute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
            curdoc().add_next_tick_callback(lambda: next_pca(self))
    
    .. code-block:: python
        :caption: callback example 2: ``neighborhood_graph``

        def neighborhood_graph(self, neighbor_num, pc_num, resolution):
            tb.mute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets) # don't modify this
            def next_neighborhood_graph(self, neighbor_num, pc_num, resolution):
                
                # The type of dt.adata.obsm is pd.Dataframe by default. 
                # Format dt.adata.obsm if necessary in following operations
                dt.adata.obsm['X_pca'] = dt.adata.obsm['X_pca'].to_numpy()

                # main operations in callback function
                sc.pp.neighbors(dt.adata, n_neighbors=int(neighbor_num), n_pcs=int(pc_num))
                sc.tl.umap(dt.adata)
                sc.tl.leiden(dt.adata, resolution=float(resolution), flavor="igraph", n_iterations=2, directed=False)

                # Update visualization. Only change the parameters.
                super().update_tab(new_obsm = 'X_umap', new_map = 'X_umap', new_group = 'leiden')

                tb.unmute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets) # Don't modify this
            curdoc().add_next_tick_callback(lambda: next_neighborhood_graph(self, neighbor_num, pc_num, resolution)) 

    * create layout
     
    .. code-block:: python

        def update_layout(self):
            super().update_layout() # don't modify this

            # column(list) arrange widgets or layouts in a column. row(list) arrange widgets or layouts in a row.
            # Customize your own layout by calling the keys in self.widgets_dict

            sccluster_key = ['sc_cluster_step1', 'cl_input1', 'cl_input2', 'cl_input3', 'sc_cluster_step2']
            values = [self.widgets_dict[key] for key in sccluster_key if key in self.widgets_dict]
            layout_sccluster = column(values)

            pca_img_key = ['pca_img']
            values = [self.widgets_dict[key] for key in pca_img_key if key in self.widgets_dict]
            layout_pca_img = column(values)

            # Merge it with basic layout with format self.layout = column([self.layout, _____ ])
            self.layout = column([self.layout, row([layout_sccluster, layout_pca_img])])
    