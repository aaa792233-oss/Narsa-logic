import streamlit as st
import pytesseract
from PIL import Image
import sympy as sp
import requests
from bs4 import BeautifulSoup
import math

st.set_page_config(page_title="Pro Logic & Grid Solver", layout="wide")
st.title("🧠 प्रो लॉजिक, सुडोकू आणि ऑटोमेशन टूल")
st.write("कोणत्याही साईझचे टेबल लॉजिक, वेब डेटा आणि ॲडव्हान्स गणित सोडवणारे स्मार्ट इंजिन.")

tab1, tab2, tab3, tab4 = st.tabs(["🧩 डायनॅमिक सुडोकू/टेबल", "🖼️ फोटो स्कॅनर", "🌐 वेब डेटा", "🧮 ॲडव्हान्स गणित"])

# ---------------------------------------------------------
# १. डायनॅमिक सुडोकू आणि टेबल लॉजिक इंजिन (कोणत्याही साईझसाठी)
# ---------------------------------------------------------
def is_valid(board, row, col, num, N, sub_size):
    # ओळ आणि स्तंभ चेक करणे
    for i in range(N):
        if board[row][i] == num or board[i][col] == num:
            return False
            
    # आतला छोटा बॉक्स (Subgrid) चेक करणे
    start_row, start_col = sub_size * (row // sub_size), sub_size * (col // sub_size)
    for i in range(sub_size):
        for j in range(sub_size):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    N = len(board)
    sub_size = int(math.isqrt(N)) # आपोआप साईझ ओळखणे (उदा. 9x9 साठी 3, 16x16 साठी 4)
    
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

with tab1:
    st.subheader("कोणत्याही साईझचा सुडोकू किंवा नंबर टेबल सोडवा")
    st.write("उदा. 4x4, 9x9 किंवा 16x16. रिकाम्या बॉक्ससाठी **0** वापरा आणि आकडे स्वल्पविरामाने वेगळे करा.")
    
    grid_input = st.text_area(
        "येथे टेबलचे आकडे टाका:", 
        "5,3,0,0,7,0,0,0,0\n6,0,0,1,9,5,0,0,0\n0,9,8,0,0,0,0,6,0\n8,0,0,0,6,0,0,0,3\n4,0,0,8,0,3,0,0,1\n7,0,0,0,2,0,0,0,6\n0,6,0,0,0,0,2,8,0\n0,0,0,4,1,9,0,0,5\n0,0,0,0,8,0,0,7,9",
        height=250
    )
    
    if st.button("टेबल सोडवा (Solve)"):
        try:
            rows = grid_input.strip().split('\n')
            board = [[int(num.strip()) for num in row.split(',')] for row in rows]
            
            # टेबल चौकोनी (Square) आहे का ते चेक करणे
            N = len(board)
            if all(len(r) == N for r in board) and N > 0:
                with st.spinner(f"{N}x{N} चे टेबल सोडवत आहे..."):
                    if solve_sudoku(board):
                        st.success(f"✅ {N}x{N} टेबल यशस्वीपणे सोडवले!")
                        for r in board:
                            st.code(" | ".join(str(x).rjust(2, ' ') for x in r))
                    else:
                        st.error("❌ हे टेबल सोडवणे शक्य नाही. दिलेले आकडे चुकीचे असू शकतात.")
            else:
                st.warning(f"टेबलची साईझ चुकीची आहे. तुम्ही {N} ओळी दिल्या आहेत, त्यामुळे प्रत्येक ओळीत {N} च आकडे असले पाहिजेत.")
        except Exception:
            st.error("त्रुटी: कृपया फॉरमॅट तपासा. फक्त आकडे आणि स्वल्पविराम वापरा.")

# ---------------------------------------------------------
# २. फोटो स्कॅनर (OCR)
# ---------------------------------------------------------
with tab2:
    st.subheader("फोटोमधील मजकूर आणि आकडे वाचा")
    img_file = st.file_uploader("फोटो निवडा:", type=['png', 'jpg', 'jpeg'])
    if img_file is not None:
        image = Image.open(img_file)
        st.image(image, width=300)
        if st.button("स्कॅन करा"):
            with st.spinner("स्कॅन करत आहे..."):
                text = pytesseract.image_to_string(image)
                if text.strip():
                    st.success("✅ स्कॅन यशस्वी!")
                    st.code(text)
                else:
                    st.warning("स्पष्ट मजकूर सापडला नाही.")

# ---------------------------------------------------------
# ३. वेब ऑटोमेशन (Web Scraper)
# ---------------------------------------------------------
with tab3:
    st.subheader("वेबसाईटवरील डेटा काढा")
    url_input = st.text_input("लिंक (URL) टाका:")
    if st.button("डेटा आणा"):
        if url_input:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                res = requests.get(url_input, headers=headers, timeout=10)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    st.success("✅ डेटा मिळाला!")
                    st.text_area("मजकूर:", soup.get_text(separator=' ', strip=True)[:1000] + "...", height=200)
                else:
                    st.error("लिंक उघडता आली नाही.")
            except Exception:
                st.error("लिंक किंवा इंटरनेट तपासा.")

# ---------------------------------------------------------
# ४. ॲडव्हान्स गणित इंजिन
# ---------------------------------------------------------
with tab4:
    st.subheader("गुंतागुंतीचे गणित सोडवा")
    math_expr = st.text_input("गणित टाका (उदा. x**2 - 5*x + 6):")
    if st.button("उत्तर काढा"):
        try:
            expr = sp.sympify(math_expr)
            st.success(f"उत्तर: {expr.evalf()}")
        except Exception:
            st.error("योग्य सूत्र द्या.")
