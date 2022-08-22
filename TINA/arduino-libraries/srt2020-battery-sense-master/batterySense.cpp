#include "batterySense.h"

SRTBatterySense::SRTBatterySense(int _sensePin)
{
  sensePin = _sensePin;
}

void SRTBatterySense::init()
{
  pinMode(sensePin, INPUT);

  for (int i = 0; i < BATTERY_CHECK_NUM_SAMPLES; i++)
  {
    batteryCheckSamples[i] = 7.2;
  }
}

void SRTBatterySense::calibrate()
{
  Serial.begin(115200);

  do
  {
    Serial.println(sampleADC());
    delay(1000);
  } while (true);
}

float SRTBatterySense::getBatteryVoltage()
{
  float v = adcToBatteryVoltage(sampleADC());
  return v;
  //return adcToBatteryVoltage(sampleADC());
}

uint32_t SRTBatterySense::sampleADC()
{
  uint32_t sum = 0;
  uint32_t avg = 0;
  for (int i = 0; i < NUM_BATTERY_SAMPLES; i++)
  {
    sum += analogRead(sensePin);
  }
  avg = sum / NUM_BATTERY_SAMPLES;

  return avg;
}

float SRTBatterySense::adcToBatteryVoltage(uint32_t adc)
{
  return (m * adc / 100000 + b) * vSenseAdjust;
}

float SRTBatterySense::getRollingAverage()
{
  if (millis() > batteryCheckPrevTime + BATTERY_CHECK_PERIOD || batteryCheckPrevTime == 0)
  {
    batteryCheckSamples[batteryCheckAverageIndex++] = getBatteryVoltage();
    if (batteryCheckAverageIndex = BATTERY_CHECK_NUM_SAMPLES)
    {
      batteryCheckAverageIndex = 0;
    }

    batteryCheckSum = 0;
    for (int i = 0; i < BATTERY_CHECK_NUM_SAMPLES; i++)
    {
      batteryCheckSum += batteryCheckSamples[i];
    }
    batteryCheckAverage = batteryCheckSum / BATTERY_CHECK_NUM_SAMPLES;

    batteryCheckPrevTime = millis();
  }

  return batteryCheckAverage;
}
