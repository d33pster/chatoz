import flet

# define a Message class
class Message():
    def __init__(self, user: str, text: str, message_type: str):
        self.user = user
        self.text = text
        self.message_type = message_type

def main(page: flet.Page):
    # column contains all the chats ~ Vertically
    chat = flet.Column()
    # for new texts
    new_text = flet.TextField()
    # welcome dialog ~ input username
    username = flet.TextField(label="Enter your username")
    
    # define join_chatoz fucntion
    def join_chatoz(e):
        if not username.value:
            username.error_text = "Username Cannot be blank!"
            username.update()
        else:
            page.session.set("username", username.value)
            page.dialog.open = False
            page.pubsub.send_all(Message(user=username.value, text=f"{username.value} has joined the chat.", message_type="login"))
            page.update()
    
    # make a dialog
    page.dialog = flet.AlertDialog(
        open=True,
        modal=True,
        title=flet.Text("Welcome to Chatoz!"),
        content=flet.Column([username], tight=True),
        actions=[flet.ElevatedButton(text="Join Chatoz", on_click=join_chatoz)],
        actions_alignment="end",
    )
    
    # define a function to show which user texted
    def on_message(message: Message):
        if message.message_type == "chat":
            chat.controls.append(flet.Text(f"{message.user}: {message.text}"))
        elif message.message_type == "login":
            chat.controls.append(flet.Text(message.text, italic=True, color=flet.colors.BLACK45, size=12))
        page.update()
    
    # use pubsub sub-module for synchronizing texts
    page.pubsub.subscribe(on_message)
    
    # define another function for button
    def send(e):
        # format using the on_message function
        page.pubsub.send_all(Message(user=page.session.get('username'), text=new_text.value, message_type="chat"))
        # reset the textfield
        new_text.value = ""
        # update the page
        page.update()
    
    # add all these in the screen
    page.add(chat, flet.Row(controls=[new_text, flet.ElevatedButton("Chatoz", on_click=send)]))
    
# activate
flet.app(main, view=flet.AppView.WEB_BROWSER)