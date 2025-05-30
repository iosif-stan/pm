#include "driver/adc.h"

#define ADC1_CH6 ADC1_CHANNEL_6  // GPIO34
#define ADC1_CH7 ADC1_CHANNEL_7  // GPIO35

#define LED_GREEN 25
#define LED_YELLOW 26
#define LED_RED 27

const int filterWindow = 10;
int buffer1[filterWindow];
int buffer2[filterWindow];
int idx = 0;

//pentru normalizarea semnalului
const int NORMALIZE_CENTER = 3600;
const int GAIN = 5;

void setup() {
  Serial.begin(115200);

  //configuram rezolutia ADC ului la 12 biti si atenuarea semnalului pentru a permite pana la 3v3
  adc1_config_width(ADC_WIDTH_BIT_12);
  adc1_config_channel_atten(ADC1_CH6, ADC_ATTEN_DB_11);
  adc1_config_channel_atten(ADC1_CH7, ADC_ATTEN_DB_11);

  //setam gpio25 26 27 ca output si pastram restul pinilor la fel
  REG_WRITE(GPIO_ENABLE_REG, READ_PERI_REG(GPIO_ENABLE_REG) |(1 << LED_GREEN) | (1 << LED_YELLOW) | (1 << LED_RED));
}

//functie cu care selectam un anumit pin GPIO si starea in care vrem sa il punem
void setLED(uint8_t pin, bool state) {
  if (state)
    REG_WRITE(GPIO_OUT_W1TS_REG, (1 << pin));
  else
    REG_WRITE(GPIO_OUT_W1TC_REG, (1 << pin));
}

//functie folosita pentru a netezi semnalul , atenuare sliding window
int average(int* buffer) {
  long sum = 0;
  for (int i = 0; i < filterWindow; ++i) sum += buffer[i];
  return sum / filterWindow;
}

//setarea pragurilor pentru aprinderea ledurilor
void updateLEDs(int avg) {
  if (avg < 3450) {
    setLED(LED_GREEN, true);
    setLED(LED_YELLOW, false);
    setLED(LED_RED, false);
  } else if (avg < 3600) {
    setLED(LED_GREEN, false);
    setLED(LED_YELLOW, true);
    setLED(LED_RED, false);
  } else {
    setLED(LED_GREEN, false);
    setLED(LED_YELLOW, false);
    setLED(LED_RED, true);
  }
}

void loop() {
  //primim valoarea raw de tensiune de pe canalele adc (0 ->4096)
  int val1 = adc1_get_raw(ADC1_CH6);
  int val2 = adc1_get_raw(ADC1_CH7);

  //umplem bufferele pentru atenuare zgomot
  buffer1[idx] = val1;
  buffer2[idx] = val2;
  idx = (idx + 1) % filterWindow;

  int avg1 = average(buffer1);
  int avg2 = average(buffer2);
  int avg = (avg1 + avg2) / 2;

  updateLEDs(avg);

  //normalizează și amplifică
  int norm1 = (avg1 - NORMALIZE_CENTER) * GAIN;
  int norm2 = (avg2 - NORMALIZE_CENTER) * GAIN;
  int normAvg = (norm1 + norm2) / 2;

  //trimite valorile normalizate + amplificate
  Serial.printf("%d %d %d\n", norm1, norm2, normAvg);
  delay(30);
}
