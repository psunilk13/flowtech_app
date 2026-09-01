def before_save(doc, method=None):
    doc.skip_auto_attendance = 0
