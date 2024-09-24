from flask import Flask, request, send_file, Response
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import io
from reportlab.lib.utils import ImageReader
import base64
from io import BytesIO
from PIL import Image




app = Flask(__name__)


@app.route('/gerar_pdf', methods=['POST'])
def criar_pdf():
    print("Requisição recebida para /gerar_pdf")
    data = request.json
    print("Dados recebidos:", data)

    condominio = data.get('condominio')
    ocorrencia_id = data.get('ocorrencia_id')
    numero_ocorrencia = data.get('numeroOcorrencia')
    data_ocorrencia = data.get('data_ocorrencia')
    nome_proprietario = data.get('nomeProprietario')
    quadra = data.get('quadra')
    lote = data.get('lote')
    tipo_multa = data.get('tipoMulta')
    data_retorno = data.get('dataRetorno')
    artigo = data.get('selectedArtigo')
    descricao = data.get('descricao')
    numero_telefone = data.get('numeroTelefone')

    print("Criando PDF...")

    pdf_buffer = io.BytesIO()

    try:
        # Definindo as margens
        margem_esquerda = 50
        margem_direita = 50
        margem_superior = 50
        margem_inferior = 50

        # Definindo o tamanho da página com base nas margens
        largura_pagina = letter[0] - margem_esquerda - margem_direita
        altura_pagina = letter[1] - margem_superior - margem_inferior

        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Definindo a posição inicial considerando as margens
        x = margem_esquerda
        y = altura_pagina - margem_superior

        data_atual = datetime.now().strftime("%d/%m/%Y")

        if condominio in ['Florais Cuiabá', 'Belvedere', 'Belvedere 2']:
            texto = [
                "Número da Ocorrência: {}".format(numero_ocorrencia),
                "Cuiabá, {}".format(data_atual),
                "Ao senhor, {}".format(nome_proprietario),
                "Quadra/Lote: {} {}".format(quadra, lote),
                "Apraz-nos cumprimentá-lo cordialmente, sirvo-me do presente para informar que a equipe de fiscalização de obras, durante vistoria realizada no dia {}, constatou o descumprimento das normas construtivas e urbanísticas do condomínio, referente ao seguinte dispositivo:".format(
                    data_ocorrencia),
                "",
                "Dispositivo Observação do fiscal: Descrição da impropriedade",
                "Art. {} {}".format(artigo, descricao),
                "Ref.: Abertura de ocorrência de obra por descumprimento de normas construtivas.",
                "",
                "NOTIFICO-LHE para sanar a irregularidade apontada, até {} a contar a partir do recebimento desta notificação.".format(
                    data_retorno),
                "",
                "Dúvidas entre em contato no whatsapp da engenharia do condomínio: {}".format(numero_telefone)
            ]
        elif condominio in ['Villa Jardim', 'Primor das Torres', 'Florais Itália']:
            texto = [
                "Número da Ocorrência: {}".format(numero_ocorrencia),
                "Cuiabá, {}".format(data_atual),
                "Ao senhor, {}".format(nome_proprietario),
                "Quadra/Lote: {} {}".format(quadra, lote),
                "Ref.: Abertura de ocorrência de obra por descumprimento de normas construtivas.",
                "Apraz-nos cumprimentá-lo cordialmente, sirvo-me do presente para informar que a equipe de fiscalização de obras, durante vistoria realizada no dia {}, constatou o descumprimento das normas construtivas e urbanísticas do condomínio, referente ao seguinte dispositivo:".format(
                    data_ocorrencia),
                "",
                "Dispositivo Observação do fiscal: Descrição da impropriedade",
                "Art. {} {}".format(artigo, descricao),
                "",
                "NOTIFICO-LHE para sanar a irregularidade apontada, até {} a contar a partir do recebimento desta notificação.".format(
                    data_retorno),
                "",
                "Dúvidas entre em contato no whatsapp da engenharia do condomínio: {}".format(numero_telefone)
            ]
        else:
            # Lógica padrão
            texto = [
                "Número da Ocorrência: {}".format(numero_ocorrencia),
                "Cuiabá, {}".format(data_atual),
                "Ao senhor, {}".format(nome_proprietario),
                "Quadra: {} Lote: {}".format(quadra, lote),
                "Ref.: Abertura de ocorrência de obra por descumprimento de normas construtivas.",
                "Apraz-nos cumprimentá-lo cordialmente, sirvo-me do presente para informar que a equipe de fiscalização de obras, durante vistoria realizada no dia {}, constatou a continuidade no".format(
                    data_ocorrencia),
                "descumprimento das normas construtivas e urbanísticas do condomínio, referente ao seguinte dispositivo:",
                "",
                "Dispositivo",
                "Observação do fiscal:",
                "Ficará aplicada automaticamente a penalidade de Multa {}, conforme prevê o Art. 194, II, do Regulamento de Construção,constante da Norma Consolidada aprovada na Assembleia Geral realizada no dia 08/12/12, na sequência, o prazo até {} para interposição de recurso perante o Conselho Deliberativo. Expirado o prazo sem as providências ou sem a interposição do competente pedido de reconsideração".format(
                    tipo_multa, data_retorno),
                "Canteiro de obra sujo",
                "Apraz-nos cumprimentá-lo cordialmente, sirvo-me do presente para informar que a equipe, constatou a ",
                "continuidade no",
                "Art. {} {}".format(artigo, descricao),
                "Dúvidas entrar em contato com o número de engenharia do condomínio.",
                "Att, Administração Condomínio {}".format(condominio)
            ]

        # Ajustando a margem do texto
        margem_texto = 15

        for line in texto:
            if y < margem_inferior:
                c.showPage()  # Cria uma nova página
                c.setFont("Helvetica", 12)
                y = altura_pagina - margem_superior  # Reinicia a posição y
            linhas = line.split('\n')
            for linha in linhas:
                palavras = linha.split(' ')
                linhas_quebradas = []
                linha_atual = ''
                for palavra in palavras:
                    if c.stringWidth(linha_atual + palavra) < largura_pagina:
                        linha_atual += palavra + ' '
                    else:
                        linhas_quebradas.append(linha_atual)
                        linha_atual = palavra + ' '
                linhas_quebradas.append(linha_atual)
                for linha_quebrada in linhas_quebradas:
                    c.drawString(x, y, linha_quebrada.strip())
                    y -= margem_texto

        c.save()
        print("PDF criado com sucesso")

        # Voltar ao início do buffer
        pdf_buffer.seek(0)

        # Retornar o PDF como uma resposta HTTP
        return send_file(pdf_buffer, as_attachment=True, download_name="ocorrencia_{}.pdf".format(numero_ocorrencia))
    except Exception as e:
        print("Erro ao criar PDF:", e)
        return json.dumps({"error": str(e)}), 500



