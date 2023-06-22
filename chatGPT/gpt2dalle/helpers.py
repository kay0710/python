import pynecone as pc

def navbar(State):
    return pc.box(
        pc.hstack(
            pc.link(
                pc.hstack(
                    pc.image(src="favicon.ico"), 
                    pc.heading("GPT to DALL-E by Kay", font_size="2em")), href="/"
            ),
            pc.menu(
                pc.menu_button(
                    pc.cond(
                        State.logged_in,
                        pc.avatar(name=State.username, size="md"),
                        pc.box(),
                    )
                ),
                pc.menu_list(
                    pc.center(
                        pc.vstack(
                            pc.avatar(name=State.username, size="md"),
                            pc.text(State.username),
                        )
                    ),
                    pc.menu_divider(),
                    pc.link(pc.menu_item("About GPT"), href="https://openai.com/blog/chatgpt"),
                    pc.link(pc.menu_item("About DALL-E"), href="https://openai.com/product/dall-e-2"),
                    pc.link(pc.menu_item("Sign Out"), on_click=State.logout),
                ),
            ),
            justify="space-between",
            border_bottom="0.2em soild #F0F0F0",
            padding_x="2em",
            padding_y="1em",
            bd="rgba(255,255,255, 0.90)",
        ),
        position="fixed",
        width="100%",
        top="0px",
        z_index="500",
    )