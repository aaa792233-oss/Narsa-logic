import streamlit as st
import requests
from bs4 import BeautifulSoup
import sympy as sp
import re

# पेज कॉन्फिगरेशन
st.set_page_config(page_title="Custom URL Math Automation", layout="wide")
st.title("🌐 कस्टम लिंक डेटा आणि ऑटोमेशन कॅल्क्युलेटर")
st.write("तू टाकलेल्या कोणत्याही लिंकवरील डेटा आणि गणिताची सूत्रे एकत्र करून उत्तर काढणारे इंजिन.")

# टॅब्स
tab1, tab2 = st.tabs(["🔗 लिंक + गणित ऑटोमेशन (URL Math)", "🧮 डायरेक्ट कॅल्क्युलेटर"])

# ---------------------------------------------------------
# १. लिंक डेटा आणि गणित ऑटोमेशन इंजिन
# ---------------------------------------------------------
with tab1:
    st.subheader("कोणतीही लिंक टाका आणि त्यावरील डेटावर गणित चालवा")
    
    # यूझर इनपुट - लिंक आणि सूत्र
    target_url = st.text_input("ज्या साईटवरून डेटा हवा आहे, ती लिंक (URL) येथे टाका:")
    user_formula = st.text_input("या डेटावर कोणते गणित किंवा सूत्र वापरायचे आहे? (उदा. Total * 2, किंवा थेट समीकरण):")
    
    if st.button("डेटा गोळा करून गणित सोडवा"):
        if target_url:
            with st.spinner("दिलेल्या लिंकवरून डेटा आणि आकडे गोळा करत आहे..."):
                try:
                    # १. वेब ऑटोमेशन - साईटवरून डेटा काढणे
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                    response = requests.get(target_url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        page_text = soup.get_text(separator=' ', strip=True)
                        
                        # २. डेटा मधून सर्व आकडे (Numbers) शोधून काढणे
                        found_numbers = [float(n) for n in re.findall(r'[-+]?\d*\.\d+|\d+', page_text)]
                        
                        if found_numbers:
                            st.success("✅ साईटवरून डेटा यशस्वीपणे गोळा केला!")
                            
                            # स्क्रीनवर सापडलेले आकडे दाखवणे
                            st.write(f"📊 **साईटवर सापडलेले एकूण आकडे:** {found_numbers[:10]}... (पहिले काही आकडे)")
                            total_sum = sum(found_numbers)
                            max_val = max(found_numbers)
                            min_val = min(found_numbers)
                            count_val = len(found_numbers)
                            
                            st.info(f"📈 **डेटा विश्लेषण:** एकूण आकडे: {count_val} | बेरीज: {total_sum} | सर्वात मोठा अंक: {max_val}")
                            
                            # ३. गणिताचे सूत्र वापरून उत्तर काढणे
                            try:
                                # जर यूझरने स्वतःचे सूत्र दिले असेल (उदा. Total * 2)
                                if user_formula:
                                    # सूत्रातील 'Total' किंवा 'total' शब्दाला एकूण बेरजेने बदलणे
                                    parsed_formula = user_formula.lower().replace('total', str(total_sum))
                                    expr = sp.sympify(parsed_formula)
                                    final_ans = expr.evalf()
                                    st.success(f"🎯 **तुमच्या सूत्रानुसार फायनल उत्तर:** {final_ans}")
                                else:
                                    # जर सूत्र दिले नसेल तर साईटवरील डेटा मधील सर्व गणिते (उदा. 25+50) ऑटो-सर्च करून सोडवणे
                                    st.warning("तुम्ही कोणतेही सूत्र दिले नाही, म्हणून साईटवरील आकड्यांची एकूण बेरीज केली आहे.")
                                    st.success(f"🎯 **एकूण बेरीज उत्तर (Total Sum):** {total_sum}")
                                    
                            except Exception:
                                st.error("त्रुटी: तुम्ही दिलेले गणिताचे सूत्र योग्य नाही. कृपया साधे सूत्र द्या (उदा. Total * 5).")
                        else:
                            st.warning("या साईटवर कोडिंगला वापरण्यासारखे कोणतेही आकडे किंवा संख्या सापडल्या नाहीत.")
                    else:
                        st.error(f"साईटकडून डेटा मिळाला नाही. एरर कोड: {response.status_code}")
                except Exception as e:
                    st.error("वेब ऑटोमेशन फेल झाले! लिंक योग्य असल्याची आणि इंटरनेट चालू असल्याची खात्री करा.")
        else:
            st.warning("कृपया आधी साईटची लिंक (URL) टाका.")

# ---------------------------------------------------------
# २. डायरेक्ट कॅल्क्युलेटर टॅब
# ---------------------------------------------------------
with tab2:
    st.subheader("थेट गणिते आणि समीकरणे सोडवा")
    direct_math = st.text_input("गणित टाईप करा (उदा. (50+25)/5 * 10):")
    if st.button("थेट उत्तर काढा"):
        if direct_math:
            try:
                expr = sp.sympify(direct_math)
                st.success(f"🎯 **उत्तर:** {expr.evalf()}")
            except Exception:
                st.error("कृपया योग्य गणिती सूत्र टाका.")
