import re
from dv_normalize.dv_num import int_to_dv

def replace_digits_with_dv(text: str) -> str:
    """
    Convert all numbers in text to Dhivehi, handling different formats:
    - Regular numbers
    - Years (when followed by ވަނަ)
    - Decimal numbers
    """
    def convert_match(match):
        full_num = match.group(0)
        
        # Handle decimal numbers
        if '.' in full_num:
            whole, decimal = full_num.split('.')
            whole_dv = int_to_dv(int(whole), is_spoken=True)
            decimal_dv = ' '.join(int_to_dv(int(d), is_spoken=True) for d in decimal)
            return f"{whole_dv} ޕޮއިންޓު {decimal_dv}"
        
        num = int(full_num)
        
        # Check if next word is ވަނަ (indicates year)
        text_after = text[match.end():].strip()
        if text_after.startswith('ވަނަ'):
            return int_to_dv(num, is_year=True)
        
        # Regular number conversion
        return int_to_dv(num, is_spoken=True)

    # Remove commas from numbers first
    text = text.replace(',', '')
    
    # Convert all numbers using the pattern
    pattern = r'\d+(?:\.\d+)?'
    text = re.sub(pattern, convert_match, text)
    
    return text

def normalize_sentence_end(text: str) -> str:
    """
    Normalize Dhivehi sentence endings using common patterns for spoken form
    """
    patterns = [
        # Noun endings with އެކެވެ
        (r'([ަ-ް]*?)އެކެވެ', r'\1އެއް'),
        (r'([ަ-ް]*?)ކެކެވެ', r'\1ކެއް'),
        (r'([ަ-ް]*?)ތެކެވެ', r'\1ތެއް'),
        (r'([ަ-ް]*?)މެކެވެ', r'\1މެއް'),
        (r'([ަ-ް]*?)ހެކެވެ', r'\1ހެއް'),
        (r'([ަ-ް]*?)ރެކެވެ', r'\1ރެއް'),
        (r'([ަ-ް]*?)ޅެކެވެ', r'\1ޅެއް'),
        
        # Endings that convert to ށް
        (r'ށެވެ', 'ށް'),
        (r'އަށެވެ', 'އަށް'),
        (r'ޔަށެވެ', 'ޔަށް'),
        (r'ކަށެވެ', 'ކަށް'),
        (r'ތަށެވެ', 'ތަށް'),
        (r'ޗަށެވެ', 'ޗަށް'),
        (r'ނަށެވެ', 'ނަށް'),
        (r'ރަށެވެ', 'ރަށް'),
        (r'ދަށެވެ', 'ދަށް'),
        
        # Common verb endings
        (r'ވެއެވެ', 'ވޭ'),
        (r'ނެއެވެ', 'ނެ'),
        (r'ވިއެވެ', 'ވި'),
        (r'ދެއެވެ', 'ދޭ'),
        (r'ޖެއެވެ', 'ޖެ'),
        (r'ލެއެވެ', 'ލެ'),
        (r'ހުރެއެވެ', 'ހުރޭ'),
        (r'ބެއެވެ', 'ބޭ'),
        (r'ރެއެވެ', 'ރޭ'),
        
        # Common noun endings
        (r'ތަކެވެ', 'ތައް'),
        (r'ގައެވެ', 'ގައި'),
        (r'އަހެވެ', 'ވަސް'),
        (r'ބަހެވެ', 'ބަސް'),
        
        # Endings that convert to ން
        (r'އިންނެވެ', 'އިން'),
        (r'ންނެވެ', 'ން'),
        (r'ދުނެވެ', 'ދުން'),
        (r'ދުމެވެ', 'ދުން'),
        (r'ރުމެވެ', 'ރުން'),
        (r'މުމެވެ', 'މުން'),
        (r'ޅެމެވެ', 'ޅެން'),
        (r'ޔުމެވެ', 'ޔުން'),
        
        # Special cases
        (r'ނޫނެވެ', 'ނޫން'),
        (r'ހުއްޓެވެ', 'ހުރި'),
        (r'ލެވެ', 'ލު'),
        (r'ދެވެ', 'ދު'),
        (r'ރެވެ', 'ރު'),
        (r'ޅެވެ', 'ޅު'),
        
        # Remove standalone އެވެ (should be last)
        (r'\s*އެވެ', ''),
    ]
    
    # Apply patterns
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    
    return text.strip()

def spoken_dv(text: str) -> str:
    """
    Normalize Dhivehi text by:
    1. Converting numbers to spoken form (including years and decimals)
    2. Normalizing sentence endings
    3. Removing special characters
    4. Cleaning up whitespace
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Pre-process
    text = text.strip()
    
    # Apply normalizations
    text = normalize_sentence_end(text)
    text = replace_digits_with_dv(text)
    
    # Post-process to fix spacing
    text = re.sub(r'(?<=[ހ-ޥ])\s+(?=[ަ-ް])', '', text)  # Fix diacritic spacing
    text = re.sub(r'\s+([.،؟!])', r'\1', text)  # Fix punctuation spacing
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces
    
    return text.strip()