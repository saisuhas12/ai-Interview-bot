# utils.py
import io, json, re, tempfile, os
from PyPDF2 import PdfReader
import docx2txt

def extract_text_from_file(uploaded_file):
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        try:
            reader = PdfReader(uploaded_file)
            text = ""
            for p in reader.pages:
                page_text = p.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
        except Exception:
            return ""
    elif name.endswith(".docx"):
        # docx2txt expects a file path; write to a temporary .docx then process
        try:
            data = uploaded_file.getvalue()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp.write(data)
                tmp_path = tmp.name
            try:
                text = docx2txt.process(tmp_path)
            finally:
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
            return text or ""
        except Exception:
            return ""
    else:
        # assume plain text
        try:
            return uploaded_file.getvalue().decode('utf-8', errors='ignore')
        except Exception:
            return ""
            
# robust JSON extractor: finds the first {...} block and tries to load it
def extract_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return None
    return None
