#include <driver/i2s.h>

#define I2S_WS 7
#define I2S_SD 21
#define I2S_SCK 6
#define I2S_PORT I2S_NUM_0

void setup() {
  // Kembali ke kecepatan yang sudah terbukti berhasil
  Serial.begin(2000000); 
  
  const i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = 16000,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT, // Ambil data utuh
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = i2s_comm_format_t(I2S_COMM_FORMAT_STAND_I2S),
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 8,
    .dma_buf_len = 64,
    .use_apll = false
  };

  const i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = -1,
    .data_in_num = I2S_SD
  };

  i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_PORT, &pin_config);
  i2s_start(I2S_PORT);
}

void loop() {
  int32_t sample = 0;
  size_t bytes_read;
  
  i2s_read(I2S_PORT, &sample, sizeof(sample), &bytes_read, portMAX_DELAY);
  
  if (bytes_read > 0) {
    // Kirim 4 byte mentah (32-bit)
    Serial.write((uint8_t*)&sample, sizeof(sample));
  }
}