bluetooth.onBluetoothConnected(function () {
    basic.showIcon(IconNames.Yes)
})
bluetooth.onBluetoothDisconnected(function () {
    basic.showIcon(IconNames.No)
})
input.onButtonPressed(Button.A, function () {
    led.setBrightness(led.brightness() / 2)
})
function affiche_debug () {
    if (is_data_recue) {
        is_data_recue = false
        led.plot(0, 0)
        basic.pause(50)
        led.unplot(0, 0)
    }
    if (is_data_transmise) {
        is_data_transmise = false
        led.plot(4, 0)
        basic.pause(50)
        led.unplot(4, 0)
    }
}
input.onButtonPressed(Button.AB, function () {
    basic.clearScreen()
    is_mode_TdB = !(is_mode_TdB)
})
function reception_bt () {
    text_rx = chaine_BT_rx.substr(0, chaine_BT_rx.indexOf(":"))
    valeur_rx = parseFloat(chaine_BT_rx.substr(chaine_BT_rx.indexOf(":") + 1, 10))
    if (text_rx == "ping") {
        ecriture_valeur_bt("pong", 1)
    }
}
input.onButtonPressed(Button.B, function () {
    led.setBrightness((led.brightness() + 1) * 2 % 256)
})
function ecriture_valeur_bt (texte: string, nombre: number) {
    is_data_transmise = true
    bluetooth.uartWriteValue("" + control.deviceName() + texte, nombre)
}
bluetooth.onUartDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    chaine_BT_rx = bluetooth.uartReadUntil(serial.delimiters(Delimiters.NewLine))
    is_data_recue = true
    reception_bt()
    ecriture_valeur_bt("P0et", etat_pin0)
    ecriture_valeur_bt("fini", 1)
})
let etat_pin0 = 0
let valeur_rx = 0
let chaine_BT_rx = ""
let text_rx = ""
let is_data_transmise = false
let is_data_recue = false
let is_mode_TdB = false
bluetooth.startUartService()
bluetooth.setTransmitPower(7)
basic.showString("Voltmetre_P0_v0a")
led.setBrightness(20)
is_mode_TdB = true
basic.forever(function () {
    etat_pin0 = pins.analogReadPin(AnalogPin.P0)
    if (is_mode_TdB) {
        led.plotBarGraph(
        etat_pin0,
        1023,
        false
        )
    } else {
        affiche_debug()
    }
    basic.pause(50)
})
