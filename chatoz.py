import flet

# define a Message class
class Message():
    def __init__(self, user: str, text: str, message_type: str):
        self.user = user
        self.text = text
        self.message_type = message_type

# define a class Chat
class Chat(flet.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment="start"
        self.controls=[
            flet.CircleAvatar(
                content=flet.Text(self.getInitials(message.user)),
                color=flet.colors.WHITE,
                bgcolor=self.getAvatarColor(message.user),
            ),
            flet.Column(
                [
                    flet.Text(message.user, weight="bold"),
                    flet.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
        ]
    
    def getInitials(self, username: str):
        if username:
            return username[:1].capitalize()
        else:
            return "Unknown Chatoz"
    
    def getAvatarColor(self, username: str):
        colors_lookup = [
            flet.colors.AMBER,
            flet.colors.BROWN,
            flet.colors.CYAN,
            flet.colors.BLUE,
            flet.colors.INDIGO,
            flet.colors.LIME,
            flet.colors.GREEN,
            flet.colors.PURPLE,
            flet.colors.ORANGE,
            flet.colors.PINK,
            flet.colors.TEAL,
            flet.colors.YELLOW,
            flet.colors.RED,
        ]
        return colors_lookup[hash(username) % len(colors_lookup)]

def main(page: flet.Page):
    # title
    page.horizontal_alignment = "stretch"
    page.title = "Chatoz Chat ~ made by d33pster"
    
    # define join_chatoz fucntion
    def join_chatoz(e):
        if not username.value:
            username.error_text = "Username cannot be blank!"
            username.update()
        else:
            page.session.set("username", username.value)
            page.dialog.open = False
            new_text.prefix = flet.Text(f"{username.value}: ")
            page.pubsub.send_all(Message(user=username.value, text=f"{username.value} has joined the chat.", message_type="login"))
            page.update()
    
    # define another function for button
    def send(e):
        if new_text.value != "":
            # format using the on_message function
            page.pubsub.send_all(Message(user=page.session.get('username'), text=new_text.value, message_type="chat"))
            # reset the textfield
            new_text.value = ""
            # update the page
            page.update()
    
    # define a function to show which user texted
    def on_message(message: Message):
        if message.message_type == "chat":
            m = Chat(message=message)
        elif message.message_type == "login":
            m = flet.Text(message.text, italic=True, color=flet.colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()
    
    # use pubsub sub-module for synchronizing texts
    page.pubsub.subscribe(on_message)
    
    # welcome dialog ~ input username
    username = flet.TextField(
        label="Enter your username to join Chatoz",
        autocorrect=True,
        on_submit=join_chatoz,
    )
    
    # make a dialog
    page.dialog = flet.AlertDialog(
        open=True,
        modal=True,
        title=flet.Text("Welcome to Chatoz!"),
        content=flet.Column([username], tight=True),
        actions=[flet.ElevatedButton(text="Join Chatoz", on_click=join_chatoz)],
        actions_alignment="end",
    )
    
    # Columns contains all the chats ~ Vertically ==> update ==> changed to listView
    chat = flet.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )
    
    # for new texts
    new_text = flet.TextField(
        hint_text="What ya thinkin...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send,
    )
    
    # add all these in the screen ==> updated this with iconbutton and Container
    page.add(
        flet.Container(
            content=chat,
            border=flet.border.all(1, flet.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        flet.Row(
            [
                new_text,
                flet.IconButton(
                    icon=flet.icons.AIRLINES_ROUNDED,
                    tooltip="Chatoz",
                    on_click=send,
                ),
            ]
        ),
    )
    
    
# activate
flet.app(port=8550, target=main, view=flet.WEB_BROWSER)