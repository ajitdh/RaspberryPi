#include <wiringPi.h>
#include <iostream>
#include <cstdlib>

using namespace std;

class Dht11 {
private:
	int pinSensor = 0;
	long int tstart = 0;
	long int tmpDta[40];
	int dta[5] = {0,0,0,0,0};
public:
	Dht11(int pin);
	void meet();
	void verzamel();
	void verwerk();
};

int main (int argc, char *argv[]) {
	int pin = 5;
	
	if (argc > 1) {
		pin = atoi(argv[1]);
	}
	
	Dht11 dht(pin);
	dht.meet();
	
	return 0;
}

Dht11::Dht11(int pin) {
	this->pinSensor = pin;
	
	wiringPiSetupGpio();
	pinMode(this->pinSensor, OUTPUT);
	digitalWrite(this->pinSensor, LOW);
	delay(200);
	digitalWrite(this->pinSensor, HIGH);
}

void Dht11::meet() {
	this->verzamel();
	this->verwerk();
}

void Dht11::verzamel() {
	int i = 0;
	
	pinMode(this->pinSensor, INPUT);
	while (digitalRead(this->pinSensor) == HIGH){};
	while (digitalRead(this->pinSensor) == LOW){};
	while (digitalRead(this->pinSensor) == HIGH){};
	this->tstart = micros();
	while (i < 40) {
		while (digitalRead(this->pinSensor) == LOW){};
		while (digitalRead(this->pinSensor) == HIGH){};
		this->tmpDta[i] = micros();
		i++;
	}
}

void Dht11::verwerk() {
	int p[8] = {0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01};
	long int t0, t1;
	t0 = this->tstart;
	
	for (int i = 0; i < 5; i++) {
		for (int j = 0; j < 8 ; j++) {
			t1 = this->tmpDta[8*i + j];
			if ((t1-t0) > 100) {
				this->dta[i] += p[j];
			}
			t0 = t1;
		}
	}
	
	if (this->dta[0] + this->dta[1] + this->dta[2] 
						+ this->dta[3] == this->dta[4]){
		cout << this->dta[0] << "," << this->dta[2] << endl;
	} else {
		cout << 0 << endl;
	}
}
