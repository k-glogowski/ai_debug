import gradio as gr

def greet(name):
    """Simple greeting function"""
    return f"Witaj, {name}! Aplikacja Gradio działa poprawnie."

# Create Gradio interface
iface = gr.Interface(
    fn=greet,
    inputs=gr.Textbox(label="Podaj swoje imię", placeholder="Wpisz imię..."),
    outputs=gr.Textbox(label="Odpowiedź"),
    title="Prosta Aplikacja Gradio",
    description="To jest prosty interfejs Gradio bez modelu ML."
)

if __name__ == "__main__":
    # Run the app - Gradio will automatically find an available port
    iface.launch(server_name="0.0.0.0", server_port=7860)
