import gradio as gr
from chain import run_rag_chain, run_feedback_chain
from database import update_vdb

def run_click_ui():
    return gr.update(interactive=False), gr.update(interactive=False), gr.update(visible=True)

def run_click(title, content):
    #db = update_vdb(keywords)
    response = run_rag_chain(title, content)
    return gr.update(value=response, visible=True), gr.update(visible=False), gr.update(visible=True), gr.update(value="", visible=True), gr.update(visible=True)

def new_click():
    return gr.update(value="", interactive=True), gr.update(value="", interactive=True), gr.update(value="", visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(value="", visible=False), gr.update(visible=False)

def feedback_click(title, content, response, feedback):
    # todo: user title, content
    response = run_feedback_chain(response, feedback)
    return response

with gr.Blocks() as demo:
    name=gr.Markdown("# SEO-agent")
    description=gr.Markdown("We will boost SEO!")

    title = gr.Textbox(label="제목")
    content = gr.Textbox(label="내용")
    response = gr.Textbox(label="추천 내용", interactive=False, visible=False)
    run_btn = gr.Button("Run")

    new_btn = gr.Button("New Try", visible=False)

    feedback = gr.Textbox(label="피드백", visible=False)
    feedback_btn = gr.Button("Run with Feedback", visible=False)

    run_btn.click(fn=run_click_ui, outputs=[title, content, response])
    run_btn.click(fn=run_click, inputs=[title, content], outputs=[response, run_btn, new_btn, feedback, feedback_btn])
    new_btn.click(fn=new_click, outputs=[title, content, response, run_btn, new_btn, feedback, feedback_btn])
    feedback_btn.click(fn=feedback_click, inputs=[title, content, response, feedback], outputs=[response])


demo.queue().launch(share=True)