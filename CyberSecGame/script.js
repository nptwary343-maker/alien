/*
  CyberGuardian Game Script
  Consolidated implementation of all modules and tools.
  Includes:
    - game core
    - phishingGame
    - passwordGame
    - firewallGame
    - terminalGame (with command templates)
    - pythonLab
    - proTools (including WiFi, Subnet, SysOps, Vulnerability Scanner, Script Generator)
*/

// Core Game Object
const game = {
    xp: 0,
    rank: 'NOOB',
    init() {
        this.updateStats();
    },
    startModule(moduleName) {
        document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
        document.getElementById('screen-' + moduleName).classList.add('active');
        // Initialize specific modules
        if (moduleName === 'phishing') phishingGame.start();
        if (moduleName === 'password') passwordGame.start();
        if (moduleName === 'firewall') firewallGame.start();
        if (moduleName === 'terminal') terminalGame.init();
        if (moduleName === 'python') pythonLab.init();
        if (moduleName === 'protools') proTools.init();
    },
    showMenu() {
        document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
        document.getElementById('screen-menu').classList.add('active');
        firewallGame.stop(); // Ensure firewall stops when returning to menu
    },
    addXP(amount) {
        this.xp += amount;
        this.updateStats();
    },
    updateStats() {
        document.getElementById('player-xp').innerText = this.xp;
        if (this.xp > 1000) this.rank = 'ELITE HACKER';
        else if (this.xp > 500) this.rank = 'WHITE HAT';
        else if (this.xp > 100) this.rank = 'SCRIPT KIDDIE';
        else this.rank = 'NOOB';
        document.getElementById('player-rank').innerText = this.rank;
    }
};

// Phishing Game
const phishingGame = {
    emails: [
        { sender: 'security@google.com', subject: 'Login Alert', body: 'New login from Windows PC.', isPhish: false },
        { sender: 'admin@paypa1.com', subject: 'Account Suspended', body: 'Click here to verify identity.', isPhish: true },
        { sender: 'hr@company.com', subject: 'Payroll Update', body: 'Please review the attached PDF.', isPhish: false },
        { sender: 'support@amaz0n-verify.net', subject: 'Order #1234', body: 'Your order is on hold. Update payment.', isPhish: true },
        { sender: 'ceo@company.com', subject: 'Urgent Transfer', body: 'Need you to buy gift cards ASAP.', isPhish: true }
    ],
    start() {
        this.nextEmail();
        document.getElementById('phishing-feedback').innerText = '';
    },
    nextEmail() {
        const idx = Math.floor(Math.random() * this.emails.length);
        const email = this.emails[idx];
        document.getElementById('email-sender').innerText = email.sender;
        document.getElementById('email-subject').innerText = email.subject;
        document.getElementById('email-body').innerText = email.body;
        this.currentEmail = email;
    },
    decide(isAccept) {
        const correct = !this.currentEmail.isPhish;
        const feedback = document.getElementById('phishing-feedback');
        if (isAccept === correct) {
            feedback.innerText = 'CORRECT! +10 XP';
            feedback.className = 'feedback correct';
            game.addXP(10);
        } else {
            feedback.innerText = 'WRONG! Security Breach!';
            feedback.className = 'feedback wrong';
        }
        setTimeout(() => {
            feedback.innerText = '';
            this.nextEmail();
        }, 1500);
    }
};

// Password Game
const passwordGame = {
    pairs: [
        { a: 'password123', b: 'Tr0ub4dor&3', winner: 2 },
        { a: 'correcthorsebatterystaple', b: 'P@ss', winner: 1 },
        { a: 'admin', b: '4dm1n$tr@t0r', winner: 2 },
        { a: 'MyDogName', b: 'K9#L0v3r!', winner: 2 }
    ],
    start() {
        this.nextPair();
        document.getElementById('password-feedback').innerText = '';
    },
    nextPair() {
        const idx = Math.floor(Math.random() * this.pairs.length);
        this.currentPair = this.pairs[idx];
        document.getElementById('pass-opt-1').innerText = this.currentPair.a;
        document.getElementById('pass-opt-2').innerText = this.currentPair.b;
    },
    check(choice) {
        const feedback = document.getElementById('password-feedback');
        const term = document.getElementById('password-terminal');
        if (choice === this.currentPair.winner) {
            feedback.innerText = 'ACCESS GRANTED +15 XP';
            feedback.className = 'feedback correct';
            term.innerHTML += `<div>> PASS_CHECK: STRONG [OK]</div>`;
            game.addXP(15);
        } else {
            feedback.innerText = 'WEAK PASSWORD CRACKED!';
            feedback.className = 'feedback wrong';
            term.innerHTML += `<div>> PASS_CHECK: WEAK [FAIL]</div>`;
        }
        term.scrollTop = term.scrollHeight;
        setTimeout(() => {
            feedback.innerText = '';
            this.nextPair();
        }, 1500);
    }
};

