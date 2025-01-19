.. _Widget_type:

Widget_type
===========

.. class:: Widget_type

    .. class:: Widget_type.div 

        An alias of `Div <https://docs.bokeh.org/en/2.4.3/docs/reference/models/widgets/markups.html?highlight=div#bokeh.models.Div>`_

        .. data:: text
            :type: str
            :value: ''
            :canonical: div.text

            **necessary_param**, the text or HTML contents of the widget.

        .. data:: disable_math
            :type: bool
            :value: False
            :canonical: div.disable_math
            
            **core_param**, whether the contents should not be processed as TeX/LaTeX input.

    .. class:: Widget_type.text

        An alias of `TextInput <https://docs.bokeh.org/en/2.4.3/docs/reference/models/widgets/inputs.html?highlight=textinput#textinput>`_

        .. data:: title
            :type: str
            :value: ''
            :canonical: text.title

            **core_param**, label of the widget.

        .. data:: value
            :type: str
            :value: ''
            :canonical: text.value

            **core_param**, initial or entered text value.
            Change events are triggered whenever <enter> is pressed.

        .. note::
            Although bokeh also provides parameter ``value_input`` that corresponds with change events triggered whenever any update happens (i.e. on every keypress), 
            we only support change events triggered whenever <enter> is pressed by parameter text.value. You are not recommended to use the parameter ``value_input``

    .. class:: Widget_type.button

        An alias of `Button <https://docs.bokeh.org/en/2.4.3/docs/reference/models/widgets/buttons.html?highlight=button#button>`_

        .. data:: label
            :type: str
            :value: 'Button'
            :canonical: button.label

            **core_param**, the text label for the button to display.

    .. class:: Widget_type.select

        An alias of `Select <https://docs.bokeh.org/en/2.4.3/docs/reference/models/widgets/inputs.html?highlight=select#select>`_

        .. data:: options
            :type: Either(List, Dict(String, List))
            :value: []
            :canonical: select.options

            **necessary_param**, Available selection options. Options may be provided either as a list of possible string values, or as a list of tuples, each of the form (``value``, ``label``). In the latter case, the visible widget text for each value will be corresponding given label. Option groupings can be provided by supplying a dictionary object whose values are in the aforementioned list format.
        
        .. data:: value
            :type: str
            :value: ''
            :canonical: select.value

            **core_param**, the inited or selected value.

        .. data:: title
            :type: str
            :value: ''
            :canonical: select.title

            **core_param**, widget's label to display.

    .. class:: Widget_type.autocompleteInput

        An alias of `AutocompleteInput <https://docs.bokeh.org/en/2.4.3/docs/reference/models/widgets/inputs.html?highlight=select#autocompleteinput>`_

        .. data:: completions
            :type: List
            :value: []
            :canonical: autocompleteInput.completions

            **necessary_param**, A list of completion strings. This will be used to guide the user upon typing the beginning of a desired value.
        
        .. data:: min_characters
            :type: PositiveInt
            :value: 2
            :canonical: autocompleteInput.min_characters

            **core_param**, The number of characters a user must type before completions are presented.
        
        .. data:: case_sensitive
            :type: bool
            :value: True
            :canonical: autocompleteInput.case_sensitive

            **core_param**, Enable or disable case sensitivity.
        
        .. data:: title
            :type: str
            :value: ''
            :canonical: autocompleteInput.title

            **core_param**, widget's label to display.

        .. data:: value
            :type: str
            :value: ''
            :canonical: autocompleteInput.value

            **core_param**, Initial or entered text value.
            Change events are triggered whenever <enter> is pressed.

        .. note::
            Although bokeh also provides parameter ``value_input`` that corresponds with change events triggered whenever any update happens (i.e. on every keypress), 
            we only support change events triggered whenever <enter> is pressed by parameter text.value. You are not recommended to use the parameter ``value_input``

    .. class:: Widget_type.checkBoxGroup
        
        An alias of `CheckboxGroup <https://docs.bokeh.org/en/2.4.3/docs/reference/models/widgets/groups.html?highlight=checkboxgroup#checkboxgroup>`_

        .. data:: labels
            :type: List
            :value: []
            :canonical: checkBoxGroup.labels

            **necessary_param**, list of text labels contained in this group.

        .. data:: active
            :type: List
            :value: []
            :canonical: checkBoxGroup.active

            **core_param**, the list of indices of selected check boxes.

    .. class:: Widget_type.radioButtonGroup

        An alias of `RadioButtonGroup <https://docs.bokeh.org/en/2.4.3/docs/reference/models/widgets/groups.html#radiobuttongroup>`_
        
        .. data:: labels
            :type: List
            :value: []
            :canonical: radioButtonGroup.labels

            **necessary_param**, list of text labels contained in this group.

        .. data:: active
            :type: Nullable(Int)
            :value: []
            :canonical: radioButtonGroup.active

            **core_param**, the index of the selected radio box, or None if nothing is selected.


    .. class:: Widget_type.slider
        
        An alias of `Slider <https://docs.bokeh.org/en/2.4.3/docs/reference/models/widgets/sliders.html?highlight=slider#slider>`_
        
        .. data:: start
            :type: NonNullable(Float)
            :value: Undefined
            :canonical: Slider.start

            **necessary_param**, the minimum allowable value.

        .. data:: end
            :type: NonNullable(Float)
            :value: Undefined
            :canonical: Slider.end

            **necessary_param**, the maximum allowable value.
        
        .. data:: value
            :type: NonNullable(Float)
            :value: Undefined
            :canonical: Slider.value

            **necessary_param**, Initial or selected value.

        .. data:: step
            :type: Float
            :value: 1
            :canonical: Slider.active

            **necessary_param**, the step between consecutive values.
        
        .. data:: title
            :type: Nullable(String)
            :value: ''
            :canonical: Slider.title

            **core_param**, label of Slider.
        
        .. data:: show_value
            :type: bool
            :value: True
            :canonical: Slider.show_value

            **core_param**, whether or not show slider's value..

        .. data:: format
            :type: Either(String, Instance(TickFormatter))
            :value: '0[.]00'
            :canonical: Slider.format

            **core_param**, format of value display.
        
        .. data:: orientation
            :type: Enum(Enumeration(horizontal, vertical))
            :value: 'horizontal'
            :canonical: Slider.orientation

            **core_param**, orient the slider either horizontally (default) or vertically.
        
        .. data:: bar_color
            :type: Color
            :value: '#e6e6e6'
            :canonical: Slider.bar_color

            **core_param**, color of the range bar. Acceptable values are:

            .. line-block::
                1. any of the named CSS colors, e.g ``'green'``, ``'indigo'``
                2. RGB(A) hex strings, e.g., ``'#FF0000'``, ``'#44444444'``
                3. CSS4 color strings, e.g., ``'rgba(255, 0, 127, 0.6)'``, ``'rgb(0 127 0 / 1.0)'``, or ``'hsl(60deg 100% 50% / 1.0)'``
                4. a 3-tuple of integers (r, g, b) between 0 and 255
                5. a 4-tuple of (r, g, b, a) where r, g, b are integers between 0 and 255, and a is between 0 and 1
                6. a 32-bit unsigned integer using the 0xRRGGBBAA byte order pattern.
                 
    
    .. class:: Widget_type.rangeSlider

        An alias of `RangeSlider <https://docs.bokeh.org/en/2.4.3/docs/reference/models/widgets/sliders.html?highlight=slider#rangeslider>`_
        
        .. data:: start
            :type: NonNullable(Float)
            :value: Undefined
            :canonical: rangeSlider.start

            **necessary_param**, the minimum allowable value.

        .. data:: end
            :type: NonNullable(Float)
            :value: Undefined
            :canonical: rangeSlider.end

            **necessary_param**, the maximum allowable value.
        
        .. data:: value
            :type: NonNullable(Tuple(Float, Float))
            :value: Undefined
            :canonical: rangeSlider.value

            **necessary_param**, Initial or selected range.

        .. data:: step
            :type: Float
            :value: 1
            :canonical: rangeSlider.active

            **necessary_param**, the step between consecutive values.
        
        .. data:: title
            :type: Nullable(String)
            :value: ''
            :canonical: rangeSlider.title

            **core_param**, label of rangeSlider.
        
        .. data:: show_value
            :type: bool
            :value: True
            :canonical: rangeSlider.show_value

            **core_param**, whether or not show slider's value..

        .. data:: format
            :type: Either(String, Instance(TickFormatter))
            :value: '0[.]00'
            :canonical: rangeSlider.format

            **core_param**, format of value display.
        
        .. data:: orientation
            :type: Enum(Enumeration(horizontal, vertical))
            :value: 'horizontal'
            :canonical: rangeSlider.orientation

            **core_param**, orient the slider either horizontally (default) or vertically.
        
        .. data:: bar_color
            :type: Color
            :value: '#e6e6e6'
            :canonical: rangeSlider.bar_color

            **core_param**, color of the range bar. Acceptable values are:

            .. line-block::
                1. any of the named CSS colors, e.g ``'green'``, ``'indigo'``
                2. RGB(A) hex strings, e.g., ``'#FF0000'``, ``'#44444444'``
                3. CSS4 color strings, e.g., ``'rgba(255, 0, 127, 0.6)'``, ``'rgb(0 127 0 / 1.0)'``, or ``'hsl(60deg 100% 50% / 1.0)'``
                4. a 3-tuple of integers (r, g, b) between 0 and 255
                5. a 4-tuple of (r, g, b, a) where r, g, b are integers between 0 and 255, and a is between 0 and 1
                6. a 32-bit unsigned integer using the 0xRRGGBBAA byte order pattern.