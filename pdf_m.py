import os


def barcode_pdf(code):
    from io import BytesIO

    from barcode import Code39
    from barcode.writer import ImageWriter

    name = "somefile.png"
    # Or to an actual file:
    with open(name, "wb") as f:
        Code39(code, writer=ImageWriter(), add_checksum=False).write(f)

    # import img2pdf
    #
    # a4_page_size = [img2pdf.in_to_pt(8.3), img2pdf.in_to_pt(11.7)]
    # layout_function = img2pdf.get_layout_fun(a4_page_size)
    #
    # pdf = img2pdf.convert(name, layout_fun=layout_function)
    # with open('A4_dog.pdf', 'wb') as f:
    #     f.write(pdf)

    from fpdf import FPDF
    pdf = FPDF()

    pdf.add_page()
    pdf.image(name, w=1002/7.8, h=280/7.8)
    pdf.output("barcode.pdf", "F")

def order_pdf(id,cl,srv,dt,sm, num_cl):
    from fpdf import FPDF
    txt = ''
    for s in srv:
        txt+=s+', '
    txt = txt[:-2]

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('Calibri Regular', '', 'C:\Windows\Fonts\calibri.ttf', uni=True)
    pdf.add_font('Calibri THICK', '', 'C:\Windows\Fonts\calibrib.ttf', uni=True)
    pdf.set_font('Calibri THICK', size=25)
    pdf.image('logo.png', w=30,h=30)
    pdf.cell(200, -30, txt="Заказ-"+id, ln=1, align="C")
    pdf.set_font('Calibri Regular', size=14)
    pdf.text(10,60, 'Дата: '+dt)
    pdf.text(10,70, 'Код клиента: '+str(num_cl))
    pdf.text(10,80, 'ФИО: '+cl)
    pdf.text(10,90, 'Услуги: '+txt)
    pdf.text(10,100, 'Стоимость: '+sm)
    pdf.output("order.pdf")

if __name__ == "__main__":
    print('im ok')
    # barcode_pdf("8888888801012022123456")
    # order_pdf()