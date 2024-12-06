import asyncio
import getpass
import os
import warnings

import pyautogui
from pywinauto.keyboard import send_keys
from PIL import Image, ImageEnhance
import pytesseract
from pywinauto.application import Application
from pywinauto_recorder.player import set_combobox
from rich.console import Console

from worker_automate_hub.api.client import (
    get_config_by_name,
    sync_get_config_by_name,
)
from worker_automate_hub.config.settings import load_env_config
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import (
    cod_icms,
    error_after_xml_imported,
    import_nfe,
    importar_notas_outras_empresas,
    is_window_open,
    is_window_open_by_class,
    itens_not_found_supplier,
    kill_process,
    login_emsys,
    rateio_despesa,
    set_variable,
    tipo_despesa,
    type_text_into_field,
    verify_nf_incuded,
    warnings_after_xml_imported,
    worker_sleep,
    zerar_icms,
)
from worker_automate_hub.utils.utils_nfe_entrada import EMSys

pyautogui.PAUSE = 0.5
console = Console()

emsys = EMSys()


async def entrada_de_notas_39(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    """
    Processo que relazia entrada de notas no ERP EMSys(Linx).

    """
    try:
        # Get config from BOF
        config = await get_config_by_name("login_emsys")
        console.print(task)

        console.print(config)

        # Seta config entrada na var nota para melhor entendimento
        nota = task.configEntrada
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        # Abre um novo emsys
        await kill_process("EMSys")
        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config.conConfiguracao, app, task)

        if return_login.sucesso == True:
            type_text_into_field(
                "Nota Fiscal de Entrada", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )
            pyautogui.press("enter")
            await worker_sleep(1)
            pyautogui.press("enter")
            console.print(
                f"\nPesquisa: 'Nota Fiscal de Entrada' realizada com sucesso",
                style="bold green",
            )
        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login

        await worker_sleep(10)

        # Procura campo documento
        console.print("Navegando pela Janela de Nota Fiscal de Entrada...\n")
        app = Application().connect(title="Nota Fiscal de Entrada")
        main_window = app["Nota Fiscal de Entrada"]

        console.print(
            "Controles encontrados na janela 'Nota Fiscal de Entrada', navegando entre eles...\n"
        )
        panel_TNotebook = main_window.child_window(
            class_name="TNotebook", found_index=0
        )
        panel_TPage = panel_TNotebook.child_window(class_name="TPage", found_index=0)
        panel_TPageControl = panel_TPage.child_window(
            class_name="TPageControl", found_index=0
        )
        panel_TTabSheet = panel_TPageControl.child_window(
            class_name="TTabSheet", found_index=0
        )
        combo_box_tipo_documento = panel_TTabSheet.child_window(
            class_name="TDBIComboBox", found_index=1
        )

        combo_box_tipo_documento.click()
        console.print(
            "Clique select box, Tipo de documento realizado com sucesso, selecionando o tipo de documento...\n"
        )

        await worker_sleep(4)

        set_combobox("||List", "NFe - NOTA FISCAL ELETRONICA PROPRIA - DANFE SERIE 077")
        console.print(
            "Tipo de documento 'NFe - NOTA FISCAL ELETRONICA PROPRIA - DANFE SERIE 077', selecionado com sucesso...\n"
        )

        await worker_sleep(4)

        # Clica em 'Importar-Nfe'
        imported_nfe = await import_nfe()
        if imported_nfe.sucesso == True:
            console.log(imported_nfe.retorno, style="bold green")
        else:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=imported_nfe.retorno,
                status=RpaHistoricoStatusEnum.Falha,
            )

        await worker_sleep(10)

        # Move até 'Notas de Outras Empresas'
        pyautogui.press('down', presses=5)
        # Clica em  'OK' para selecionar
        pyautogui.click(970, 666)
        await worker_sleep(3)

        try:
            empresa = str(int(nota.get("cnpjFornecedor")[8:12]))
            await importar_notas_outras_empresas(
                nota.get("dataEmissao"), nota.get("numeroNota"), empresa
            )

            await worker_sleep(10)

            # INTERAGINDO COM O CAMPO ALMOXARIFADO
            fornecedor = nota.get("nomeFornecedor")
            filialEmpresaOrigem = nota.get("filialEmpresaOrigem")
            console.print(
                f"Inserindo a informação do Almoxarifado {filialEmpresaOrigem} ...\n"
            )
            try:
                new_app = Application(backend="uia").connect(
                    title="Informações para importação da Nota Fiscal Eletrônica"
                )
                window = new_app["Informações para importação da Nota Fiscal Eletrônica"]
                edit = window.child_window(
                    class_name="TDBIEditCode", found_index=3, control_type="Edit"
                )
                valor_almoxarifado = filialEmpresaOrigem + "50"
                edit.set_edit_text(valor_almoxarifado)
                edit.type_keys("{TAB}")
            except Exception as e:
                console.print(f"Erro ao iterar itens de almoxarifado: {e}")
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Erro ao iterar itens de almoxarifado: {e}",
                    status=RpaHistoricoStatusEnum.Falha,
                )

            await worker_sleep(1)
            # INTERAGINDO COM O CAMPO TIPO DE DESPESAS
            if "brs" in fornecedor.lower():
                despesa = "192"
            elif "ataca" in fornecedor.lower():
                despesa = "15"
            elif "hygia" in fornecedor.lower():
                despesa = "193"
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=f"Fornecedor não mapeado para andamento no processo, forneceodr: {fornecedor}",
                    status=RpaHistoricoStatusEnum.Falha,
                )

            tipo_despesa_work = await tipo_despesa(despesa)
            if tipo_despesa_work.sucesso == True:
                console.log(tipo_despesa_work.retorno, style="bold green")
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=tipo_despesa_work.retorno,
                    status=RpaHistoricoStatusEnum.Falha,
                )

            # INTERAGINDO COM O CHECKBOX ZERAR ICMS
            checkbox_zerar_icms = await zerar_icms()
            if checkbox_zerar_icms.sucesso == True:
                console.log(checkbox_zerar_icms.retorno, style="bold green")
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=checkbox_zerar_icms.retorno,
                    status=RpaHistoricoStatusEnum.Falha,
                )

            # INTERAGINDO COM O CAMPO DE CODIGO DO ICMS
            cod_icms_work = await cod_icms("33")
            if cod_icms_work.sucesso == True:
                console.log(cod_icms_work.retorno, style="bold green")
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=cod_icms_work.retorno,
                    status=RpaHistoricoStatusEnum.Falha,
                )

            # INTERAGINDO COM O CAMPO Manter Natureza de Operação selecionada
            console.print(
                f"Selecionando a opção 'Manter Natureza de Operação selecionada'...\n"
            )
            checkbox = window.child_window(
                title="Manter Natureza de Operação selecionada",
                class_name="TDBICheckBox",
            )
            if not checkbox.get_toggle_state() == 1:
                checkbox.click()
                console.print(
                    "A opção 'Manter Natureza de Operação selecionada' selecionado com sucesso... \n"
                )

            await worker_sleep(2)
            console.print("Clicando em OK... \n")


            console.print("Clicando em OK... \n")

            max_attempts = 3
            i = 0
            while i < max_attempts:
                console.print("Clicando no botão de OK...\n")
                try:
                    try:
                        btn_ok = main_window.child_window(title="Ok")
                        btn_ok.click()
                    except:
                        btn_ok = main_window.child_window(title="&Ok")
                        btn_ok.click()
                except:
                    console.print("Não foi possivel clicar no Botão OK... \n")

                await worker_sleep(1)
                i += 1
        except:
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao importar nota fiscal.",
                status=RpaHistoricoStatusEnum.Descartado,
            )
        
        await worker_sleep(40)

        await emsys.verify_warning_and_error("Information", "&No")

        await worker_sleep(3)

        # Seleciona pagamento
        console.log("Seleciona Pagamento", style="bold yellow")
        pyautogui.click(623, 374)
        await worker_sleep(1)
        pyautogui.click(889, 349)
        await worker_sleep(1)
        pyautogui.write("27")
        await worker_sleep(1)
        pyautogui.hotkey("enter")

        # Digita "Valor"

        pyautogui.click(1285, 352)
        await worker_sleep(1)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("del")
        await worker_sleep(1)
        pyautogui.write(nota["valorNota"])

        await emsys.incluir_registro()
        await worker_sleep(30)

        await worker_sleep(5)
        console.print(
            "Verificando a existencia de POP-UP de Itens que Ultrapassam a Variação Máxima de Custo ...\n"
        )
        itens_variacao_maxima = await is_window_open_by_class(
            "TFrmTelaSelecao", "TFrmTelaSelecao"
        )
        if itens_variacao_maxima["IsOpened"] == True:
            app = Application().connect(class_name="TFrmTelaSelecao")
            main_window = app["TFrmTelaSelecao"]
            send_keys("%o")

        await worker_sleep(3)
        console.print(
            "Verificando a existencia de POP-UP de Itens que Ultrapassam a Variação Máxima de Custo ...\n"
        )
        itens_variacao_maxima = await is_window_open_by_class(
            "TFrmTelaSelecao", "TFrmTelaSelecao"
        )
        if itens_variacao_maxima["IsOpened"] == True:
            app = Application().connect(class_name="TFrmTelaSelecao")
            main_window = app["TFrmTelaSelecao"]
            send_keys("%o")

        await worker_sleep(2)
        console.print(
            "Verificando a existencia de Warning informando que a Soma dos pagamentos não bate com o valor da nota. ...\n"
        )
        app = Application().connect(class_name="TFrmNotaFiscalEntrada")
        main_window = app["TFrmNotaFiscalEntrada"]

        try:
            warning_pop_up_pagamentos = main_window.child_window(
                class_name="TMessageForm", title="Warning"
            )
        except:
            warning_pop_up_pagamentos = None

        if warning_pop_up_pagamentos.exists():
            console.print(
                "Erro: Warning informando que a Soma dos pagamentos não bate com o valor da nota. ...\n"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"A soma dos pagamentos não bate com o valor da nota.",
                status=RpaHistoricoStatusEnum.Falha,
            )
        else:
            console.print(
                "Warning informando que a Soma dos pagamentos não bate com o valor da nota não existe ...\n"
            )

        max_attempts = 7
        i = 0
        aguarde_rateio_despesa = True

        while i < max_attempts:
            await worker_sleep(3)

            from pywinauto import Desktop

            for window in Desktop(backend="uia").windows():
                if "Rateio" in window.window_text():
                    aguarde_rateio_despesa = False
                    console.print(
                        "A janela 'Rateio da Despesas' foi encontrada. Continuando para andamento do processo...\n"
                    )
                    break

            if not aguarde_rateio_despesa:
                break

            i += 1

        if aguarde_rateio_despesa:
            console.log(f"Número máximo de tentativas atingido. A tela para Rateio da Despesa não foi encontrada.")

        if not aguarde_rateio_despesa:
            despesa_rateio_work = await rateio_despesa(nota.get("filialEmpresaOrigem"))
            if despesa_rateio_work.sucesso == True:
                console.log(despesa_rateio_work.retorno, style="bold green")
            else:
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=despesa_rateio_work.retorno,
                    status=RpaHistoricoStatusEnum.Falha,
                )

        # Verifica se a info 'Nota fiscal incluida' está na tela
        await worker_sleep(15)
        warning_pop_up = await is_window_open("Warning")
        if warning_pop_up["IsOpened"] == True:
            app = Application().connect(title="Warning")
            main_window = app["Warning"]
            main_window.set_focus()

            console.print(f"Obtendo texto do Warning...\n")
            console.print(f"Tirando print da janela do warning para realização do OCR...\n")

            window_rect = main_window.rectangle()
            screenshot = pyautogui.screenshot(
                region=(
                    window_rect.left,
                    window_rect.top,
                    window_rect.width(),
                    window_rect.height(),
                )
            )
            username = getpass.getuser()
            path_to_png = f"C:\\Users\\{username}\\Downloads\\warning_popup_{nota.get("nfe")}.png"
            screenshot.save(path_to_png)
            console.print(f"Print salvo em {path_to_png}...\n")

            console.print(
                f"Preparando a imagem para maior resolução e assertividade no OCR...\n"
            )
            image = Image.open(path_to_png)
            image = image.convert("L")
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            image.save(path_to_png)
            console.print(f"Imagem preparada com sucesso...\n")
            console.print(f"Realizando OCR...\n")
            captured_text = pytesseract.image_to_string(Image.open(path_to_png))
            console.print(
                f"Texto Full capturado {captured_text}...\n"
            )
            os.remove(path_to_png)
            if 'movimento não permitido' in captured_text.lower():
                return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Filial: {nota.get("filialEmpresaOrigem")} está com o livro fechado ou encerrado, verificar com o setor fiscal",
                status=RpaHistoricoStatusEnum.Falha,
                )
            else:
                return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Warning não mapeado para seguimento do robo, mensagem: {captured_text}",
                status=RpaHistoricoStatusEnum.Falha,
                )
            
        await worker_sleep(3)
        retorno = False
        try:
            max_attempts = 60
            i = 0

            while i < max_attempts:
                information_pop_up = await is_window_open("Information")
                if information_pop_up["IsOpened"] == True:
                    break
                else:
                    console.print(f"Aguardando confirmação de nota incluida...\n")
                    await worker_sleep(5)
                    i += 1

            information_pop_up = await is_window_open("Information")
            if information_pop_up["IsOpened"] == True:
                app = Application().connect(class_name="TFrmNotaFiscalEntrada")
                main_window = app["Information"]

                main_window.set_focus()

                console.print(f"Obtendo texto do Information...\n")
                console.print(f"Tirando print da janela do Information para realização do OCR...\n")

                window_rect = main_window.rectangle()
                screenshot = pyautogui.screenshot(
                    region=(
                        window_rect.left,
                        window_rect.top,
                        window_rect.width(),
                        window_rect.height(),
                    )
                )
                username = getpass.getuser()
                path_to_png = f"C:\\Users\\{username}\\Downloads\\information_popup_{nota.get("nfe")}.png"
                screenshot.save(path_to_png)
                console.print(f"Print salvo em {path_to_png}...\n")

                console.print(
                    f"Preparando a imagem para maior resolução e assertividade no OCR...\n"
                )
                image = Image.open(path_to_png)
                image = image.convert("L")
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(2.0)
                image.save(path_to_png)
                console.print(f"Imagem preparada com sucesso...\n")
                console.print(f"Realizando OCR...\n")
                captured_text = pytesseract.image_to_string(Image.open(path_to_png))
                console.print(
                    f"Texto Full capturado {captured_text}...\n"
                )
                os.remove(path_to_png)
                if 'nota fiscal inc' in captured_text.lower():
                    console.print(f"Tentando clicar no Botão OK...\n")
                    btn_ok = main_window.child_window(class_name="TButton")

                    if btn_ok.exists():
                        btn_ok.click()
                        retorno = True
                else:
                    return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Pop_up Informantion não mapeado para andamento do robô, mensagem {captured_text}",
                        status=RpaHistoricoStatusEnum.Falha,
                    )
            else:
                console.print(f"Aba Information não encontrada")
                retorno = await verify_nf_incuded()

        except Exception as e:
            console.print(f"Erro ao conectar à janela Information: {e}\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro em obter o retorno, Nota inserida com sucesso, erro {e}",
                status=RpaHistoricoStatusEnum.Falha,
            )

        if retorno:
            console.print("\nNota lançada com sucesso...", style="bold green")
            await worker_sleep(6)
            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Nota Lançada com sucesso!",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
        else:
            console.print("Erro ao lançar nota", style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao lançar nota",
                status=RpaHistoricoStatusEnum.Falha,
            )

    except Exception as ex:
        observacao = f"Erro Processo Entrada de Notas: {str(ex)}"
        logger.error(observacao)
        console.print(observacao, style="bold red")
        return {"sucesso": False, "retorno": observacao}

    finally:
        await kill_process("EMSys")
