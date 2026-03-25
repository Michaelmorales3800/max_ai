"""
max_avatar.py — MAX's VSeeFace Avatar Controller
Controls VSeeFace via the VTube Studio API (WebSocket on port 8001).
VSeeFace must be running with "Enable VTube Studio API" turned ON.
 
Install: pip install websocket-client
"""
 
import threading
import time
import json
import random
 
try:
    import websocket
    WS_AVAILABLE = True
except ImportError:
    WS_AVAILABLE = False
 
VSEEFACE_HOST = "127.0.0.1"
VSEEFACE_PORT = 8001
PLUGIN_NAME   = "MAX AI"
PLUGIN_DEV    = "MAX"
 
 
class MaxAvatar:
    EXPR_TALKING = "talking"
    EXPR_IDLE    = "default"
    EXPR_THINK   = "thinking"
 
    def __init__(self):
        self.ws        = None
        self.token     = None
        self.connected = False
        self._auth_done = False
 
        if not WS_AVAILABLE:
            print("[MAX Avatar] websocket-client not installed.")
            print("[MAX Avatar] Run:  pip install websocket-client")
            print("[MAX Avatar] VSeeFace disabled — MAX still works normally.")
            return
 
        t = threading.Thread(target=self._connect, daemon=True)
        t.start()
        time.sleep(1.5)
 
    def _connect(self):
        url = f"ws://{VSEEFACE_HOST}:{VSEEFACE_PORT}"
        try:
            self.ws = websocket.WebSocket()
            self.ws.connect(url, timeout=3)
            self.connected = True
            print(f"[MAX Avatar] Connected to VSeeFace at {url}")
            self._authenticate()
        except Exception as e:
            self.connected = False
            print(f"[MAX Avatar] Could not connect to VSeeFace: {e}")
            print("[MAX Avatar] Make sure VSeeFace is running with VTube Studio API enabled.")
 
    def _send(self, payload: dict) -> dict | None:
        if not self.connected or not self.ws:
            return None
        try:
            self.ws.send(json.dumps(payload))
            response = self.ws.recv()
            return json.loads(response)
        except Exception:
            self.connected = False
            return None
 
    def _authenticate(self):
        req = {
            "apiName": "VTubeStudioPublicAPI", "apiVersion": "1.0",
            "requestID": "auth-req-1", "messageType": "AuthenticationTokenRequest",
            "data": {"pluginName": PLUGIN_NAME, "pluginDeveloper": PLUGIN_DEV, "pluginIcon": None}
        }
        resp = self._send(req)
        if resp and resp.get("data", {}).get("authenticationToken"):
            self.token = resp["data"]["authenticationToken"]
            auth = {
                "apiName": "VTubeStudioPublicAPI", "apiVersion": "1.0",
                "requestID": "auth-req-2", "messageType": "AuthenticationRequest",
                "data": {"pluginName": PLUGIN_NAME, "pluginDeveloper": PLUGIN_DEV, "authenticationToken": self.token}
            }
            resp2 = self._send(auth)
            if resp2 and resp2.get("data", {}).get("authenticated"):
                self._auth_done = True
                print("[MAX Avatar] VSeeFace authentication successful ✅")
            else:
                print("[MAX Avatar] Auth failed — approve the plugin popup in VSeeFace.")
 
    def _trigger_hotkey(self, hotkey_name: str):
        if not self.connected or not self._auth_done:
            return
        payload = {
            "apiName": "VTubeStudioPublicAPI", "apiVersion": "1.0",
            "requestID": f"hotkey-{hotkey_name}", "messageType": "HotkeyTriggerRequest",
            "data": {"hotkeyID": hotkey_name}
        }
        self._send(payload)
 
    def animate_talking(self, duration: float = 2.5):
        if not self.connected:
            return
        def _do():
            self._trigger_hotkey(self.EXPR_TALKING)
            time.sleep(max(duration + random.uniform(-0.3, 0.5), 0.5))
            self._trigger_hotkey(self.EXPR_IDLE)
        threading.Thread(target=_do, daemon=True).start()
 
    def animate_thinking(self, duration: float = 1.0):
        if not self.connected:
            return
        def _do():
            self._trigger_hotkey(self.EXPR_THINK)
            time.sleep(duration)
        threading.Thread(target=_do, daemon=True).start()
 
    def set_idle(self):
        self._trigger_hotkey(self.EXPR_IDLE)
 
    def is_ready(self) -> bool:
        return self.connected and self._auth_done
 
 
if __name__ == "__main__":
    print("Testing MAX Avatar → VSeeFace connection...")
    av = MaxAvatar()
    time.sleep(2)
    if av.is_ready():
        print("Connected! Triggering talking animation for 3s...")
        av.animate_talking(3)
        time.sleep(4)
    else:
        print("Not connected. Start VSeeFace and enable VTube Studio API on port 8001.")
 