@app.route('/gerar_pdfav', methods=['POST'])
def gerar_pdfav():
    # Recebe os dados do POST
    data = request.json

    # Extrai os dados do JSON
    numero_ocorrencia = data.get('numero_ocorrencia', '')
    data_hoje = data.get('data_hoje', '')
    nome_proprietario = data.get('nome_proprietario', '')
    quadra = data.get('quadra', '')
    lote = data.get('lote', '')
    data_avaliacao = data.get('data_avaliacao', '')
    data_envio_ocorrencia = data.get('data_envio_ocorrencia', '')
    dispositivo = data.get('dispositivo', '')
    descricao = data.get('descricao', '')
    observacoes = data.get('observacoes', '')
    data_retorno = data.get('data_retorno', '')

    # Inicia o PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    margem_esquerda = 50
    margem_direita = 50
    margem_superior = 50
    margem_inferior = 50

    # Define o conteúdo do PDF
    texto = [
        "Número da Ocorrência: {}".format(numero_ocorrencia),
        "Cuiabá, {}".format(data_hoje),
        "Ao senhor (a), {}".format(nome_proprietario),
        "Quadra/Lote: {} {}".format(quadra, lote),
        "Ref.: Continuidade no descumprimento das normas construtivas.",
        "Apraz-nos cumprimentá-lo cordialmente, sirvo-me do presente para informar que a equipe de fiscalização de obras, durante a vistoria realizada no dia {}, constatou a continuidade no".format(data_avaliacao),
        "descumprimento das normas construtivas e urbanísticas do condomínio, informado no COMUNICADO DE ABERTURA DE OCORRÊNCIA, enviado no dia {}, referente ao seguinte dispositivo:".format(data_envio_ocorrencia),
        "",
        "{}".format(dispositivo),
        "{}".format(descricao),
        "{}".format(observacoes),
        "NOTIFICO-LHE para sanar a irregularidade apontada, até {} a contar a partir do recebimento desta notificação. Vencido o prazo, sem manifestação ou regularização das impropriedades, ficará aplicada automaticamente a penalidade de multa administrativa de obra, nos termos de escalonamentos previstos nos artigos 83 e 84 das Normas Construtivas. Na sequência, o prazo de 5 (cinco) dias úteis para interposição de recurso.".format(data_retorno),
        "Dúvidas entre em contato no whatsapp da engenharia do condomínio"
    ]

    # Ajustando a margem do texto
    margem_texto = 15
    x = margem_esquerda  # Posição inicial de x
    y = letter[1] - margem_superior  # Posição inicial de y
    for line in texto:
        if y < margem_inferior:
            c.showPage()  # Cria uma nova página
            y = letter[1] - margem_superior  # Reinicia a posição y
        c.drawString(x, y, line)
        y -= margem_texto

    # Adiciona as imagens ao PDF
    for i, image_file in enumerate(request.files.getlist("imagens")):
        img = Image.open(image_file)
        img.save('image_{}.png'.format(i))  # Salva a imagem em um arquivo temporário ou permanente
        c.drawImage('image_{}.png'.format(i), 100, y - 100 - i * 100, width=100, height=100)

    # Fecha o PDF
    c.save()

    # Retornar o PDF diretamente como uma resposta HTTP
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='ocorrencia.pdf')

if __name__ == "__main__":
    app.run(host='192.168.0.8')