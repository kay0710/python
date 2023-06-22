from pcconfig import config
import pynecone as pc

import openai
import openai_class
from openai_class import kay_settings

# docs_url = "https://pynecone.io/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"

openai_class.set_API_KEY(kay_settings['OPENAI_API_KEY'])

class State(pc.State):
    prompt = ""
    img_url = ""
    img_flag = False
    
    def send_prompt(self, input):
        self.prompt = openai_class.askGPT(input)
    
    def make_img(self):
        self.img_url = openai_class.askDALL_E(self.prompt)
        self.img_flag = True
    
    pass

def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            pc.heading(
                "Pynecone Test page",
                font_size="2em"
            ),
            pc.box(
                "Hello from kay ", font_size="1em"
            ),
            pc.input(
                placeholder="Enter a object..",
                on_blur=State.set_prompt
            ),
            pc.button(
                "Get Image",
                one_click=[State.img_flag, State.make_img],
                width="100%"
            ),
            pc.cond(
                State.img_flag,
                pc.image(
                    src=State.img_url,
                    height="25em",
                    width="25em"
                ),
            ),
            # pc.link(
            #     "Check out our docs!",
            #     href=State.img_url,
            #     border="0.1em solid",
            #     padding="0.5em",
            #     border_radius="0.5em",
            #     _hover={
            #         "color": "rgb(107,99,246)",
            #     },
            # ),
            spacing="1.5em",
            font_size="2em",
            
        ),
        padding_top="10%",
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