// Firewall Game
const firewallGame = {
    active: false,
    score: 0,
    interval: null,
    start() {
        this.active = true;
        this.score = 0;
        document.getElementById('fw-score').innerText = 0;
        document.getElementById('firewall-grid').innerHTML = '';
        this.interval = setInterval(() => {
            if (!this.active) return;
            this.spawnPacket();
        }, 1000);
    },
    stop() {
        this.active = false;
        clearInterval(this.interval);
        const grid = document.getElementById('firewall-grid');
        if (grid) grid.innerHTML = '';
    },
    spawnPacket() {
        const grid = document.getElementById('firewall-grid');
        const packet = document.createElement('div');
        const isMalicious = Math.random() > 0.5;
        packet.className = `packet ${isMalicious ? 'malicious' : 'safe'}`;
        packet.style.left = Math.floor(Math.random() * 80) + 10 + '%';
        packet.style.top = '0%';
        let top = 0;
        const anim = setInterval(() => {
            if (!this.active) { clearInterval(anim); return; }
            top += 2;
            packet.style.top = top + '%';
            if (top > 90) {
                clearInterval(anim);
                if (packet.parentNode) packet.parentNode.removeChild(packet);
                if (isMalicious && this.active) game.addXP(-5);
            }
        }, 50);
        packet.onclick = () => {
            if (isMalicious) {
                game.addXP(5);
                this.score += 5;
                document.getElementById('fw-score').innerText = this.score;
            } else {
                game.addXP(-5);
            }
            clearInterval(anim);
            if (packet.parentNode) packet.parentNode.removeChild(packet);
        };
        grid.appendChild(packet);
    }
};

// Terminal Game
const terminalGame = {
    input: null,
    output: null,
    init() {
        this.input = document.getElementById('term-input');
        this.output = document.getElementById('term-output');
        this.input.addEventListener('keydown', e => {
            if (e.key === 'Enter') {
                this.execute(this.input.value);
                this.input.value = '';
            }
        });
        this.input.focus();
    },
    print(text, type = 'normal') {
        const div = document.createElement('div');
        div.innerText = text;
        if (type === 'response') div.className = 'cmd-response';
        if (type === 'error') div.className = 'cmd-error';
        this.output.appendChild(div);
        this.output.scrollTop = this.output.scrollHeight;
    },
    async execute(cmd) {
        this.print(`root@kali:~# ${cmd}`);
        const args = cmd.trim().split(' ');
        const command = args[0].toLowerCase();
        if (command === 'help') {
            this.print('Available Commands:', 'response');
            this.print('  [REAL SYSTEM COMMANDS ENABLED]');
            this.print('  nmap, ping, ipconfig, dir, etc.');
            this.print('  ask_ai <query>  - Ask CyberAI');
            this.print('  clear           - Clear terminal');
            this.print('  exit            - Return to menu');
            return;
        }
        if (command === 'clear') { this.output.innerHTML = ''; return; }
        if (command === 'exit') { game.showMenu(); return; }
        if (command === 'ask_ai') {
            const query = args.slice(1).join(' ');
            this.print(`CyberAI: Analyzing "${query}"...`, 'response');
            this.print('> TIP: Ensure input validation is strict.');
            return;
        }
        // Forward to backend
        try {
            const res = await fetch('http://localhost:5000/run_command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: cmd })
            });
            const data = await res.json();
            if (data.error) this.print(`Error: ${data.error}`, 'error');
            else {
                if (data.stdout) this.print(data.stdout);
                if (data.stderr) this.print(data.stderr, 'error');
            }
        } catch (e) {
            this.print('Connection Error: Is server.py running?', 'error');
        }
    },
    loadTemplate() {
        const select = document.getElementById('cmd-template');
        const val = select.value;
        if (val) { this.input.value = val; this.input.focus(); }
    }
};

// Python Lab
const pythonLab = {
    init() { },
    async run() {
        const code = document.getElementById('python-code').value;
        const out = document.getElementById('python-output');
        out.innerHTML = '<div>> Running script...</div>';
        try {
            const res = await fetch('http://localhost:5000/run_python', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code })
            });
            const data = await res.json();
            if (data.error) out.innerHTML += `<div class="cmd-error">${data.error}</div>`;
            else {
                if (data.stdout) out.innerHTML += `<div class="cmd-response">${data.stdout.replace(/\n/g, '<br>')}</div>`;
                if (data.stderr) out.innerHTML += `<div class="cmd-error">${data.stderr.replace(/\n/g, '<br>')}</div>`;
            }
        } catch (e) {
            out.innerHTML += '<div class="cmd-error">Connection Error: Is server.py running?</div>';
        }
    }
};

