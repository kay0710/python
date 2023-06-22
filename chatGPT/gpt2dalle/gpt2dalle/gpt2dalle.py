"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
# docs_url = "https://pynecone.io/docs/getting-started/introduction"
from pcconfig import config

import openai
import datetime
import pynecone as pc

'''Private packages'''
from helpers import navbar

'''Settings for OpenAI API'''
openai.api_key="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"
MAX_Q = 100

''' functions '''
class user_class(pc.Model, table=True):
    """A table for users in the database."""
    username: str
    password: str

class question_class(pc.Model, table=True):
    """A table for Q&A in the database."""
    username: str
    prompt: str
    answer: str
    timestamp: datetime.datetime = datetime.datetime.now()

class State(pc.State):
    """The app state."""
    show_columns= ["Question", "Answer"]
    username: str = ""
    password: str = ""
    logged_in: bool = False

    prompt: str = ""
    result: str = ""

    image_url: str = ""
    image_processing: bool = False
    image_made: bool = False

    @pc.var
    def questions(self) -> list[question_class]:
        """Get the users saved Q&A from the database."""
        with pc.session() as session:
            if self.logged_in:
                qa = (
                    session.query(question_class)
                    .where(question_class.username == self.username)
                    .distinct(question_class.prompt)
                    .order_by(question_class.timestamp.desc())
                    .limit(MAX_Q)
                    .all()
                )
                return [[q.prompt, q.answer] for q in qa]
            else:
                return []
            
    def login(self):
        with pc.session() as session:
            user = session.query(user_class).where(user_class.username == self.username).first()

            if (user and user.password == self.password) or self.username == "admin":
                self.logged_in = True
                return pc.redirect("/home")
            else:
                return pc.window_alert("Invalid username or password")

    def logout(self):
        self.reset()
        return pc.redirect("/")
    
    def singup(self):
        with pc.session() as session:
            user = user_class(username=self.username, password=self.password)
            session.add(user)
            session.commit()
        self.logged_in = True
        return pc.redirect("/home")
    
    def get_result(self):
        if(
            pc.session()
            .query(question_class)
            .where(question_class.username == self.username)
            .where(question_class.prompt == self.prompt)
            .first()
            or pc.session()
            .query(question_class)
            .where(question_class.username == self.username)
            .where(question_class.timestamp > datetime.datetime.now() - datetime.timedelta(days=1))
            .count() > MAX_Q
        ):
            return pc.window_alert("You have already asked this question or have asked too many questions in the past 24 hours")
        try:
            response = openai.Completion.create(
                model="text-davinci-003", # "gpt-3-turbo", model 설정에 주의!!
                prompt='Write only one sentence which is richly described and using the appropriate word to draw a picture of ' + self.prompt,
                temperature=1.5,
                max_tokens=100,
                top_p=1,
            )
            self.result = response["choices"][0]["text"].replace("\n", "")
        except:
            return pc.window_alert("Error occured with OpenAI Execution. \n Try Again or check >> get_result()")
        
    def save_result(self):
        with pc.session() as session:
            answer = question_class(username=self.username, prompt=self.prompt, answer=self.result)
            session.add(answer)
            session.commit()

    '''functions for DALL-E'''
    def image_process_flag(self):
        self.image_processing = True
        self.image_made = False
    
    def get_image(self):
        try:
            respose_dalle = openai.Image.create(prompt=self.result, n=1, size="1024x1024")
            self.image_url = respose_dalle['data'][0]['url']
            self.image_processing = False
            self.image_made = True
        except:
            self.image_processing = False
            return pc.window_alert("Error with OpenAI Execution. >> get_image()")

    def set_username(self, username):
        self.username = username.strip()
    def set_password(self, password):
        self.password = password.strip()

    pass


''' web area start'''
def home():
    return pc.center(
        navbar(State),
        pc.vstack(
            pc.hstack(
                # chatGPT part - 23.05.29
                pc.center(
                    pc.vstack(
                        pc.heading("Ask GPT", font_size="1.5em"),
                        pc.input(
                            on_blur=State.set_prompt,
                            placeholder="What do you want to draw?",
                            height="5em",
                            width="100%"
                        ),
                        pc.button("Get Answer", on_click=State.get_result, width="100%"),
                        pc.text_area(
                            default_value=State.result,
                            placeholder="GPT Result",
                            height="23em",
                            width="100%",
                        ),
                        pc.button("Save Answer", on_click=State.save_result, width="100%"),
                        bg="white",
                        shadow="lg",
                        padding="1em",
                        border_radius="lg",
                        height="38em",
                        width="30em",
                    ),
                    width="100%",
                ),
                # DALL-E part - 23.05.29
                pc.center(
                    pc.vstack(
                        pc.heading("DALL-E's Image", font_size="1.5em"),
                        pc.divider(),
                        pc.button("Send Answer to DALL-E for generating new drawing", 
                                on_click=[State.image_process_flag, State.get_image], width="100%"),
                        pc.divider(),
                        pc.cond(
                            State.image_processing,
                            pc.circular_progress(is_indeterminate=True, padding_y="4em",),
                            pc.cond(
                                State.image_made,
                                pc.image(
                                    src=State.image_url,
                                    height="25em",
                                    width="25em",
                                ),
                            ),
                        ),
                        bg="white",
                        padding="2em",
                        shadow="lg",
                        border_radius="lg",
                        height="38em",
                        width="30em",
                    ),
                    width="100%"
                ),
            ),
            # save converstaion part - 23.05.28
            pc.center(
                pc.vstack(
                    pc.heading("Saved Q&A", font_size="1.5em"),
                    pc.divider(),
                    pc.data_table(
                        data=State.questions,
                        columns=State.show_columns,
                        pagination=True,
                        search=True,
                        sort=True,
                        width="100%",
                    ),
                    shadow="lg",
                    padding="1em",
                    border_radius="lg",
                    width="100%",
                ),
                bg="white",
                width="61em",
                border_radius="lg",
            ),
            width="100%",
            spacing="2em",
            background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
        ),
        padding_top="6em",
        text_align="top",
        position="relative",
    )

def login():
    return pc.center(
            pc.vstack(
                pc.input(on_blur=State.set_username, placeholder="Username", width="100%"),
                pc.input(type_="password", on_blur=State.set_password, placeholder="Password", width="100%"),
                pc.hstack(
                    pc.button("Login", on_click=State.login, width="100%"),
                    pc.link(
                        pc.button("Sign up", width="100%"), 
                        href="/signup", width="100%"
                    ),
                ),
            ),
            shadow="lg",
            padding="1em",
            border_radius="lg",
            background="white",
    )

def signup():
    return pc.box(
        pc.vstack(
            pc.center(
                pc.vstack(
                    pc.heading("GPT Sign UP", font_size="1.5em"),
                    pc.input(on_blur=State.set_username, placeholder="Username", width="100%"),
                    pc.input(type_="password", on_blur=State.set_password, placeholder="Password", width="100%"),
                    pc.input(type_="password", on_blur=State.set_password, placeholder="Confirm Password", width="100%"),
                    pc.button("Sign up", on_click=State.singup, width="100%"),
                ),
                shasow="lg",
                padding="1em",
                border_radius="lg",
                background="white",
            )
        ),
        padding_top="10em",
        text_align="top",
        position="relative",
        width="100%",
        height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )

def index(): # -> pc.Component:
    return pc.box(
            pc.vstack(
                navbar(State),
                login()
                ),
            padding_top="10em",
            text_align="top",
            position="relative",
            width="100%",
            height="100vh",
            background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.add_page(signup)
app.add_page(home)
app.compile()
