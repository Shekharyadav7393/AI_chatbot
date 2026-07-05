from app.utils.validators import sanitize_filename, validate_file_type


def test_validate_supported_file_types():
    assert validate_file_type("policy.pdf")
    assert validate_file_type("faq.docx")
    assert validate_file_type("terms.txt")
    assert not validate_file_type("malware.exe")


def test_sanitize_filename_removes_unsafe_characters():
    assert sanitize_filename("../customer policy?.pdf") == ".._customer_policy_.pdf"
