from flask import Flask, request, jsonify

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>First Meta</title>
<style>
body{margin:0;font-family:system-ui;background:#212121;color:white;display:flex;flex-direction:column;height:100vh}
.header{padding:15px;text-align:center;border-bottom:1px solid #444;font-weight:bold}
.chat{flex:1;overflow-y:auto;padding:20px}
.msg{margin:15px 0;padding:12px 16px;border-radius:12px;max-width:80%}
.user{background:#2f2f2f;align-self:flex-end;margin-left:auto}
.bot{background:#444654}
.input-box{display:flex;padding:15px;border-top:1px solid #444}
input{flex:1;padding:12px;border-radius:25px;border:1px solid #555;background:#2f2f2f;color:white;outline:none}
button{margin-left:10px;padding:12px 20px;border-radius:25px;border:none;background:white;color:black;font-weight:bold}
</style>
</head>
<body>
<div class="header">First Meta — Builder: Andrea Kisumu</div>
<div class="chat" id="chat">
<div class="msg bot">Hello! I am First Meta. How can I help you today? 🚀</div>
</div>
<div class="input-box">
<input id="inp" placeholder="Message First Meta...">
<button onclick="send()">Send</button>
</div>
<script>
function send(){
 let inp=document.getElementById('inp');
 let chat=document.getElementById('chat');
 if(!inp.value) return;
 chat.innerHTML+='<div class="msg user">'+inp.value+'</div>';
 let q=inp.value;
 inp.value='';
 fetch('/api/chat?q='+encodeURIComponent(q))
 .then(r=>r.text())
 .then(t=>{
   chat.innerHTML+='<div class="msg bot">'+t+'</div>';
   chat.scrollTop=chat.scrollHeight;
 });
 chat.scrollTop=chat.scrollHeight;
}
document.getElementById('inp').addEventListener('keydown',e=>{if(e.key==='Enter')send()});
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/api/chat')
def chat_api():
    q = request.args.get('q','')
    # For now simple reply - later we connect Groq
    return f"You said: {q}. First Meta is working! Builder Andrea Kisumu Version 2.4 is LIVE!"
