from enum import Enum
from bokeh.models import Select, Button, CheckboxGroup, TextInput, ColorPicker, AutocompleteInput, ColumnDataSource, Div

class Widget_type(Enum):
    button = 'button'
    text = 'text'
    select = 'select'
    checkboxgroup = 'checkboxgroup'

def make_widget(
    widget_type: Widget_type, 
    **kwargs
):
    """
    kwargs: widget_type == "button"
    | widget_type | necessary params | core params |
    |--|--|--|
    | "button" | / | "label" |
    | "text" | / | "title", "value" |
    """
    match widget_type:
        case  Widget_type.button:
            necessary_param = []
            core_param = ['label']
            all_param = ['align', 'aspect_ratio', 'background', 'button_type', 'css_classes', 'default_size',
                'disabled', 'height', 'height_policy', 'icon', 'js_event_callbacks', 'js_property_callbacks',
                'label', 'margin', 'max_height', 'max_width', 'min_height', 'min_width', 'name', 
                'sizing_mode', 'subscribed_events', 'syncable', 'tags', 'visible', 'width', 'width_policy']
            kwargs = examine_args(widget_type, necessary_param, core_param, all_param, **kwargs)
            return Button(**kwargs)
        case  Widget_type.text:
            necessary_param = []
            core_param = ['title', 'value']
            all_param = ['align', 'aspect_ratio', 'background', 'css_classes', 'default_size',
                'disabled', 'height', 'height_policy', 'js_event_callbacks', 'js_property_callbacks',
                'margin', 'max_height', 'max_length', 'max_width', 'min_height', 'min_width', 'name',
                'placeholder', 'sizing_mode', 'subscribed_events', 'syncable', 'tags', 'title', 'value',
                'value_input', 'visible', 'width', 'width_policy']
            kwargs = examine_args(widget_type, necessary_param, core_param, all_param, **kwargs)
            return TextInput(**kwargs)
        case Widget_type.select:
            necessary_param = []
            core_param = ['options']
            all_param = ['align', 'aspect_ratio', 'background', 'css_classes', 'default_size', 'disabled',
                'height', 'height_policy', 'js_event_callbacks', 'js_property_callbacks', 'margin', 
                'max_height', 'max_width', 'min_height', 'min_width', 'name', 'options', 'sizing_mode', 
                'subscribed_events', 'syncable', 'tags', 'title', 'value', 'visible', 'width', 'width_policy']
            kwargs = examine_args(widget_type, necessary_param, core_param, all_param, **kwargs)
            return Select(**kwargs)
        case Widget_type.checkboxgroup:
            necessary_param = ['labels']
            core_param = ['active']
            all_param = ['active', 'align', 'aspect_ratio', 'background', 'css_classes', 'default_size', 
                'disabled', 'height', 'height_policy', 'inline', 'js_event_callbacks', 'js_property_callbacks',
                'labels', 'margin', 'max_height', 'max_width', 'min_height', 'min_width', 'name', 'sizing_mode',
                'subscribed_events', 'syncable', 'tags', 'visible', 'width', 'width_policy']
            kwargs = examine_args(widget_type, necessary_param, core_param, all_param, **kwargs)
            return CheckboxGroup(**kwargs)

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