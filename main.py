import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO
    input_marca=ft.TextField(value='marca', label="Marca")
    input_modello=ft.TextField(value='modello', label="Modello")
    input_anno=ft.TextField(value='anno', label="Anno")
    def handleAdd(e):
        currentVal = txtOut.value
        txtOut.value = currentVal + 1
        txtOut.update()

    def handleRemove(e):
        currentVal = txtOut.value
        txtOut.value = currentVal - 1
        txtOut.update()

    btnMinus = ft.IconButton(icon=ft.Icons.REMOVE,
                             icon_color="red",
                             icon_size=24, on_click=handleRemove)
    btnAdd = ft.IconButton(icon=ft.Icons.ADD,
                           icon_color="green",
                           icon_size=24, on_click=handleAdd)
    txtOut = ft.TextField(width=80, disabled=True,
                          value=0, border_color="green",
                          text_align=ft.TextAlign.CENTER)





    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO
    def aggiungi_automobile_handler(e):
        marca = input_marca.value
        modello = input_modello.value
        anno= input_anno.value
        posti = txtOut.value


        if not marca:
            alert.show_alert("❌ Il campo 'Marca' è obbligatorio")
            return
        if not modello:
            alert.show_alert("❌ Il campo 'Modello' è obbligatorio")
            return
        if not anno or not posti:
            alert.show_alert("❌ Compila tutti i campi (Anno e Posti).")
            return

        try:
            anno = int(anno)
            posti = int(posti)
        except ValueError as ex:
            alert.show_alert('❌ anno e posti devono essere numeri interi')
            return
        if anno>2025:
            alert.show_alert("❌ L'anno deve essere minore di 2025")
            return
        if posti <= 0:
            alert.show_alert("❌ Il numero di posti deve essere maggiore di zero.")
            return

        try:
            autonoleggio.aggiungi_automobile(marca, modello, anno, posti)
            input_marca.value = ""
            input_modello.value = ""
            input_anno.value = ""
            txtOut.value =0

            aggiorna_lista_auto()
            page.update()
            alert.show_alert("✅ Automobile aggiunta con successo.")
        except Exception as ex:
            alert.show_alert(f"❌ Errore durante l'aggiunta dell'automobile: {ex}")

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    pulsante_conferma_auto=ft.ElevatedButton('Aggiungi automobile',on_click=aggiungi_automobile_handler)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Text('aggiungi nuova automobile', size=20),
        ft.Row(spacing=35,
               controls=[input_marca,input_modello,input_anno,btnMinus,txtOut,btnAdd],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(spacing=35,
               controls=[pulsante_conferma_auto],
               alignment=ft.MainAxisAlignment.CENTER),
        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
