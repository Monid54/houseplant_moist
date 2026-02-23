#include <WiFi.h>
#include <HTTPClient.h>
#include "<secrets.h"

const char* hostIpFallback = "192.168.1.161";
const char* hostMdns = "plant-hub.local";
const int port = 8080;

const char* sensorId = "plant1";

#define SENSOR_PIN 3   // ADC-Pin for moisture sensor (0..4095)

static const uint32_t INTERVAL_MS = 900000; // 900s = 15min

int readAveraged(int pin, int samples = 12) {
  long sum = 0;
  for (int i = 0; i < samples; i++) {
    sum += analogRead(pin);
    delay(5);
  }
  return (int)(sum / samples);
}

// Calibration: 390 = dry, 630 = moist (values depend on your sensor and soil!)
int toPercent(int raw, int dry = 390, int wet = 630) {
  int pct = map(raw, dry, wet, 0, 100);
  if (pct < 0) pct = 0;
  if (pct > 100) pct = 100;
  return pct;
}

// Build the URL for the POST request.
// It first tries to resolve the host name using mDNS, and if that fails, it falls back to a hardcoded IP address.
// The IP address demends on your local network setup and the device running the backend service.
String buildUrl() {
  if (hostIpFallback && strlen(hostIpFallback) > 0) {
    return "http://" + String(hostIpFallback) + ":" + String(port) + "/ingest";
  }
  IPAddress ip;
  if (WiFi.hostByName(hostMdns, ip)) {
    return "http://" + ip.toString() + ":" + String(port) + "/ingest";
  }
  return "";
}

// This function sends a POST request with a JSON payload to the specified URL.
bool postJson(const String& url, const String& payload) {
  HTTPClient http;
  http.setTimeout(6000);
  http.begin(url);
  http.addHeader("Content-Type", "application/json");

  int code = http.POST(payload);
  String resp = http.getString();
  http.end();

  Serial.print("POST -> ");
  Serial.print(code);
  Serial.print(" resp=");
  Serial.println(resp);

  return (code >= 200 && code < 300);
}

// This function ensures that the device is connected to WiFi.
// If it's not connected, it attempts to connect using the provided SSID and password.
void ensureWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  Serial.print("Connecting WiFi");
  uint32_t start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < 20000) {
    delay(400);
    Serial.print(".");
  }
  Serial.println();
  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("WiFi OK, IP=");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("WiFi connect failed");
  }
}

// The setup function initializes the serial communication,
// configures the ADC resolution,
// sets the sensor pin as input,
// and ensures that the device is connected to WiFi.
void setup() {
  Serial.begin(115200);
  delay(200);

  analogReadResolution(12); // 0..4095
  pinMode(SENSOR_PIN, INPUT);

  WiFi.mode(WIFI_STA);
  WiFi.setAutoReconnect(true);
  WiFi.persistent(false);

  ensureWiFi();   // Start with WiFi connection, but continue even if it fails (will retry in loop)
}

void loop() {
  // Wifi-Check and reconnect if needed.
  // We want to avoid sending data if we are not connected, but also don't want to block the loop for too long if WiFi is down.
  ensureWiFi();

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi reconnect...");
    WiFi.reconnect();
    delay(2000);
    return;
  }

  int raw = readAveraged(SENSOR_PIN);
  int moisture = toPercent(raw);

  String url = buildUrl();
  if (url.length() == 0) {
    Serial.println("DNS failed (mDNS + fallback).");
    delay(INTERVAL_MS);
    return;
  }

  // build JSON payload manually to avoid adding ArduinoJson dependency
  String payload = String("{\"sensor_id\":\"") + sensorId +
                   String("\",\"raw\":") + raw +
                   String(",\"moisture\":") + moisture +
                   String(",\"rssi\":") + WiFi.RSSI() +
                   String("}");

  // Retry (important if Wifi is flaky or backend is temporarily unavailable), but don't block the loop for too long.
  bool ok = false;
  for (int i = 0; i < 3 && !ok; i++) {
    ok = postJson(url, payload);
    if (!ok) {
      Serial.println("Retry POST...");
      delay(1500);
    }
  }

  Serial.print("raw=");
  Serial.print(raw);
  Serial.print(" moisture=");
  Serial.print(moisture);
  Serial.print("% ok=");
  Serial.println(ok ? "true" : "false");

  delay(INTERVAL_MS);
}
