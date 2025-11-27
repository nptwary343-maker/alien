from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import sys
import psutil
import threading
import socket
import requests
import hashlib
import re

app = Flask(__name__)
CORS(app)

@app.route('/run_command', methods=['POST'])
def run_command():
    data = request.json
    cmd = data.get('command')
    if not cmd: return jsonify({"error": "No command"}), 400
    try:
        # Cross-platform support
        if sys.platform.startswith('win'):
            result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, timeout=10)
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return jsonify({"stdout": result.stdout, "stderr": result.stderr})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run_python', methods=['POST'])
def run_python():
    data = request.json
    code = data.get('code')
    if not code: return jsonify({"error": "No code"}), 400
    try:
        result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=10)
        return jsonify({"stdout": result.stdout, "stderr": result.stderr})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- ADVANCED TOOLS (ZERO DELAY) ---

@app.route('/tool/wifi', methods=['GET'])
def tool_wifi():
    try:
        if sys.platform.startswith('win'):
            result = subprocess.run(["netsh", "wlan", "show", "networks", "mode=bssid"], capture_output=True, text=True)
            return jsonify({"raw": result.stdout})
        else:
            return jsonify({"error": "WiFi scanning requires Windows (netsh)."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tool/processes', methods=['GET'])
def tool_processes():
    # Fast Process List (Top 20 by Memory)
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            procs.append(p.info)
        except: pass
    
    # Sort by memory usage and take top 20
    procs.sort(key=lambda x: x['memory_percent'] or 0, reverse=True)
    return jsonify({"processes": procs[:20]})

@app.route('/tool/kill', methods=['POST'])
def tool_kill():
    pid = request.json.get('pid')
    if not pid: return jsonify({"error": "PID required"}), 400
    try:
        p = psutil.Process(int(pid))
        p.terminate()
        return jsonify({"status": "Killed", "pid": pid})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tool/subnet', methods=['POST'])
def tool_subnet():
    # Fast Subnet Sweep
    base_ip = request.json.get('base_ip') # e.g. "192.168.1"
    if not base_ip: return jsonify({"error": "Base IP required"}), 400
    
    active_hosts = []
    lock = threading.Lock()

    def check_host(ip):
        try:
            # Fast ping (1 count, 200ms timeout)
            param = '-n' if sys.platform.lower()=='win32' else '-c'
            res = subprocess.run(['ping', param, '1', '-w', '200', ip], stdout=subprocess.DEVNULL)
            if res.returncode == 0:
                with lock:
                    active_hosts.append(ip)
        except: pass

    threads = []
    # Scan 1-254
    for i in range(1, 255):
        ip = f"{base_ip}.{i}"
        t = threading.Thread(target=check_host, args=(ip,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
        
    return jsonify({"hosts": sorted(active_hosts, key=lambda x: int(x.split('.')[-1]))})

# --- EXISTING PRO TOOLS ---
@app.route('/tool/portscan', methods=['POST'])
def tool_portscan():
    target = request.json.get('target')
    if not target: return jsonify({"error": "Target required"}), 400
    
    open_ports = []
    def scan_port(ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3) # Reduced timeout for speed
            if sock.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            sock.close()
        except: pass

    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 3306, 3389, 8080]
    threads = [threading.Thread(target=scan_port, args=(target, p)) for p in common_ports]
    for t in threads: t.start()
    for t in threads: t.join()
        
    return jsonify({"target": target, "open_ports": sorted(open_ports)})

@app.route('/tool/webaudit', methods=['POST'])
def tool_webaudit():
    url = request.json.get('url')
    if not url: return jsonify({"error": "URL required"}), 400
    if not url.startswith('http'): url = 'http://' + url
    try:
        r = requests.get(url, timeout=3)
        return jsonify({"url": url, "status": r.status_code, "headers": dict(r.headers)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tool/hash', methods=['POST'])
def tool_hash():
    text = request.json.get('text')
    return jsonify({
        "md5": hashlib.md5(text.encode()).hexdigest(),
        "sha256": hashlib.sha256(text.encode()).hexdigest()
    })

@app.route('/tool/vulnscan', methods=['POST'])
def tool_vulnscan():
    url = request.json.get('url')
    if not url: return jsonify({"error": "URL required"}), 400
    if not url.startswith('http'): url = 'http://' + url
    
    report = []
    try:
        # 1. Check for SQL Injection patterns in URL
        sqli_payloads = ["'", "\"", " OR 1=1", " UNION SELECT"]
        for p in sqli_payloads:
            try:
                r = requests.get(url + p, timeout=2)
                if "sql" in r.text.lower() or "database" in r.text.lower():
                    report.append(f"[CRITICAL] Possible SQLi with payload: {p}")
            except: pass

        # 2. Check for XSS (Reflected)
        xss_payload = "<script>alert(1)</script>"
        try:
            r = requests.get(url + "?q=" + xss_payload, timeout=2)
            if xss_payload in r.text:
                report.append("[HIGH] Reflected XSS found on ?q= parameter")
        except: pass

        # 3. Check Security Headers (Deep)
        try:
            r = requests.get(url, timeout=2)
            headers = r.headers
            if 'X-Frame-Options' not in headers: report.append("[MED] Missing X-Frame-Options (Clickjacking risk)")
            if 'Content-Security-Policy' not in headers: report.append("[LOW] Missing Content-Security-Policy")
            if 'Strict-Transport-Security' not in headers: report.append("[LOW] Missing HSTS")
        except: pass

        if not report: report.append("No obvious vulnerabilities found (Basic Scan).")
        
        return jsonify({"url": url, "report": report})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tool/scriptgen', methods=['POST'])
def tool_scriptgen():
    type_ = request.json.get('type')
    target = request.json.get('target') or "127.0.0.1"
    
    script = ""
    if type_ == 'portscan':
        script = f"""import socket
target = "{target}"
print(f"Scanning {{target}}...")
for port in [21, 22, 80, 443]:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    if s.connect_ex((target, port)) == 0:
        print(f"Port {{port}} is OPEN")
    s.close()"""
    elif type_ == 'ddos_sim':
        script = f"""import threading, requests
target = "{target}"
def attack():
    while True:
        try:
            requests.get(target)
            print("Request sent!")
        except: pass
for i in range(10):
    threading.Thread(target=attack).start()"""
    elif type_ == 'keylogger_sim':
        script = """# EDUCATIONAL PURPOSES ONLY
import keyboard
print("Listening for keystrokes (Press ESC to stop)...")
keyboard.wait('esc')
print("Stopped.")"""
    else:
        script = "# Unknown script type"

    return jsonify({"script": script})

# --- FACEBOOK SECURITY TOOLS (EDUCATIONAL) ---

@app.route('/tool/fb_phish_check', methods=['POST'])
def tool_fb_phish_check():
    url = request.json.get('url', '').lower()
    risk = "SAFE"
    reasons = []
    
    suspicious_domains = ['faceb00k', 'facbook', 'login-verify', 'secure-account', 'fb-update']
    if any(s in url for s in suspicious_domains):
        risk = "CRITICAL"
        reasons.append("Suspicious domain spoofing detected")
    if "facebook.com" not in url and "fb.com" not in url:
        risk = "HIGH"
        reasons.append("Not an official Facebook domain")
    if len(url) > 50:
        risk = "MEDIUM"
        reasons.append("Unusually long URL length")
        
    return jsonify({"url": url, "risk": risk, "reasons": reasons})

@app.route('/tool/fb_pass_audit', methods=['POST'])
def tool_fb_pass_audit():
    pwd = request.json.get('password', '')
    score = 0
    feedback = []
    
    if len(pwd) >= 12: score += 1
    else: feedback.append("Too short (aim for 12+ chars)")
    
    if re.search(r"[A-Z]", pwd): score += 1
    else: feedback.append("Missing uppercase letter")
    
    if re.search(r"[0-9]", pwd): score += 1
    else: feedback.append("Missing number")
    
    if re.search(r"[!@#$%^&*]", pwd): score += 1
    else: feedback.append("Missing special character")
    
    if "facebook" in pwd.lower() or "password" in pwd.lower():
        score = 0
        feedback = ["Contains common dictionary words"]
        
    return jsonify({"score": score, "max_score": 4, "feedback": feedback})

@app.route('/tool/fb_breach_check', methods=['POST'])
def tool_fb_breach_check():
    # Simulated breach check
    identity = request.json.get('identity', '')
    breached = hash(identity) % 5 == 0 # 20% chance of "breach" for demo
    return jsonify({
        "identity": identity,
        "found": breached,
        "source": "Simulated Dark Web Database" if breached else None
    })

@app.route('/tool/fb_2fa_sim', methods=['GET'])
def tool_fb_2fa_sim():
    # Simulate generating a 2FA code
    import random
    code = f"{random.randint(0,999999):06d}"
    return jsonify({"code": code, "expiry": "30 seconds"})

@app.route('/tool/fb_privacy_check', methods=['GET'])
def tool_fb_privacy_check():
    checklist = [
        {"id": 1, "task": "Set 'Who can see your future posts?' to Friends", "status": "Pending"},
        {"id": 2, "task": "Review 'Apps and Websites' permissions", "status": "Pending"},
        {"id": 3, "task": "Enable 'Profile Picture Guard'", "status": "Pending"},
        {"id": 4, "task": "Hide 'Friends List' from public", "status": "Pending"}
    ]
    return jsonify({"checklist": checklist})

if __name__ == '__main__':
    print("🚀 CyberGuardian ADVANCED Server Running...")
    app.run(host='0.0.0.0', port=5000)
