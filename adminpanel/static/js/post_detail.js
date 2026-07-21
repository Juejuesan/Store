.review-page{
padding:30px;
animation:fade .6s;
}

.review-header{
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:30px;
}

.review-header h1{
font-size:34px;
font-weight:700;
color:#2563eb;
}

.review-grid{
display:grid;
grid-template-columns:1.3fr 1fr;
gap:30px;
margin-bottom:30px;
}

.image-card,
.info-card,
.description-card{
background:white;
border-radius:20px;
padding:25px;
box-shadow:0 15px 40px rgba(0,0,0,.08);
}

.main-image{
width:100%;
height:500px;
object-fit:cover;
border-radius:18px;
transition:.4s;
}

.main-image:hover{
transform:scale(1.02);
}

.badge{
display:inline-block;
background:#fef3c7;
color:#b45309;
padding:8px 18px;
border-radius:30px;
font-weight:600;
margin-bottom:20px;
}

.info-row{
display:flex;
justify-content:space-between;
padding:18px 0;
border-bottom:1px solid #edf2f7;
}

.description-card h3{
margin-bottom:15px;
color:#2563eb;
}

.description-card p{
line-height:1.9;
color:#555;
}

.action-area{
display:flex;
justify-content:center;
gap:20px;
margin-top:35px;
}

.approve-btn,
.reject-btn,
.back-btn{
padding:16px 34px;
border-radius:50px;
font-size:16px;
font-weight:600;
text-decoration:none;
transition:.35s;
}

.approve-btn{
background:#22c55e;
color:white;
}

.approve-btn:hover{
transform:translateY(-4px);
box-shadow:0 15px 35px rgba(34,197,94,.3);
}

.reject-btn{
background:#ef4444;
color:white;
}

.reject-btn:hover{
transform:translateY(-4px);
box-shadow:0 15px 35px rgba(239,68,68,.3);
}

.back-btn{
background:#2563eb;
color:white;
}

.back-btn:hover{
background:#1d4ed8;
}

@keyframes fade{
from{
opacity:0;
transform:translateY(30px);
}
to{
opacity:1;
transform:translateY(0);
}
}