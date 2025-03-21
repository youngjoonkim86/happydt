import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
from anthropic import Anthropic

# Claude API 초기화
client = Anthropic(api_key="your_claude_api_key")  # 🔁 여기에 본인의 Claude API 키를 넣으세요

st.set_page_config(page_title="Claude 3 PDF 분석기 (OCR 기반)", layout="centered")
st.title("📄 Claude 3 PDF 이미지 분석기 (OCR → Claude)")

uploaded_file = st.file_uploader("분석할 PDF 파일을 업로드하세요", type="pdf")

if uploaded_file:
    st.success("✅ PDF 업로드 완료. 분석 중...")

    # 1. PDF → 이미지 변환
    images = convert_from_bytes(uploaded_file.read(), dpi=300)
    st.image(images[0], caption="📷 첫 페이지 미리보기", use_column_width=True)

    # 2. 이미지 → 텍스트 (OCR)
    ocr_texts = []
    for idx, img in enumerate(images[:3]):  # 너무 많을 경우 앞 3페이지만 사용
        text = pytesseract.image_to_string(img, lang="kor+eng")
        ocr_texts.append(f"[페이지 {idx+1}]\n{text}")

    combined_text = "\n\n".join(ocr_texts)

    # 3. Claude API에 전달할 프롬프트
    prompt = (
        "다음은 PDF를 이미지로 변환하고 OCR로 추출한 텍스트입니다.\n"
        "표가 있다면 표로 재구성하고, 전체 내용을 항목별로 정리해 주세요.\n\n"
        + combined_text
    )

    if st.button("🧠 Claude에게 분석 요청"):
        with st.spinner("Claude 3가 문서를 분석 중입니다..."):
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.content[0].text
            st.subheader("🧠 Claude 3 분석 결과")
            st.write(result)

            # 결과 다운로드
            st.download_button("📥 결과 다운로드 (txt)", result, file_name="claude_analysis.txt")