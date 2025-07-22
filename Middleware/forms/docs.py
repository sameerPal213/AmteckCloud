from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.units import inch


def QAQC1001(filename):
    # set up padding for frames
    base_padding = dict(
            leftPadding=.075*inch,
            rightPadding=.075*inch,
            topPadding=.025*inch,
            bottomPadding=0.25*inch)

    # Set up frames
    form_name_frame = Frame(.5*inch, 10.25*inch, 7.5*inch, .25*inch,
            **base_padding)
    project_frame   = Frame(.5*inch,    9.7*inch,   3.75*inch,  .4457*inch,
            **base_padding)
    f = [

    # Set up pages
    first_page_template = PageTemplate(
            id="FirstPage", 
            frames = f)

    # Set up document format
    d = BaseDocTemplate(filename)

