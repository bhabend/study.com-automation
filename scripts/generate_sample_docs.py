from app.docs_export import save_docx, generate_diff

orig = "This is a sample original.\nLine two.\n"
opt = "This is a sample optimized.\nLine two changed.\n"
save_docx("outputs/sample_original.docx", "Sample Original", orig)
save_docx("outputs/sample_optimized.docx", "Sample Optimized", opt)
print(generate_diff(orig, opt))
