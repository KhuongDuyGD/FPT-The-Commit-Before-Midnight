screen chapter1_end():
    modal True
    zorder 100
    add Solid("#0b1523ef")
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 25
        text "CHAPTER 1 COMPLETE" size 30 color "#a8bbd2" xalign 0.5
        text current_route.replace("_", " ") size 56 bold True color "#f3be85" xalign 0.5
        textbutton "New Game" action Jump("start") text_size 29 xalign 0.5
        textbutton "Return to Main Menu" action MainMenu(confirm=False) text_size 28 xalign 0.5
