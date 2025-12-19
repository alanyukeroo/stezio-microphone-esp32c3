# ESP32-C3 Audio Streamer

This project allows you to stream live audio from an SPH0645 I2S microphone using a XIAO ESP32-C3 to a web browser via a Node.js server.

## Hardware Setup

You will need the following parts:

- XIAO ESP32-C3
- SPH0645 I2S Microphone
- Jumper wires

### Wiring Table

Connect the SPH0645 to the XIAO ESP32-C3 as follows:

| SPH0645 Pin | XIAO ESP32-C3 Pin | Function |
| :--- | :--- | :--- |
| 3V | 3.3V | Power |
| GND | GND | Ground |
| BCLK | D4 (GPIO 6) | Bit Clock (SCK) |
| LRC | D5 (GPIO 7) | Word Select (WS) |
| DOUT | D6 (GPIO 21) | Data Out (SD) |
| SEL | GND | Left Channel Select |

**Note:** Connecting SEL to GND is required to set the microphone to the left channel.

## Software Setup

### 1. Node.js Backend (Windows)

1. Create a folder for your project on your laptop.
2. Inside that folder, create a file named `server.js` and `index.html`.
3. Open a terminal in that folder and install the websocket library:
   ```bash
   npm install ws
   ```

### 2. MicroPython (ESP32-C3)

1. Flash the latest stable MicroPython firmware to your XIAO ESP32-C3.
2. Open `main.py` in Thonny.
3. Update the `WIFI_SSID`, `WIFI_PASS`, and `LAPTOP_IP` variables with your local network details.

## Running the Project

1. **Start the Server:** Open your terminal and run `node server.js`. You should see a message saying the server is active.
2. **Open the Web Page:** Open your browser and go to `http://localhost:3001`.
3. **Run the ESP32 Code:** In Thonny, press the Run button to start the script on your board.
4. **Listen:** Click the **Mulai Dengar** (Start Listening) button on the web page.

## Troubleshooting

### Common Errors

- **EADDRINUSE:** This means port 3000 or 3001 is already taken. Close other node processes or change the port in `server.js`.
- **ECONNRESET:** The ESP32 found the laptop but the connection was blocked. Check your Windows Firewall and ensure port 5000 is open.
- **Wifi Internal State Error:** Perform a hard reset by unplugging and plugging back the USB cable.

### Noise Issues

- Keep the wires between the mic and the board as short as possible.
- Avoid placing the mic directly next to the WiFi antenna on the XIAO board.
- If the sound has a clicking noise, ensure you are using the optimized scheduling code in your `index.html`.

## Project Files

- **main.py:** Handles audio capture and WiFi transmission.
- **server.js:** Bridges the TCP data from the ESP32 to the web browser via WebSockets.
- **index.html:** Provides the user interface and plays the audio using the Web Audio API. 
