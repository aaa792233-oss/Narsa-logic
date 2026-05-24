<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Chart Tracker</title>
    <style>
        body { font-family: Arial; background-color: #eef2f3; text-align: center; padding-top: 30px; }
        .main-box { background: white; padding: 20px; width: 60%; margin: auto; box-shadow: 0px 4px 8px gray; border-radius: 10px; }
        input { padding: 10px; margin: 5px; width: 90px; text-align: center; border: 1px solid #ccc; }
        button { padding: 10px 20px; background: #28a745; color: white; border: none; cursor: pointer; font-size: 16px; border-radius: 5px;}
        table { margin: 20px auto; border-collapse: collapse; width: 100%; background: #ffdeb3; }
        th, td { border: 2px solid #d49c5e; padding: 15px; }
        .jodi { font-size: 30px; font-weight: bold; color: black; }
        .panel { font-size: 16px; line-height: 1.5; }
    </style>
</head>
<body>

    <div class="main-box">
        <h2>📊 डेटा ट्रॅकिंग सॉफ्टवेअर</h2>
        <input type="text" id="openP" placeholder="ओपन पॅनेल">
        <input type="number" id="jodiNum" placeholder="जोडी (Jodi)">
        <input type="text" id="closeP" placeholder="क्लोज पॅनेल">
        <button onclick="saveData()">सेव्ह करा</button>

        <table>
            <thead>
                <tr>
                    <th>ओपन पॅनेल</th>
                    <th>जोडी (Jodi)</th>
                    <th>क्लोज पॅनेल</th>
                </tr>
            </thead>
            <tbody id="tableBody">
            </tbody>
        </table>
    </div>

    <script>
        function saveData() {
            let op = document.getElementById("openP").value;
            let jodi = document.getElementById("jodiNum").value;
            let cp = document.getElementById("closeP").value;

            if(op === "" || jodi === "" || cp === "") {
                alert("कृपया सर्व रकाने भरा!");
                return;
            }

            let opFormat = op.split('').join('<br>');
            let cpFormat = cp.split('').join('<br>');

            let row = `<tr>
                <td class="panel">${opFormat}</td>
                <td class="jodi">${jodi}</td>
                <td class="panel">${cpFormat}</td>
            </tr>`;

            document.getElementById("tableBody").innerHTML += row;

            document.getElementById("openP").value = "";
            document.getElementById("jodiNum").value = "";
            document.getElementById("closeP").value = "";
        }
    </script>

</body>
</html>
