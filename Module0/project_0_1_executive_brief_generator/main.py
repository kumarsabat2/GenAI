import gradio as gr
from app.brief_service import generate_brief

def main():
    with gr.Blocks() as demo:
        gr.Markdown("""
        #Executive Brief Generator

       Your * first Gen AI app**
        1.Enter a topic 
        2. Paste meeting notes
        3. Click "Generate Brief"
      The LLM will generate a brief for the topic based on the meeting notes.
        """)
        topic = gr.Textbox(label="Topic", placeholder="Enter a topic",lines=1)
        source_text = gr.TextArea(label="Meeting Notes", placeholder="Paste meeting notes", lines=10)
        generate_button = gr.Button("Generate Brief",variant="primary")
        brief_output = gr.Markdown(label="Executive Brief")

        generate_button.click(generate_brief, inputs=[topic, source_text], outputs=[brief_output])

    demo.launch()
    
if __name__ == "__main__":
    main()