// Pro Tools (advanced utilities)
const proTools = {
    init() { this.show('scan'); },
    show(toolId) {
        document.querySelectorAll('.tool-panel').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.tool-tab').forEach(t => t.classList.remove('active'));
        const panel = document.getElementById('tool-' + toolId);
        if (panel) panel.classList.add('active');
        const tabs = document.querySelectorAll('.tool-tab');
        const map = { scan: 0, wifi: 1, subnet: 2, sys: 3, vuln: 4, script: 5, audit: 6, hash: 7 };
        if (map[toolId] !== undefined && tabs[map[toolId]]) tabs[map[toolId]].classList.add('active');
    },
    async runWifi() {
        const out = document.getElementById('wifi-output');
        out.innerText = '> Scanning Airwaves (netsh)...';
        try {
            const res = await fetch('http://localhost:5000/tool/wifi');
            const data = await res.json();
            out.innerText = data.error ? `Error: ${data.error}` : data.raw;
        } catch { out.innerText = 'Connection Error'; }
    },
    async runSubnet() {
        const base = document.getElementById('subnet-ip').value;
        const out = document.getElementById('subnet-output');
        out.innerText = `> Sweeping ${base}.1-254... (Fast Mode)`;
        try {
            const res = await fetch('http://localhost:5000/tool/subnet', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ base_ip: base })
            });
            const data = await res.json();
            if (data.error) out.innerText = `Error: ${data.error}`;
            else {
                out.innerText = `Active Hosts on ${base}.x:\n`;
                if (data.hosts.length === 0) out.innerText += 'No hosts found.';
                else data.hosts.forEach(h => out.innerText += `[+] ${h} IS UP\n`);
            }
        } catch { out.innerText = 'Connection Error'; }
    },
    async runSys() {
        const out = document.getElementById('sys-output');
        out.innerText = '> Fetching Process List...';
        try {
            const res = await fetch('http://localhost:5000/tool/processes');
            const data = await res.json();
            out.innerText = 'TOP 20 MEMORY CONSUMERS:\nPID   | MEM% | NAME\n--------------------------\n';
            data.processes.forEach(p => {
                out.innerText += `${String(p.pid).padEnd(6)}| ${p.memory_percent.toFixed(1).padEnd(5)}| ${p.name}\n`;
            });
        } catch { out.innerText = 'Connection Error'; }
    },
    async killProc() {
        const pid = document.getElementById('kill-pid').value;
        if (!pid) return;
        try {
            const res = await fetch('http://localhost:5000/tool/kill', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pid })
            });
            const data = await res.json();
            if (data.error) alert(`Error: ${data.error}`);
            else { alert(`PID ${pid} Killed!`); this.runSys(); }
        } catch { alert('Connection Error'); }
    },
    async runScan() {
        const target = document.getElementById('scan-target').value;
        const out = document.getElementById('scan-output');
        out.innerText = `> Scanning ${target}... (May take 10-20s)`;
        try {
            const res = await fetch('http://localhost:5000/tool/portscan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target })
            });
            const data = await res.json();
            if (data.error) out.innerText = `Error: ${data.error}`;
            else {
                out.innerText = `Scan Complete at ${data.scan_time}\nTarget: ${data.target}\n\nOPEN PORTS:\n`;
                if (data.open_ports.length === 0) out.innerText += 'No common open ports found.';
                else data.open_ports.forEach(p => out.innerText += `[+] Port ${p} OPEN\n`);
            }
        } catch { out.innerText = 'Connection Error.'; }
    },
    async runAudit() {
        const target = document.getElementById('audit-target').value;
        const out = document.getElementById('audit-output');
        out.innerText = `> Auditing ${target}...`;
        try {
            const res = await fetch('http://localhost:5000/tool/webaudit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: target })
            });
            const data = await res.json();
            if (data.error) out.innerText = `Error: ${data.error}`;
            else {
                out.innerText = `Target: ${data.url}\nStatus: ${data.status}\n\nSECURITY HEADERS:\n`;
                for (const [k, v] of Object.entries(data.audit)) out.innerText += `${k}: ${v}\n`;
            }
        } catch { out.innerText = 'Connection Error.'; }
    },
    async runHash() {
        const text = document.getElementById('hash-input').value;
        const out = document.getElementById('hash-output');
        try {
            const res = await fetch('http://localhost:5000/tool/hash', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            const data = await res.json();
            if (data.error) out.innerText = `Error: ${data.error}`;
            else out.innerText = `MD5:\n${data.md5}\n\nSHA256:\n${data.sha256}`;
        } catch { out.innerText = 'Connection Error.'; }
    },
    async runVuln() {
        const target = document.getElementById('vuln-target').value;
        const out = document.getElementById('vuln-output');
        out.innerText = `> Scanning ${target} for vulnerabilities...`;
        try {
            const res = await fetch('http://localhost:5000/tool/vulnscan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: target })
            });
            const data = await res.json();
            if (data.error) out.innerText = `Error: ${data.error}`;
            else {
                out.innerText = `SCAN REPORT FOR: ${data.url}\n\n`;
                data.report.forEach(line => out.innerText += line + '\n');
            }
        } catch { out.innerText = 'Connection Error.'; }
    },
    async runScriptGen() {
        const type = document.getElementById('script-type').value;
        const target = document.getElementById('script-target').value;
        const out = document.getElementById('script-output');
        out.value = '# Generating script...';
        try {
            const res = await fetch('http://localhost:5000/tool/scriptgen', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type, target })
            });
            const data = await res.json();
            out.value = data.script;
        } catch { out.value = '# Connection Error.'; }
    }
};

// Initialize on page load
window.addEventListener('load', () => {
    game.init();
});
