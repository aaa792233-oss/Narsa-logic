import streamlit as st
import pytesseract
from PIL import Image
import sympy as sp
import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------
# १. स्वतःचे मॅथ आणि लॉजिक इंजिन (Custom Logic Engine)
# ---------------------------------------------------------
def solve_math(expression):
    try:
        expr = sp.sympify(expression) 
        result = expr.evalf()
        return f"उत्तर: {result}"
    except Exception as e:
        return "त्रुटी: कृपया योग्य गणिती सूत्र द्या (उदा. 25 * 4 + 10)."

def solve_sequence(seq_str):
    try:
        numbers = [float(x.strip()) for x in seq_str.split(',')]
        if len(numbers) < 3:
            return "पॅटर्न ओळखण्यासाठी किमान ३ अंक द्या."
        
        diff1 = [numbers[i+1] - numbers[i] for i in range(len(numbers)-1)]
        
        if len(set(diff1)) == 1:
            next_num = numbers[-1] + diff1[0]
            return f"पुढील अंक: {next_num} (लॉजिक: प्रत्येक अंकात {diff1[0]} चा फरक आहे)"
        
        diff2 = [diff1[i+1] - diff1[i] for i in range(len(diff1)-1)]
        if len(set(diff2)) == 1:
            next_diff = diff1[-1] + diff2[0]
            next_num = numbers[-1] + next_diff
            return f"पुढील अंक: {next_num} (लॉजिक: फरकांचा फरक {diff2[0]} ने वाढत आहे)"

        return "हा एक अत्यंत गुंतागुंतीचा पॅटर्न आहे. सध्या इंजिन फक्त साधे आणि दुहेरी फरक ओळखते."
    except Exception:
        return "त्रुटी: कृपया अंक स्वल्पविरामाने (comma) वेगळे करून लिहा (उदा. 2, 5, 10, 17)."

# ---------------------------------------------------------
# २. फोटो स्कॅनर (Offline OCR)
# ---------------------------------------------------------
def scan_image(image):
    try:
        text = pytesseract.image_to_string(image)
        return text if text.strip() else "फोटोमध्ये कोणतेही आकडे किंवा मजकूर आढळला नाही."
    except Exception as e:
        return "त्रुटी: स्कॅनिंग अयशस्वी. Tesseract-OCR बरोबर इन्स्टॉल केले आहे का तपासा."

# ---------------------------------------------------------
# ३. वेब ऑटोमेशन / स्क्रॅपिंग (URL Data Fetcher)
# ---------------------------------------------------------
def fetch_web_data(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        text = soup.get_text(separator=' ', strip=True)
        return text[:1000] + "...\n\n(डेटा खूप मोठा असल्याने फक्त सुरुवातीचा भाग दाखवला आहे.)"
    except Exception as e:
        return "त्रुटी: लिंक वाचता आली नाही. लिंक योग्य असल्याची खात्री करा."

# ---------------------------------------------------------
# ४. ॲपचा यूझर इंटरफेस (UI Design)
# ---------------------------------------------------------
st.set_page_config(page_title="स्मार्ट लॉजिक टूल", layout="centered")
st.title("स्मार्ट लॉजिक आणि कॅल्क्युलेटर टूल 🚀")
st.write("बाहेरील AI शिवाय चालणारे स्वतःचे इंजिन (Math, Logic, OCR & Web Data)")

tab1, tab2, tab3, tab4 = st.tabs(["🧮 गणित (Math)", "🔢 अंकमालिका (Pattern)", "🖼️ फोटो स्कॅन", "🌐 वेब लिंक"])

with tab1:
    st.subheader("समीकरणे आणि गणित सोडवा")
    math_input = st.text_input("गणित टाका (उदा. (50+25)/5 * 2):")
    if st.button("गणित सोडवा"):
        st.info(solve_math(math_input))

with tab2:
    st.subheader("अंकांमधील फरक आणि मालिका ओळखा")
    seq_input = st.text_input("मालिका टाका (उदा. 2, 5, 10, 17):")
    if st.button("पॅटर्न आणि पुढील अंक शोधा"):
        st.info(solve_sequence(seq_input))

with tab3:
    st.subheader("गणिताचा किंवा आकड्यांचा फोटो अपलोड करा")
    img_file = st.file_uploader("फोटो निवडा (JPG/PNG)", type=['png', 'jpg', 'jpeg'])
    if img_file is not None:
        image = Image.open(img_file)
        st.image(image, caption="अपलोड केलेला फोटो", width=300)
        if st.button("फोटोमधील आकडे वाचा"):
            extracted_text = scan_image(image)
            st.success("स्कॅन केलेला डेटा:")
            st.code(extracted_text)

with tab4:
    st.subheader("वेबसाईटवरील डेटा गोळा करा")
    url_input = st.text_input("येथे लिंक (URL) पेस्ट करा:")
    if st.button("डेटा आणा"):
        with st.spinner('डेटा गोळा करत आहे...'):
            web_data = fetch_web_data(url_input)
            st.success("वेबसाईटवरील डेटा:")
            st.text_area("निकाल", web_data, height=200)
