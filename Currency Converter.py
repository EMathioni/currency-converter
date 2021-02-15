import requests
from bs4 import BeautifulSoup as bs
from babel.numbers import format_currency

url_base = "https://www.iban.com/currency-codes"
url_base_tw = 'https://transferwise.com/gb/currency-converter/'

rq = requests.get(url_base)
html_page = rq.text
m_soup = bs(html_page, 'html.parser')
m_table = m_soup.find('tbody')
m_formated_table = m_table.find_all('tr')
data_list = []


def convert_coin(pais1, pais2, valor):
  str(pais1).lower()
  str(pais2).lower()
  force_int = float(valor)
  tw_formated_url = f"{url_base_tw}{pais1}-to-{pais2}-rate?amount={valor}"
  tw_rq = requests.get(tw_formated_url)
  tw_html_page = tw_rq.text
  tw_m_soup = bs(tw_html_page, 'html.parser')
  tw_m_conv = tw_m_soup.find('div', class_='col-lg-6 text-xs-center text-lg-left')
  m_formated_conv = tw_m_conv.find('span', class_='text-success').string
  result = float(m_formated_conv) * force_int
  return format_currency(result, pais2, locale='pt_BR')

def new_consult():
  user_input = str(input("#> ")).lower()
  if user_input == "s":
    for id, pais in enumerate(data_list):
      print(f"#{id} -- {pais['País']}")
    start()
  elif user_input == "n":
    print("Programa encerrado, obrigado por usar nosso Conversor de Moedas v2!")
    print("GitHub: https://github.com/EMathioni")
    return
  else:
    print("Caractere inválido, use apenas 's' (sim) e 'n' (não)")
    new_consult()

for line in m_formated_table:
    line = line.find_all('td')
    nome_moeda = line[1].text
    if nome_moeda != "No universal currency":
      country = {
        'País': line[0].string,
        'code_coin': line[2].string,
      }
      data_list.append(country)

def start():
  try:
    print("Para começar, escolha o numero do país da moeda de origem!")
    user_input = int(input("#> "))
    print("------------")
    country = data_list[user_input]
    print(f"(X) {country['País']}")
    print("------------")
    print("Agora escolha a # do país de conversão")
    user_input2 = int(input("#> "))
    print("------------")
    country2 = data_list[user_input2]
    print(f"(X) {country2['País']}")
    print("------------")
    print(f"Deseja converter quantos {country['code_coin']} em {country2['code_coin']}?")
    user_input3 = float(input("#> "))
    print("------------")
    if user_input > len(data_list) or user_input2 > len(data_list):
      print("Numero maior do que a lista!")
      start() 
    else:
      resultado = convert_coin(country['code_coin'], country2['code_coin'], user_input3)
      print(f"{user_input3} {country['code_coin']} ({country['País']}) em {country2['code_coin']} ({country2['País']}) é: {resultado}")
      print("Deseja consultar novamente? s/n")
      new_consult()
  except ValueError:
    print("Letras e palavras não são permitidos, use apenas numeros.")
    start()
  except AttributeError:
    print("Uma das opções selecionadas não está disponível no momento. Desculpe.")
    print("Deseja consultar novamente? s/n")
    new_consult()


print("Obrigado por usar o Conversor de Moedas v2 :)")
print("GitHub: https://github.com/EMathioni")
print("---------------")
for id, pais in enumerate(data_list):
  print(f"#{id} -- {pais['País']}")
start()
