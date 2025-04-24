import time
import json
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1) Conectar ao Chrome em modo depuração
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)

# 2) Acessar a página e aguardar login
driver.get("https://aquitemjt.trt8.jus.br")
print("Por favor, faça login no site...")

# 2.1) Clicar no menu "Atermações" após o login
try:
    menu_atermacoes = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Atermações"))
    )
    menu_atermacoes.click()
    print("Menu 'Atermações' clicado.")
except Exception as e:
    print("Erro ao clicar no menu 'Atermações':", e)

try:
    # Aguarda até que o botão Novo esteja clicável
    novo_btn = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "action-button[label='botao.novo'] button"
        ))
    )
    novo_btn.click()
    print("Botão 'Novo' clicado com sucesso.")
except Exception as e:
    print("Erro ao clicar no botão 'Novo':", e)

try:
    nome_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "nome"))
    )
    print("Login detectado – campo 'nome' visível.")
except Exception as e:
    print("Erro ao aguardar login:", e)
    driver.quit()
    exit()

# 3) Escolher o JSON pelo popup do Tkinter
root = tk.Tk()
root.withdraw()
root.update()
file_path = filedialog.askopenfilename(
    title="Selecione o arquivo JSON",
    filetypes=[("Arquivos JSON", "*.json")]
)
root.destroy()

if not file_path:
    print("Nenhum arquivo selecionado.")
    driver.quit()
    exit()

# 4) Carregar e extrair campos do JSON
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
valor_nome = data.get("nome", "")
valor_telefone = data.get("telefone", "")
print(f"JSON → nome: {valor_nome}, telefone: {valor_telefone}")

# 5) Preencher o campo 'nome'
nome_input.clear()
nome_input.send_keys(valor_nome)
print("Campo 'nome' preenchido.")

# 6) Agora preencher o 'telefone'
try:
    # 6.1 Localiza o <input> interno do telefone
    telefone_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#telefone input"))
    )

    # 6.2 Insere o valor diretamente no atributo .value
    js_set_value = """
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """
    driver.execute_script(js_set_value, telefone_input, valor_telefone)
    print("Campo 'telefone' preenchido via JS.")

except Exception as e:
    print("Erro ao preencher o 'telefone':", e)

# 7) Preencher o 'email'
try:
    # extrair do JSON
    valor_email = data.get("email", "")
    print("Valor extraído para 'email':", valor_email)

    # localizar o input de email
    email_input = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "email"))
    )
    # limpar e inserir o valor
    email_input.clear()
    email_input.send_keys(valor_email)
    print("Campo 'email' preenchido.")
except Exception as e:
    print("Erro ao preencher o 'email':", e)

# 8) Preencher o 'cpf'
try:
    # extrai do JSON
    valor_cpf = data.get("cpf", "")
    print("Valor extraído para 'cpf':", valor_cpf)

    # localiza o <input> dentro de #cpf
    cpf_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#cpf input"))
    )

    # forçar via JavaScript para lidar com máscara e Angular
    js_set_cpf = """
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """
    driver.execute_script(js_set_cpf, cpf_input, valor_cpf)
    print("Campo 'cpf' preenchido via JS.")

except Exception as e:
    print("Erro ao preencher o 'cpf':", e)

    # 9) Preencher o 'rg'
try:
    # extrai do JSON
    valor_rg = data.get("rg", "")
    print("Valor extraído para 'rg':", valor_rg)

    # localiza o input de RG
    rg_input = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "rg"))
    )
    rg_input.clear()
    rg_input.send_keys(valor_rg)
    print("Campo 'rg' preenchido.")

except Exception as e:
    print("Erro ao preencher o 'rg':", e)

# 10) Preencher o 'ctps'
try:
    # extrai do JSON
    valor_ctps = data.get("ctps", "")
    print("Valor extraído para 'ctps':", valor_ctps)

    # localiza o input de CTPS
    ctps_input = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "ctps"))
    )
    ctps_input.clear()
    ctps_input.send_keys(valor_ctps)
    print("Campo 'ctps' preenchido.")

except Exception as e:
    print("Erro ao preencher o 'ctps':", e)

# 11) Clicar na aba "Contrato"
try:
    tab_contrato = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, "p-tabpanel-1-label"))
    )
    tab_contrato.click()
    print("Aba 'Contrato' selecionada.")
except Exception as e:
    print("Erro ao clicar na aba 'Contrato':", e)

# 12) Preencher o 'dataAdmissao'
try:
    # extrai do JSON (formato esperado: DD/MM/YYYY)
    valor_data = data.get("dataadmissao", "")
    print("Valor extraído para 'dataadmissao':", valor_data)

    # localiza o <input> interno do p-calendar
    calendar_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#dataAdmissao input"))
    )

    # força via JavaScript para o Angular reconhecer
    js_set_date = """
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """
    driver.execute_script(js_set_date, calendar_input, valor_data)
    print("Campo 'dataAdmissao' preenchido via JS.")

except Exception as e:
    print("Erro ao preencher o 'dataAdmissao':", e)

# Final) Manter aberto para conferência e encerrar
time.sleep(10)
driver.quit()

