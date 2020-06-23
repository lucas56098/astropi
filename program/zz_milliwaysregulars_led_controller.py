from sense_hat import SenseHat

class LedController():
    #uses the led_matrix on sense_hat to show messages and images

    def __init__(self):
        #initalizes sense_hat
        self.__sense = SenseHat()
        self.__sense.clear()


    def letter(self, X, i):
        #dont panic! letters
        o = (0,0,0)
        length = 75
        text = [
                o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,
                o,o,o,o,o,o,o,o,o,X,X,X,o,o,o,o,X,X,X,o,o,X,o,o,o,X,o,X,o,X,X,X,X,X,o,o,o,X,X,X,X,o,o,o,X,X,X,o,o,X,o,o,o,X,o,X,X,X,o,o,X,X,X,X,o,o,X,o,o,o,o,o,o,o,o,
                o,o,o,o,o,o,o,o,o,X,o,o,X,o,o,X,o,o,o,X,o,X,o,o,o,X,o,X,o,o,o,X,o,o,o,o,o,X,o,o,o,X,o,X,o,o,o,X,o,X,o,o,o,X,o,o,X,o,o,X,o,o,o,o,o,o,X,o,o,o,o,o,o,o,o,
                o,o,o,o,o,o,o,o,o,X,o,o,o,X,o,X,o,o,o,X,o,X,X,o,o,X,o,o,o,o,o,X,o,o,o,o,o,X,o,o,o,X,o,X,o,o,o,X,o,X,X,o,o,X,o,o,X,o,o,X,o,o,o,o,o,o,X,o,o,o,o,o,o,o,o,
                o,o,o,o,o,o,o,o,o,X,o,o,o,X,o,X,o,o,o,X,o,X,o,X,o,X,o,o,o,o,o,X,o,o,o,o,o,X,X,X,X,o,o,X,X,X,X,X,o,X,o,X,o,X,o,o,X,o,o,X,o,o,o,o,o,o,X,o,o,o,o,o,o,o,o,
                o,o,o,o,o,o,o,o,o,X,o,o,o,X,o,X,o,o,o,X,o,X,o,o,X,X,o,o,o,o,o,X,o,o,o,o,o,X,o,o,o,o,o,X,o,o,o,X,o,X,o,o,X,X,o,o,X,o,o,X,o,o,o,o,o,o,X,o,o,o,o,o,o,o,o,
                o,o,o,o,o,o,o,o,o,X,o,o,X,o,o,X,o,o,o,X,o,X,o,o,o,X,o,o,o,o,o,X,o,o,o,o,o,X,o,o,o,o,o,X,o,o,o,X,o,X,o,o,o,X,o,o,X,o,o,X,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,
                o,o,o,o,o,o,o,o,o,X,X,X,o,o,o,o,X,X,X,o,o,X,o,o,o,X,o,o,o,o,o,X,o,o,o,o,o,X,o,o,o,o,o,X,o,o,o,X,o,X,o,o,o,X,o,X,X,X,o,o,X,X,X,X,o,o,X,o,o,o,o,o,o,o,o,
                ]

        return text[i:i+8] + text[i+length :i+8+length] + text[i+2*length :i+8+2*length] + text[i+3*length :i+8+3*length] + text[i+4*length :i+8+4*length] + text[i+5*length :i+8+5*length] + text[i+6*length :i+8+6*length] + text[i+7*length :i+8+7*length]


    def letter_smile(self, X):
        #smiling face
        o = (0,0,0)
        return [X,X,X,X,X,X,X,X,
                X,o,o,o,o,o,o,X,
                X,o,X,o,o,X,o,X,
                X,o,o,o,o,o,o,X,
                X,o,X,o,o,X,o,X,
                X,o,X,X,X,X,o,X,
                X,o,o,o,o,o,o,X,
                X,X,X,X,X,X,X,X,
                ]


    def dont_panic(self):
        #changing colour and moving the text
        for i in range(0,50*68):
            X = (abs(i % 510 -255), abs((i + 100) % 510 -255), abs((i + 220) % 510 -255))
            self.__sense.set_pixels(self.letter(X,int(i/50)))


    def smile_a_little_bit(self):
        #changing colour of smile
        for i in range(0,1000):
            X = (abs(i % 510 -255), abs((i + 100) % 510 -255), abs((i + 220) % 510 -255))
            self.__sense.set_pixels(self.letter_smile(X))


    def show_message(self, message):
        #show message
        self.__sense.show_message(message)
