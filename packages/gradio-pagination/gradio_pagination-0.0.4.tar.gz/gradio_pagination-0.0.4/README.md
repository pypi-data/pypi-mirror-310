---
tags: [gradio-custom-component, SimpleTextbox, gradio pagination]
title: gradio_pagination
short_description: pagination component
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

# `gradio_pagination`
<a href="https://pypi.org/project/gradio_pagination/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_pagination"></a>  

pagination component

## Installation

```bash
pip install gradio_pagination
```

## Usage

```python
import json

import gradio as gr
from gradio_pagination import pagination

total=10000
current_page = 1
page_size = 10
page_size_options = [10, 20, 30, 50, 300]

def rerender_pagination_total(total_num):
    global total, page_size, current_page, page_size_options
    total = int(total_num)
    current_page = 1 # If the total number changes, whether to reset the current page to 1 depends on your business logic.
    print('overide total to ', total)
    return json.dumps({
        "total": int(total),
        "page": int(current_page),
        "page_size": int(page_size),
        "page_size_options": page_size_options,
    })

def rerender_pagination_page(page):
    global total, page_size, current_page, page_size_options
    current_page = int(page)
    print('overide current_page to ', current_page)
    return json.dumps({
        "total": int(total),
        "page": int(current_page),
        "page_size": int(page_size),
        "page_size_options": page_size_options,
    })

def rerender_pagination_size(size):
    global total, page_size, current_page, page_size_options
    page_size = int(size)
    print('overide page_size to ', page_size)
    return json.dumps({
        "total": int(total),
        "page": int(current_page),
        "page_size": int(page_size),
        "page_size_options": page_size_options,
    })

def rerender_pagination_size_options(options: str):
    global total, page_size, current_page, page_size_options
    try:
        page_size_options = list(map(int, options.split(',')))
        print('overide page_size_options to ', page_size_options)
    except ValueError as e:
        print(f"{e}, the options str is: {options}")
    return json.dumps({
        "total": int(total),
        "page": int(current_page),
        "page_size": int(page_size),
        "page_size_options": page_size_options,
    })

def show_page_info_into_text_box(data):
    global total, page_size, current_page, page_size_options
    current_page = data.page
    page_size = data.page_size
    total = data.total
    page_size_options = data.page_size_options
    print('pagination change: ', data)
    return str(current_page), str(page_size), str(total), ",".join(map(str, sorted(page_size_options)))

with gr.Blocks() as demo:
    gr.Markdown("## Pagination Demo")
    pagination_component = pagination(total=total, page=1, page_size=10, page_size_options=page_size_options)

    with gr.Row():
        page_display = gr.Textbox(label="Current Page", value=str(current_page), interactive=True)
        size_display = gr.Textbox(label="Page Size", value=str(page_size), interactive=True)
        total_display = gr.Textbox(label="Total", value=str(total), interactive=True)
        options_display = gr.Textbox(label="Page Size Options", value=str(",".join(map(str, page_size_options))), interactive=True)

    pagination_component.change(
        fn=show_page_info_into_text_box,
        inputs=pagination_component,
        outputs=[page_display, size_display, total_display]
    )
    page_display.change(fn=rerender_pagination_page, inputs=page_display, outputs=pagination_component)
    size_display.change(fn=rerender_pagination_size, inputs=size_display, outputs=pagination_component)
    total_display.change(fn=rerender_pagination_total, inputs=total_display, outputs=pagination_component)
    options_display.change(fn=rerender_pagination_size_options, inputs=options_display, outputs=pagination_component)

if __name__ == "__main__":
    demo.launch()

```

## `pagination`

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>value</code></td>
<td align="left" style="width: 25%;">

```python
str | Callable | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>placeholder</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>every</code></td>
<td align="left" style="width: 25%;">

```python
Timer | float | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>inputs</code></td>
<td align="left" style="width: 25%;">

```python
Component | Sequence[Component] | set[Component] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>show_label</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>160</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>rtl</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>False</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>key</code></td>
<td align="left" style="width: 25%;">

```python
int | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>total</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>0</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>page</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>1</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>page_size</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>10</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>page_size_options</code></td>
<td align="left" style="width: 25%;">

```python
list[int] | None
```

</td>
<td align="left"><code>[10, 20, 50, 100]</code></td>
<td align="left">None</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `change` | Triggered when the value of the pagination changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input. |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, str | None: Returns a namespace object representing the pagination state.


 ```python
 def predict(
     value: str | None
 ) -> str | None:
     return value
 ```
 
