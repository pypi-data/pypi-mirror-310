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
        outputs=[page_display, size_display, total_display, options_display]
    )
    page_display.change(fn=rerender_pagination_page, inputs=page_display, outputs=pagination_component)
    size_display.change(fn=rerender_pagination_size, inputs=size_display, outputs=pagination_component)
    total_display.change(fn=rerender_pagination_total, inputs=total_display, outputs=pagination_component)
    options_display.change(fn=rerender_pagination_size_options, inputs=options_display, outputs=pagination_component)

if __name__ == "__main__":
    demo.launch()
