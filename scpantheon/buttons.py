from enum import Enum
from bokeh.models import Select, Button, CheckboxGroup, TextInput, AutocompleteInput, Div, RadioButtonGroup, Slider, RangeSlider

class Widget_type(Enum):
    button = Button
    text = TextInput
    select = Select
    checkBoxGroup = CheckboxGroup
    autocompleteInput = AutocompleteInput
    div = Div
    radioButtonGroup = RadioButtonGroup
    slider = Slider
    rangeSlider = RangeSlider

def make_widget(
    widget_type: Widget_type,
    func = None, 
    **kwargs
):
    match widget_type:
        case Widget_type.div:
            necessary_param = ['text']
            core_param = ['disable_math']
            all_param = ['align', 'aspect_ratio', 'background', 'css_classes', 'default_size', 'disable_math', 
                'disabled', 'height', 'height_policy', 'js_event_callbacks', 'js_property_callbacks', 'margin', 
                'max_height', 'max_width', 'min_height', 'min_width', 'name', 'render_as_text', 'sizing_mode', 
                'style', 'subscribed_events', 'syncable', 'tags', 'text', 'visible', 'width', 'width_policy']

        case Widget_type.slider:
            necessary_param = ['start', 'end', 'value', 'step']
            core_param = ['title', 'format', 'orientation', 'show_value', 'bar_color']
            all_param = ['align', 'aspect_ratio', 'background', 'bar_color', 'css_classes', 'default_size', 
                'direction', 'disabled', 'end', 'format', 'height', 'height_policy', 'js_event_callbacks', 
                'js_property_callbacks', 'margin', 'max_height', 'max_width', 'min_height', 'min_width', 
                'name', 'orientation', 'show_value', 'sizing_mode', 'start', 'step', 'subscribed_events', 
                'syncable', 'tags', 'title', 'tooltips', 'value', 'value_throttled', 'visible', 'width', 
                'width_policy']
            change_name = 'value'
        
        case Widget_type.rangeSlider:
            necessary_param = ['start', 'end', 'value', 'step']
            core_param = ['title', 'format', 'orientation', 'show_value', 'bar_color']
            all_param = ['align', 'aspect_ratio', 'background', 'bar_color', 'css_classes', 'default_size', 
                'direction', 'disabled', 'end', 'format', 'height', 'height_policy', 'js_event_callbacks', 
                'js_property_callbacks', 'margin', 'max_height', 'max_width', 'min_height', 'min_width', 
                'name', 'orientation', 'show_value', 'sizing_mode', 'start', 'step', 'subscribed_events', 
                'syncable', 'tags', 'title', 'tooltips', 'value', 'value_throttled', 'visible', 'width', 
                'width_policy']
            change_name = 'value'

        case  Widget_type.button:
            necessary_param = []
            core_param = ['label']
            all_param = ['align', 'aspect_ratio', 'background', 'button_type', 'css_classes', 'default_size',
                'disabled', 'height', 'height_policy', 'icon', 'js_event_callbacks', 'js_property_callbacks',
                'label', 'margin', 'max_height', 'max_width', 'min_height', 'min_width', 'name', 
                'sizing_mode', 'subscribed_events', 'syncable', 'tags', 'visible', 'width', 'width_policy']
            event_name = 'button_click'

        case  Widget_type.text:
            necessary_param = []
            core_param = ['title', 'value']
            all_param = ['align', 'aspect_ratio', 'background', 'css_classes', 'default_size',
                'disabled', 'height', 'height_policy', 'js_event_callbacks', 'js_property_callbacks',
                'margin', 'max_height', 'max_length', 'max_width', 'min_height', 'min_width', 'name',
                'placeholder', 'sizing_mode', 'subscribed_events', 'syncable', 'tags', 'title', 'value',
                'value_input', 'visible', 'width', 'width_policy']
            change_name = 'value'
            
        case Widget_type.select:
            necessary_param = ['options', 'value']
            core_param = ['title']
            all_param = ['align', 'aspect_ratio', 'background', 'css_classes', 'default_size', 'disabled',
                'height', 'height_policy', 'js_event_callbacks', 'js_property_callbacks', 'margin', 
                'max_height', 'max_width', 'min_height', 'min_width', 'name', 'options', 'sizing_mode', 
                'subscribed_events', 'syncable', 'tags', 'title', 'value', 'visible', 'width', 'width_policy']
            change_name = 'value'
        
        case Widget_type.checkBoxGroup:
            necessary_param = ['labels']
            core_param = ['active']
            all_param = ['active', 'align', 'aspect_ratio', 'background', 'css_classes', 'default_size', 
                'disabled', 'height', 'height_policy', 'inline', 'js_event_callbacks', 'js_property_callbacks',
                'labels', 'margin', 'max_height', 'max_width', 'min_height', 'min_width', 'name', 'sizing_mode',
                'subscribed_events', 'syncable', 'tags', 'visible', 'width', 'width_policy']
            change_name = 'active'
        
        case Widget_type.radioButtonGroup:
            necessary_param = ['labels']
            core_param = ['active']
            all_param = ['active', 'align', 'aspect_ratio', 'background', 'button_type', 'css_classes', 
                'default_size', 'disabled', 'height', 'height_policy', 'js_event_callbacks', 
                'js_property_callbacks', 'labels', 'margin', 'max_height', 'max_width', 'min_height', 'min_width',
                'name', 'orientation', 'sizing_mode', 'subscribed_events', 'syncable', 'tags', 'visible', 'width', 
                'width_policy']
            change_name = 'active'

    kwargs = examine_args(widget_type, necessary_param, core_param, all_param, **kwargs)
    widget = widget_type.value(**kwargs)
    if func and event_name:
        widget.on_event(event_name, func)
    elif func and change_name:
        widget.on_change(change_name, func)
    return widget

def examine_args(
    widget_type: Widget_type,
    necessary_params: list,
    core_params: list,
    all_params: list,
    **kwargs
):
    print("Note: For", widget_type, "parameters", necessary_params, "must be included to function.",
        core_params, "are also useful, others may not be used")
    filtered_kwargs = {key: value for key, value in kwargs.items() if key in all_params}
    illegal_keys = set(kwargs.keys()) - set(filtered_kwargs.keys())
    if illegal_keys != set():
        print("Warning:", illegal_keys, "are not allowed parameters for", widget_type,
            "and will be ignored. All parameters allowed for", widget_type, "are", all_params)
    return filtered_kwargs