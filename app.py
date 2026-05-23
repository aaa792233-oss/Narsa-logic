import streamlit as st
import pandas as pd
from collections import Counter
import re

# पेजची सेटिंग
st.set_page_config(page_title="Smart Pattern Analyzer", layout="wide")
st.title("📊 स्मार्ट चार्ट पॅटर्न आणि रेकॉर्ड ॲनालिझर")
st.write("चार्टमधील जुन्या आकड्यांवरून 'हॉट आकडे' आणि 'लाईन' ओळखणारे टूल.")

# ---------------------------------------------------------
# १. डेटा इनपुट सेक्शन
# ---------------------------------------------------------
st.subheader("१. चार्टमधील आकडे टाका")
st.write("चार्टमधले शेवटचे काही आकडे स्पेस किंवा स्वल्पविराम (Comma) देऊन बॉक्समध्ये टाका. (उदा. 53, 48, 04, 83)")

# युझरकडून आकडे घेण्यासाठी बॉक्स
raw_data = st.text_area("येथे आकडे टाईप करा:", "53 48 04 83 79 14 36 98 75 37 97 68 95 13 95 51 34 18")

# ---------------------------------------------------------
# २. लॉजिक आणि ॲनालिसिस
# ---------------------------------------------------------
if st.button("पॅटर्न आणि अंदाज काढा"):
    if raw_data:
        # कचरा साफ करून फक्त आकडे काढणे
        cleaned_data = re.sub(r'[^0-9\s,]', ' ', raw_data).replace(',', ' ')
        numbers = [int(x) for x in cleaned_data.split() if x.isdigit()]
        
        if len(numbers) > 0:
            st.success(f"✅ सिस्टीमने एकूण {len(numbers)} आकडे विश्लेषणासाठी (Analysis) घेतले आहेत.")
            
            # --- पॅटर्न १: सर्वात जास्त आलेले आकडे ---
            count = Counter(numbers)
            most_common = count.most_common(5) # टॉप ५
            least_common = count.most_common()[-5:] # सर्वात कमी
            
            # --- पॅटर्न २: सिंगल डिजिट (ओपन/क्लोज) ॲनालिसिस ---
            single_digits = []
            for n in numbers:
                # दोन अंकी संख्येचे दोन भाग करणे (उदा. 53 -> 5 आणि 3)
                single_digits.extend([int(d) for d in str(n)])
            
            digit_count = Counter(single_digits)
            most_common_digits = digit_count.most_common(4)
            
            st.markdown("---")
            st.subheader("📈 चार्टचे विश्लेषण (Chart Analysis)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("🔥 हॉट आकडे (जे पुन्हा पुन्हा येत आहेत)")
                for num, freq in most_common:
                    st.write(f"जोडी **{num}** (आली: {freq} वेळा)")
                    
            with col2:
                st.warning("❄️ कोल्ड आकडे (जे खूप कमी आले आहेत)")
                for num, freq in least_common:
                    st.write(f"जोडी **{num}** (आली: {freq} वेळा)")

            # --- फायनल अंदाज (Prediction) ---
            st.markdown("---")
            st.subheader("🎯 पुढील आकड्याचा अंदाज (Probability Prediction)")
            st.write("जुन्या पॅटर्ननुसार सर्वात स्ट्राँग 'सिंगल' आकडे (Open/Close साठी):")
            
            c1, c2, c3, c4 = st.columns(4)
            if len(most_common_digits) >= 4:
                c1.success(f"पहिला चान्स: **{most_common_digits[0][0]}**")
                c2.success(f"दुसरा चान्स: **{most_common_digits[1][0]}**")
                c3.success(f"तिसरा चान्स: **{most_common_digits[2][0]}**")
                c4.success(f"चौथा चान्स: **{most_common_digits[3][0]}**")
                
            st.caption("टीप: हे ॲप जुन्या चार्टच्या गणितावर (Probability) आधारित सर्वात स्ट्राँग आकडे काढते. यामुळे अचूक अंदाज बांधायला मदत होईल.")
        else:
            st.error("कृपया बॉक्समध्ये योग्य आकडे टाका.")
