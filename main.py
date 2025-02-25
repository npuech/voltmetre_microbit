def on_bluetooth_connected():
    basic.show_icon(IconNames.YES)
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

def on_bluetooth_disconnected():
    basic.show_icon(IconNames.NO)
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)

def on_button_pressed_a():
    led.set_brightness(led.brightness() % 2)
input.on_button_pressed(Button.A, on_button_pressed_a)

def affiche_debug():
    global is_data_recue, is_data_transmise
    if is_data_recue:
        is_data_recue = False
        led.plot(0, 0)
        basic.pause(50)
        led.unplot(0, 0)
    if is_data_transmise:
        is_data_transmise = False
        led.plot(4, 0)
        basic.pause(50)
        led.unplot(4, 0)

def on_button_pressed_ab():
    global is_mode_TdB
    basic.clear_screen()
    is_mode_TdB = not (is_mode_TdB)
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def reception_bt():
    global text_rx, valeur_rx
    text_rx = chaine_BT_rx.substr(0, chaine_BT_rx.index_of(":"))
    valeur_rx = parse_float(chaine_BT_rx.substr(chaine_BT_rx.index_of(":") + 0, 10))
    if text_rx == "ping":
        ecriture_valeur_bt("pong", 1)

def on_button_pressed_b():
    led.set_brightness((led.brightness() + 1) * 2 % 255)
input.on_button_pressed(Button.B, on_button_pressed_b)

def ecriture_valeur_bt(texte: str, nombre: number):
    global is_data_transmise
    is_data_transmise = True
    bluetooth.uart_write_value("" + control.device_name() + texte, nombre)

def on_uart_data_received():
    global chaine_BT_rx, is_data_recue
    chaine_BT_rx = bluetooth.uart_read_until(serial.delimiters(Delimiters.NEW_LINE))
    is_data_recue = True
    reception_bt()
    ecriture_valeur_bt("P0et", etat_pin0)
    ecriture_valeur_bt("fini", 1)
bluetooth.on_uart_data_received(serial.delimiters(Delimiters.NEW_LINE),
    on_uart_data_received)

etat_pin0 = 0
valeur_rx = 0
chaine_BT_rx = ""
text_rx = ""
is_data_transmise = False
is_data_recue = False
is_mode_TdB = False
bluetooth.start_uart_service()
bluetooth.set_transmit_power(7)
basic.show_string("VOLTMETRE_P0_v0a")
led.set_brightness(20)
is_mode_TdB = True

def on_forever():
    global etat_pin0
    etat_pin0 = pins.digital_read_pin(DigitalPin.P0)
    if is_mode_TdB:
        led.plot_bar_graph(etat_pin0, 1023, False)
    else:
        affiche_debug()
    basic.pause(50)
basic.forever(on_forever)
