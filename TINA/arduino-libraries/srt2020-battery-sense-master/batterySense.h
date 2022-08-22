/*

My name is Dustin Richards and welcome to my header file!

To use this class: call the constructor, then call init() in the setup() function

There are six parameters that should be checked before using this class:
  r1, r2, adc1, v1, adc2, and v2.

========
VOLTAGE DIVIDER
========
r1 and r2 are for the voltage divider, since an ESP32 can't take the 7-ish
  volts that our battery packs put out. We use a voltage divider to step
  down the voltage to something that our ESP32 can safely measure.

A voltage divider follows this equation:

  Vout = Vin * (r2 / (r1 + r2))

It's a ratio between the two resistor values! The equation corresponds with
  this diagram:

  Vin------/\/\/\/----Vout----\/\/\/\------GND
             r1                  r2

As you can see from the equation above, the smaller r2 is, the lower Vout
  is compared to Vin. Enter the resistor values that you used in your
  voltage divider so the code can correctly calculate the battery voltage
  by reading the ESP32's ADC (analog to digital converter) pin. I used
  r1 = 22k and r2 = 10k, meaning that for a 7V battery input, 2.1875V
  will be on the ADC pin.

  Vout = 7V * (10000 / (22000 + 10000)) = 7V * 0.3125 = 2.1875V

But, we're actually concerned with finding the battery voltage and not
  the voltage on the pin, so I solved for Vin and we calculate Vout
  instead:

  Vin = Vout * (r2 + r1) / r2

========
ADC CALIBRATION
========
The ADC (analog to digital converter) lets us check the voltage present
  on an ADC-capable pin on the ESP32. This will return a 12-bit value
  with - ideally - 0 being 0V and 4095 being 3.3V. However, the ADC isn't
  perfect and needs to be calibrated to compensate for this fact. This
  often isn't a huge concern, but when we're using this information to
  make sure we don't damage the battery by discharging it too far, it's
  good to be sure your voltage readings are accurate.

To calibrate the ADC using this class, call calibrate() after calling
  init() in setup() in your Arduino sketch. This will put the class
  into a loop where it's just continually sampling the ADC and
  outputting the result to the serial monitor. With the battery plugged
  in, neasure the voltage on the ADC pin with a multimeter and check
  the ADC value in the serial monitor. Enter these values into v1 and
  adc1. Do the same with a different voltage for v2 and adc2.
  Just DO NOT exceed 3.3V on the ADC pins. You can adjust the voltage
  divider to output a lower voltage or connect an external voltage
  source to do this. When you're done, remove the calibrate() function
  call and your code should run normally again.
 */

#ifndef __SRT_BATTERY_SENSE
#define __SRT_BATTERY_SENSE

#include <Arduino.h>

class SRTBatterySense
{
private:
  //set r1 and r2 to equal your voltage divider resistor values
  const float r1 = 22000;
  const float r2 = 10000;
  const float vSenseAdjust = (r2 + r1) / r2;

  //set these to two different points measured with a multimeter to calibrate the ADC
  const int adc1 = 631;
  const float v1 = 0.665;
  const int adc2 = 2611;
  const float v2 = 2.294;
  
  const float m = (float)(v2 - v1) * 100000 / (float)(adc2 - adc1);
  const float b = v2 - m * adc2 / 100000;

  int sensePin;
  const int NUM_BATTERY_SAMPLES = 200;

  float adcToBatteryVoltage(uint32_t adc);
  uint32_t sampleADC();

  uint64_t batteryCheckPrevTime = 0;
  static const int BATTERY_CHECK_NUM_SAMPLES = 10; //number of battery reading samples to average
  const uint32_t BATTERY_CHECK_PERIOD = 1000; //time between battery checks, in milliseconds
  int batteryCheckAverageIndex = 0;
  float batteryCheckSum = 0;
  float batteryCheckAverage = 0;
  float batteryCheckSamples[BATTERY_CHECK_NUM_SAMPLES];

public:
  SRTBatterySense(int _sensePin);
  void init();
  void calibrate();
  float getBatteryVoltage();
  float getRollingAverage();
};

#endif
