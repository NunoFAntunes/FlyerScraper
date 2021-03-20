import PySimpleGUI as sg
from datetime import datetime

def open_add(date_of_interface):
	layout = [[sg.Text("Atenção: Por favor preencha o nome do concorrente em letras minúsculas", text_color ="red", key="new_add")], [sg.Input("competidor", key="nome_add_competidor"), sg.Button("Ok", key="okAdd")]]
	window = sg.Window("Add Competitor", layout, modal=True)
	choice = None
	while True:
		event, values = window.read()
		if event == "Exit" or event == sg.WIN_CLOSED:
			break
		if event == "okAdd":
			with open('competitors.conf', "a", encoding='utf8') as f:
				f.write(values["nome_add_competidor"] + "\n")
			layoutOut = create_layout(date_of_interface)
			break
	window.close()
	return layoutOut

def open_rem(date_of_interface):
	layout = [[sg.Text("Atenção: Por favor preencha o nome de um concorrente existente na lista e em letras minúsculas", text_color ="red", key="new_rem")],[sg.Input("competidor", key="nome_rem_competidor"), sg.Button("Ok", key="okRem")]]
	window = sg.Window("Remove Competitor", layout, modal=True)

	while True:
		event, values = window.read()
		if event == "Exit" or event == sg.WIN_CLOSED:
			break
		if event == "okRem":
			with open("competitors.conf", "r") as f:
				lines = f.readlines()
			with open("competitors.conf", "w") as f:
				for line in lines:
					if line.strip("\n") != values["nome_rem_competidor"]:
						f.write(line)
			layoutOut = create_layout(date_of_interface)
			break
	window.close()
	return layoutOut

def create_layout(data):
	now = data
	layout = [[sg.Text("Baixar folhetos após data:")],
	[sg.CalendarButton("Escolher Data", target='-DATE-', format="%d/%b/%Y", close_when_date_chosen=True, default_date_m_d_y=(now.month, now.day, now.year)), sg.Input(now.strftime("%d/%b/%Y"), key='-DATE-', disabled=True, use_readonly_for_disable=True, size=(15,1))]]

	checkboxes = []
	checkbox_line = []
	with open('competitors.conf', encoding='utf8') as f:
		split=0
		for line in f:
			line = line.strip()
			if split != 3:
				checkbox = sg.Checkbox(line, key="-IN{comp}-".format(comp=line), size=(10,1))
				checkbox_line.append(checkbox)
				split = split+1
			else:
				checkboxes.append(checkbox_line)
				checkbox_line = []
				checkbox = sg.Checkbox(line, key="-IN{comp}-".format(comp=line), size=(10,1))
				checkbox_line.append(checkbox)
				split = 1
		checkboxes.append(checkbox_line)

	botoes_competidores = [[sg.Button("Adicionar Competidor", key="open_add"), sg.Button("Remover Competidor",  key="open_rem"), sg.Button("Refresh", key="refresh_interface")]]

	layout = layout + [[sg.Frame(layout=checkboxes, title='Competidores',title_color='red', relief=sg.RELIEF_SUNKEN)]] + botoes_competidores + [[sg.Text('Output', key='-OUT-')],[sg.Button("Ok"), sg.Button("Sair")]]
	return layout

def main():
	layout = create_layout(datetime.now())
	window = sg.Window("Baixar Folhetos", layout)

	while True:
		event, values = window.read()
		if event is None or event == 'Sair':
			break
		window['-OUT-'].update('DONE!')
		if event == "open_add":
			layoutOut = open_add(datetime.strptime(values['-DATE-'], "%d/%b/%Y"))
			window.close()
			window = sg.Window("Baixar Folhetos", layoutOut)
		if event == "open_rem":
			layoutOut = open_rem(datetime.strptime(values['-DATE-'], "%d/%b/%Y"))
			window.close()
			window = sg.Window("Baixar Folhetos", layoutOut)
	window.close()

if __name__ == "__main__":
	main()