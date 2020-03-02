#include "MicroBit.h"

MicroBit uBit;

void countdown(int value) {
    for (int i = value; i > 0; i--) {
        uBit.display.printChar('0' + i);
        uBit.sleep(1000);
    }

    while (1) {
        uBit.display.printChar('0');
    }
}

int main() {
    uBit.init();

    int value = 5;

    while (1) {
        if (uBit.buttonAB.isPressed()) {
            countdown(value);
        } else if (uBit.buttonA.isPressed() && value > 1) {
            value--;
            uBit.sleep(500);
        } else if (uBit.buttonB.isPressed() && value < 9) {
            value++;
            uBit.sleep(500);
        }
 
        uBit.display.printChar('0' + value);
    }
}