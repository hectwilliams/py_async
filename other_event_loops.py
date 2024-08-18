"""
    Combine asynico evemt loop with another event loop
    Tinkter event loop and asyncio event will be interoperability

Common Tkinter Events:

<Button-1>	
    Button 1 is the leftmost button, button 2 is the middle button(where available), and button 3 the rightmost button. <Button-1>, <ButtonPress-1>, and <1> are all synonyms.
<B1-Motion>	
    The mouse is moved, with mouse button 1 being held down (use B2 for the middle button, B3 for the right button).
<ButtonRelease-1>	
    Button 1 was released. This is probably a better choice in most cases than the Button event, because if the user accidentally presses the button, they can move the mouse off the widget to avoid setting off the event.
<Double-Button-1>	
    Button 1 was double clicked. You can use Double or Triple as prefixes.
<Enter>	
    The mouse pointer entered the widget (this event doesn't mean that the user pressed the Enter key!).
<Leave>	
    The mouse pointer left the widget.
<FocusIn>	
    Keyboard focus was moved to this widget, or to a child of this widget.
<FocusOut>	
    Keyboard focus was moved from this widget to another widget.
<Return>	
    The user pressed the Enter key. For an ordinary 102-key PC-style keyboard, the special keys are Cancel (the Break key), BackSpace, Tab, Return(the Enter key), Shift_L (any Shift key), Control_L (any Control key), Alt_L (any Alt key), Pause, Caps_Lock, Escape, Prior (Page Up), Next (Page Down), End, Home, Left, Up, Right, Down, Print, Insert, Delete, F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, Num_Lock, and Scroll_Lock.
<Key>	
    The user pressed any key. The key is provided in the char member of the event object passed to the callback (this is an empty string for special keys).
a	
    The user typed an "a". Most printable characters can be used as is. The exceptions are space (<space>) and less than (<less>). Note that 1 is a keyboard binding, while <1> is a button binding.
<Shift-Up>	
    The user pressed the Up arrow, while holding the Shift key pressed. You can use prefixes like Alt, Shift, and Control.
<Configure>	
    The widget changed size (or location, on some platforms). The new size is provided in the width and height attributes of the event object passed to the callback.
<Activate>	
    A widget is changing from being inactive to being active. This refers to changes in the state option of a widget such as a button changing from inactive (grayed out) to active.
<Deactivate>	
    A widget is changing from being active to being inactive. This refers to changes in the state option of a widget such as a radiobutton changing from active to inactive (grayed out).
<Destroy>	
    A widget is being destroyed.
<Expose>	
    This event occurs whenever at least some part of your application or widget becomes visible after having been covered up by another window.
<KeyRelease>	
    The user let up on a key.
<Map>	
    A widget is being mapped, that is, made visible in the application. This will happen, for example, when you call the widget's .grid() method.
<Motion>	
    The user moved the mouse pointer entirely within a widget.
<MouseWheel>	
    The user moved the mouse wheel up or down. At present, this binding works on Windows and MacOS, but not under Linux.
<Unmap>	
    A widget is being unmapped and is no longer visible.
<Visibility>	
    Happens when at least some part of the application window becomes visible on the screen.

"""

import asyncio
import tkinter
import threading

class EventLoops:
    def __init__(self) -> None:
        self.count = 0
        self.root = None 
        self.label1 = None
        self.async_loop = None 
    def setup_gui(self):
        """setup gui"""
        self.root = tkinter.Tk()
        self.root.geometry('600x600')
        button1 = tkinter.Button(self.root,height=5, width=10, text="?")
        button1.grid(row=1, column=1)
        button1.bind('<ButtonPress-1>', self.stop_prog)
        button2 = tkinter.Button(self.root,height=5, width=10, text="Click Me")
        button2.grid(row=2, column=1)
        button2.bind('<ButtonPress-1>', self.show_counter)
        self.label1 = tkinter.Label(self.root, text="0")
        self.label1.grid(row=3, column=1)
    def stop_prog(self, e):
        """button click closes gui application"""
        self.root.quit()
    def show_counter(self, e):
        """button click increments and displays value on gui"""
        self.count = self.count + 1
        self.label1.configure(text=count)
        asyncio.run_coroutine_threadsafe(self.counter_updated(), self.async_loop)
    async def counter_updated(self):
        print('counter updated')
    async def tick(self):
        """prints message when event loop is available"""
        k=0
        while True:
            k += 1
            print("TICK", k)
            await asyncio.sleep(0.5)
    async def main(self):
        """setup/starts event loop"""
        task = asyncio.create_task((self.tick()))
        self.async_loop = task.get_loop() # get event loop 
        await asyncio.wait((task,))
    def run_asyncio(self):
        """calls asynchronous main to start"""
        asyncio.run(self.main())
eventloops_inst = EventLoops() 
eventloops_inst.setup_gui()
t=threading.Thread(target=eventloops_inst.run_asyncio, daemon=True) # thread terminates if main thread terminates 
t.start()
eventloops_inst.root.mainloop()