BHARAT JAN SUCHNA PORTAL — शुरुआती Home Page

महत्वपूर्ण:
यह एक स्वतंत्र सार्वजनिक सूचना मंच है, सरकारी वेबसाइट नहीं।
किसी भी सरकारी विभाग का लोगो/चिह्न या सरकारी होने का भ्रामक दावा न करें।
आँकड़ों और सूचनाओं के साथ मूल स्रोत तथा अपडेट की तारीख जोड़ें।

1) Python install करें।
2) इस folder में terminal खोलें।
3) चलाएँ:
   python -m venv venv
   Windows: venv\\Scripts\\activate
   Linux/Termux: source venv/bin/activate
   pip install -r requirements.txt
4) Firebase Console में Firestore Database बनाएँ।
5) Firebase Project Settings > Service Accounts से service-account JSON बनाएँ।
   इसे इसी folder में serviceAccountKey.json नाम से रखें।
   इस फाइल को GitHub/public hosting पर कभी upload न करें।
6) चलाएँ:
   python app.py
7) Browser में खोलें:
   http://127.0.0.1:5000

Firebase architecture:
- सभी Firebase Admin SDK imports और connection firebase.py में हैं।
- app.py केवल firebase.py के functions बुलाता है।
- HTML/CSS/JS में Firebase config या secret key नहीं है।
- Frontend केवल Flask के /api/stats और /api/notices endpoints से बात करता है।

Firestore collections:
1) portal_public / stats document:
   states: 36
   districts: "—" (सत्यापित संख्या डालें)
   villages: "—" (सत्यापित संख्या डालें)
   notices: 0

2) notices collection documents:
   title: "सूचना का शीर्षक"
   department: "विभाग का नाम"
   date: "DD-MM-YYYY"
   published: true
   created_at: Firestore Timestamp

सुरक्षा:
- serviceAccountKey.json निजी रखें और .gitignore में है।
- सार्वजनिक users को Firestore का सीधा write access न दें।
- Admin login, roles, validation और audit log अगला चरण है।
- अभी Search/Language/Login links केवल UI placeholders हैं; वे काम करने वाले फीचर नहीं हैं।
