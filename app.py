import streamlit as st
import pytesseract
from PIL import Image, ImageOps
import numpy as np
import re
import math

# पेज कॉन्फिगरेशन
st.set_page_config(page_title="AI Smart Grid Solver", layout="wide")
st.title("🤖 AI स्मार्ट ग्रिड आणि ऑटोमेशन सॉल्वर")
st.write("अॅक्टिव्ह रिकॉल: फोटो अपलोड करा, रिकाम्या जागा आपोआप ओळखून टेबल सोडवले जाईल.")

tab1, tab2 = st.tabs(["🖼️ ऑटोमॅटिक फोटो सॉल्वर", "🧮 ॲडव्हान्स गणित"])

# ---------------------------------------------------------
# कोर लॉजिक - सुडोकू सॉल्वर (Dynamic N x N)
# ---------------------------------------------------------
def is_valid(board, row, col, num, N, sub_size):
    for i in range(N):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = sub_size * (row // sub_size), sub_size * (col // sub_size)
    for i in range(sub_size):
        for j in range(sub_size):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    N = len(board)
    if N == 0: return True 
    sub_size = int(math.isqrt(N))
    
    for row in range(N):
        for col in range(N):
            if board[row][col] == 0:
                for num in range(1, N + 1):
                    if is_valid(board, row, col, num, N, sub_size):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

# ---------------------------------------------------------
# OCR आणि इंटेलिजेंट डेटा प्रोसेसिंग
# ---------------------------------------------------------
def process_image_and_solve(image):
    gray_image = ImageOps.grayscale(image)
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    extracted_text = pytesseract.image_to_string(gray_image, config=custom_config)
    
    cleaned_data = re.sub(r'[^0-9\s]', '', extracted_text)
    raw_numbers = cleaned_data.split()
    
    digits = []
    for item in raw_numbers:
        for char in item:
            digits.append(int(char))
            
    total_digits = len(digits)
    if total_digits == 0:
        return None, "फोटोमध्ये कोणतेही आकडे सापडले नाहीत."
        
    N = int(math.sqrt(total_digits))
    
    if N * N != total_digits or N not in [4, 9, 16]:
        if total_digits <= 16: N = 4
        elif total_digits <= 81: N = 9
        else: N = 16
        
        if len(digits) < N*N:
            digits.extend([0] * (N*N - len(digits)))
        else:
            digits = digits[:N*N]
            
    board = np.array(digits).reshape(N, N).tolist()
    return board, None

# ---------------------------------------------------------
# व्हिज्युअल ग्रिड बनवणारे फंक्शन (HTML/CSS)
# ---------------------------------------------------------
def draw_grid(original_board, solved_board):
    N = len(solved_board)
    sub_size = int(math.isqrt(N))
    
    html = '<table style="border-collapse: collapse; margin: 20px auto; font-family: sans-serif;">'
    for row in range(N):
        html += '<tr>'
        for col in range(N):
            val = solved_board[row][col]
            orig_val = original_board[row][col]
            
            # अॅक्टिव्ह रिकॉल: रिकाम्या (0) जागा शोधून तिथे वेगळा रंग देणे
            if orig_val == 0:
                text_color = "#007BFF" # AI ने शोधलेले उत्तर निळ्या रंगात
                bg_color = "#E6F2FF"   # बॅकग्राऊंड हलका निळा
                display_val = f"<b>{val}</b>"
            else:
                text_color = "#333333" # मूळ आकडे काळ्या रंगात
                bg_color = "#FFFFFF"
                display_val = str(val)
                
            # बॉर्डर जाड करणे (Subgrid नुसार)
            border_top = "2px solid black" if row % sub_size == 0 else "1px solid #ccc"
            border_left = "2px solid black" if col % sub_size == 0 else "1px solid #ccc"
            border_bottom = "2px solid black" if row == N-1 else ""
            border_right = "2px solid black" if col == N-1 else ""
            
            style = f"border-top: {border_top}; border-left: {border_left}; border-bottom: {border_bottom}; border-right: {border_right}; padding: 15px 20px; text-align: center; font-size: 22px; color: {text_color}; background-color: {bg_color}; width: 50px; height: 50px;"
            
            html += f'<td style="{style}">{display_val}</td>'
        html += '</tr>'
    html += '</table>'
    return html

# ---------------------------------------------------------
# १. ऑटोमॅटिक फोटो सॉल्वर टॅब
# ---------------------------------------------------------
with tab1:
    st.subheader("फोटो अपलोड करा आणि रिकाम्या जागा भरा")
    
    uploaded_file = st.file_uploader("फोटो निवडा...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="अपलोड केलेला फोटो", width=300)
        
        if st.button("ऑटो-सॉल्व्ह आणि डिझाईन करा"):
            with st.spinner("AI फोटोचे विश्लेषण करत आहे आणि रिकाम्या जागा शोधत आहे..."):
                board, error = process_image_and_solve(image)
                
                if error:
                    st.error(error)
                else:
                    N = len(board)
                    original_board = [row[:] for row in board] # मूळ बोर्ड सेव्ह करणे (Active Recall साठी)
                    
                    st.write(f"🧩 **फोटोवरून ओळखलेले मूळ {N}x{N} टेबल (रिकाम्या जागा 0):**")
                    st.markdown(draw_grid(original_board, original_board), unsafe_allow_html=True)
                        
                    solved_board = [row[:] for row in board]
                    if solve_sudoku(solved_board):
                        st.success("✅ AI ने रिकाम्या जागा यशस्वीपणे शोधल्या आहेत!")
                        st.write("🏁 **फायनल उत्तर (निळ्या रंगात AI ने शोधलेले आकडे):**")
                        # इथे मूळ बोर्ड आणि सोडवलेला बोर्ड पास करून रंग बदलले जातील
                        st.markdown(draw_grid(original_board, solved_board), unsafe_allow_html=True)
                    else:
                        st.error("❌ या टेबलचे लॉजिकल उत्तर काढणे शक्य नाही. फोटो अस्पष्ट असू शकतो.")

# ---------------------------------------------------------
# २. डायरेक्ट गणित टॅब
# ---------------------------------------------------------
with tab2:
    st.subheader("थेट गणित सोडवा")
    import sympy as sp
    math_expr = st.text_input("गणित टाका (उदा. sin(45) * 100):")
    if st.button("उत्तर काढा"):
        try:
            expr = sp.sympify(math_expr)
            st.success(f"उत्तर: {expr.evalf()}")
        except Exception:
            st.error("योग्य सूत्र द्या.")
