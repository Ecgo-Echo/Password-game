<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hệ Thống Bảo Mật Tuyệt Đối</title>
    <style>
        :root {
            --bg: #121212;
            --card: #1e1e1e;
            --text: #e0e0e0;
            --primary: #00ff41; /* Màu Matrix cho ngầu */
            --error: #ff4b2b;
        }

        body {
            background-color: var(--bg);
            color: var(--text);
            font-family: 'Segoe UI', Arial, sans-serif;
            display: flex;
            justify-content: center;
            padding: 40px 20px;
            margin: 0;
        }

        .container {
            background: var(--card);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            width: 100%;
            max-width: 550px;
        }

        .timer {
            font-size: 1.5rem;
            color: var(--primary);
            text-align: center;
            margin-bottom: 20px;
            font-family: monospace;
        }

        input {
            width: 100%;
            padding: 15px;
            background: #2d2d2d;
            border: 1px solid #444;
            color: white;
            border-radius: 8px;
            font-size: 1.1rem;
            box-sizing: border-box;
            outline: none;
        }

        input:focus { border-color: var(--primary); }

        .rules-list { margin-top: 20px; }

        .rule-card {
            background: #2a1010;
            border: 1px solid var(--error);
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 6px;
            font-size: 0.95rem;
            animation: fadeIn 0.4s ease;
        }

        .rule-card.done {
            background: #102a10;
            border-color: var(--primary);
            text-decoration: line-through;
            opacity: 0.6;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        #finalStep {
            display: none;
            margin-top: 30px;
            border-top: 2px dashed #444;
            padding-top: 20px;
        }

        button {
            width: 100%;
            padding: 15px;
            background: var(--primary);
            color: black;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            text-transform: uppercase;
            margin-top: 15px;
        }

        button:hover { background: #00cc33; }
    </style>
</head>
<body>

<div class="container">
    <h2 style="text-align:center">🔐 TRÌNH QUẢN LÝ MẬT KHẨU v2.0</h2>
    <div class="timer" id="displayTime">00:00</div>
    
    <p>Nhập mật khẩu của bạn:</p>
    <input type="text" id="pw" placeholder="Bắt đầu nhập..." autocomplete="off">

    <div class="rules-list" id="rulesBox"></div>

    <div id="finalStep">
        <h3>Xác nhận lại mật khẩu vừa tạo:</h3>
        <input type="password" id="pwConfirm" placeholder="Nhập lại y hệt nhé...">
        <button id="btnFinish">XÁC NHẬN HOÀN TẤT</button>
    </div>
</div>

<script>
    const pwInput = document.getElementById('pw');
    const rulesBox = document.getElementById('rulesBox');
    const finalStep = document.getElementById('finalStep');
    const displayTime = document.getElementById('displayTime');
    
    let seconds = 0;
    const startTime = Date.now();

    // Đồng hồ đếm thời gian
    setInterval(() => {
        seconds = Math.floor((Date.now() - startTime) / 1000);
        let m = Math.floor(seconds / 60).toString().padStart(2, '0');
        let s = (seconds % 60).toString().padStart(2, '0');
        displayTime.innerText = `${m}:${s}`;
    }, 1000);

    const checkList = [
        { id: 1, text: "Phải có ít nhất 8 ký tự.", check: s => s.length >= 8 },
        { id: 2, text: "Phải có ít nhất 1 chữ IN HOA.", check: s => /[A-Z]/.test(s) },
        { id: 3, text: "Phải có ít nhất 1 con số.", check: s => /[0-9]/.test(s) },
        { id: 4, text: "Phải có 1 ký tự đặc biệt (ví dụ: @, #, $).", check: s => /[!@#$%^&*]/.test(s) },
        { id: 5, text: "Phải chứa số La Mã (I, V, X, L, C, D, M).", check: s => /[IVXLCDM]/.test(s) },
        { id: 6, text: "Phải có tên 1 loài động vật (ví dụ: 'meo', 'cho', 'ga').", check: s => /(meo|cho|ga|lon|ho|voi|ran)/i.test(s) },
        { id: 7, text: "Tổng các chữ số trong mật khẩu phải bằng 25.", check: s => {
            let nums = s.match(/\d/g);
            return nums ? nums.reduce((a, b) => a + parseInt(b), 0) === 25 : false;
        }},
        { id: 8, text: "Mật khẩu phải chứa tên của tháng hiện tại (ví dụ: 'thang 2').", check: s => s.toLowerCase().includes("thang 2") },
        { id: 9, text: "Mật khẩu phải có độ dài là một số nguyên tố (ví dụ: 17, 19, 23...).", check: s => {
            let n = s.length;
            if (n < 2) return false;
            for(let i=2; i <= Math.sqrt(n); i++) if(n % i === 0) return false;
            return true;
        }},
        { id: 10, text: "Phải chứa câu thần chú: 'Toi dang phi thoi gian'.", check: s => s.includes("Toi dang phi thoi gian") }
    ];

    function updateRules() {
        const val = pwInput.value;
        rulesBox.innerHTML = '';
        let countDone = 0;

        for (let rule of checkList) {
            const isDone = rule.check(val);
            const div = document.createElement('div');
            div.className = `rule-card ${isDone ? 'done' : ''}`;
            div.innerText = `Yêu cầu #${rule.id}: ${rule.text}`;
            rulesBox.appendChild(div);

            if (isDone) countDone++;
            else break; // Chỉ hiện yêu cầu tiếp theo khi yêu cầu trước đã xong
        }

        if (countDone === checkList.length) {
            finalStep.style.display = 'block';
            pwInput.readOnly = true;
        } else {
            finalStep.style.display = 'none';
        }
    }

    pwInput.addEventListener('input', updateRules);

    document.getElementById('btnFinish').onclick = () => {
        if (document.getElementById('pwConfirm').value === pwInput.value) {
            const timeStr = displayTime.innerText;
            alert(`XÁC NHẬN THÀNH CÔNG!\nBạn đã lãng phí đúng ${timeStr} cuộc đời cho trò này.\nNhấn OK để nhận phần thưởng!`);
            window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"; // Rickroll thần thánh
        } else {
            alert("Mật khẩu xác nhận sai bét! Thử lại đi.");
        }
    };

    updateRules();
</script>

</body>
</html>