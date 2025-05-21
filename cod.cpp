#include <Arduino.h>

#define OPT1_PIN 34     // ADC1_CHANNEL_6
#define OPT2_PIN 35     // ADC1_CHANNEL_7

#define N_SAMPLES 10

float buffer1[N_SAMPLES] = {0};
float buffer2[N_SAMPLES] = {0};
int idx = 0;

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);  // rezoluție ADC 12 biți
}

float average(const float* buf) {
  float sum = 0;
  for (int i = 0; i < N_SAMPLES; i++) {
    sum += buf[i];
  }
  return sum / N_SAMPLES;
}

void loop() {
  // Citește ambii senzori
  buffer1[idx] = analogRead(OPT1_PIN);
  buffer2[idx] = analogRead(OPT2_PIN);

  // Calculează mediile
  float avg1 = average(buffer1);
  float avg2 = average(buffer2);

  // Calculează semnalul filtrat (diferența pentru atenuarea zgomotului comun)
  float filtered_signal = avg1 - avg2;

  // Afișează valorile
  Serial.print("Media senzor 1: ");
  Serial.println(avg1);
  Serial.print("Media senzor 2: ");
  Serial.println(avg2);
  Serial.print("Semnal filtrat: ");
  Serial.println(filtered_signal);

  // Incrementare index cu wrap-around
  idx = (idx + 1) % N_SAMPLES;

  delay(10);
}
