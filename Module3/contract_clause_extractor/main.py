import gradio as gr

from app.clause_service import extract_contract_clauses,load_sample_nda_text

def main():
    with gr.Blocks() as demo:

        gr.Markdown(
            """
# Contract Clause Extractor

Upload a contract **PDF/TXT** or paste text, then extract structured clauses into JSON.

**Clause types:** termination, liability, payment, confidentiality, governing law, other

Guardrails check file type and contract length before calling the LLM.
"""
        )
        with gr.Row():
            with gr.Column():
                file_input = gr.File(
                    label="Upload Contract (PDF/TXT)",
                    file_types=[".pdf", ".txt"],
                    type="filepath",
                )

                text_input = gr.Textbox(
                    label="Or paste text",
                    placeholder="Paste your contract text here...",
                    lines=10,
                )

                load_sample_button = gr.Button("Load Sample NDA")
                extract_button = gr.Button("Extract Clauses", variant="primary")

            
            with gr.Column():
                summary_output = gr.Markdown(label="Extraction Summary")
                json_output = gr.Code(label="Validated Json", language="json")
                clauses_output = gr.DataFrame(label="Clauses Table", interactive=False)

        
        load_sample_button.click(
            fn= lambda: load_sample_nda_text(),
            inputs=[],
            outputs=[text_input],
        )

        extract_button.click(
            fn= extract_contract_clauses,
            inputs=[file_input, text_input],
            outputs=[summary_output, json_output, clauses_output],
        )
    demo.launch()


if __name__ == "__main__":
    main()


    