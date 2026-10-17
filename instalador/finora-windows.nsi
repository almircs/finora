Unicode true
ManifestDPIAware true
!include "MUI2.nsh"
!define APPNAME "Finora"
!define EXENAME "Finora.exe"
!define VERSION "2.1.0"
!define UNKEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\Finora"
Name "${APPNAME}"
Caption "Instalar ${APPNAME}"
OutFile "instalador-windows.exe"
InstallDir "$LOCALAPPDATA\Programs\Finora"
InstallDirRegKey HKCU "Software\Finora" "InstallDir"
RequestExecutionLevel user
SetCompressor /SOLID lzma
SetCompressorDictSize 64
BrandingText "${APPNAME} ${VERSION}"
!define MUI_ICON "payload\icon.ico"
!define MUI_UNICON "payload\icon.ico"
!define MUI_ABORTWARNING
!define MUI_WELCOMEFINISHPAGE_BITMAP "welcome.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "welcome.bmp"
!define MUI_WELCOMEPAGE_TITLE "Bem-vindo ao Finora"
!define MUI_WELCOMEPAGE_TEXT "Este assistente vai instalar o Finora, seu controle de receitas e despesas.$\r$\n$\r$\nNão é preciso ser administrador. Ao terminar, você encontra o Finora na Área de Trabalho e no Menu Iniciar.$\r$\n$\r$\nSe você usava o Caixa Diário, seus lançamentos são trazidos automaticamente.$\r$\n$\r$\nClique em Avançar para instalar."
!define MUI_FINISHPAGE_TITLE "Pronto!"
!define MUI_FINISHPAGE_TEXT "O Finora foi instalado.$\r$\n$\r$\nPara trazer seus dados do Gastos Diários, abra Backup e ajustes e escolha o arquivo database.sqlite."
!define MUI_FINISHPAGE_RUN "$INSTDIR\${EXENAME}"
!define MUI_FINISHPAGE_RUN_TEXT "Abrir o Finora agora"
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "PortugueseBR"
VIProductVersion "2.1.0.0"
VIAddVersionKey /LANG=${LANG_PORTUGUESEBR} "ProductName" "${APPNAME}"
VIAddVersionKey /LANG=${LANG_PORTUGUESEBR} "FileDescription" "Instalador do ${APPNAME}"
VIAddVersionKey /LANG=${LANG_PORTUGUESEBR} "FileVersion" "${VERSION}"
VIAddVersionKey /LANG=${LANG_PORTUGUESEBR} "ProductVersion" "${VERSION}"
VIAddVersionKey /LANG=${LANG_PORTUGUESEBR} "LegalCopyright" "${APPNAME}"
Section "Instalar"
  nsExec::Exec 'taskkill /F /IM ${EXENAME}'
  nsExec::Exec 'taskkill /F /IM CaixaDiario.exe'
  Sleep 500
  RMDir /r "$INSTDIR\resources\app"
  SetOutPath "$INSTDIR"
  File /r "payload\*.*"
  WriteUninstaller "$INSTDIR\Desinstalar.exe"
  ; remove a versão anterior (Caixa Diário); os lançamentos dela continuam guardados e o Finora os importa
  Delete "$DESKTOP\Caixa Diário.lnk"
  Delete "$SMPROGRAMS\Caixa Diário.lnk"
  RMDir /r "$LOCALAPPDATA\Programs\Caixa Diario"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\CaixaDiario"
  DeleteRegKey HKCU "Software\CaixaDiario"
  CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${EXENAME}" "" "$INSTDIR\icon.ico" 0
  CreateShortCut "$SMPROGRAMS\${APPNAME}.lnk" "$INSTDIR\${EXENAME}" "" "$INSTDIR\icon.ico" 0
  WriteRegStr HKCU "Software\Finora" "InstallDir" "$INSTDIR"
  WriteRegStr HKCU "${UNKEY}" "DisplayName" "${APPNAME}"
  WriteRegStr HKCU "${UNKEY}" "DisplayVersion" "${VERSION}"
  WriteRegStr HKCU "${UNKEY}" "Publisher" "${APPNAME}"
  WriteRegStr HKCU "${UNKEY}" "DisplayIcon" "$INSTDIR\icon.ico"
  WriteRegStr HKCU "${UNKEY}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKCU "${UNKEY}" "UninstallString" '"$INSTDIR\Desinstalar.exe"'
  WriteRegDWORD HKCU "${UNKEY}" "NoModify" 1
  WriteRegDWORD HKCU "${UNKEY}" "NoRepair" 1
  WriteRegDWORD HKCU "${UNKEY}" "EstimatedSize" 230000
SectionEnd
Section "Uninstall"
  nsExec::Exec 'taskkill /F /IM ${EXENAME}'
  Sleep 500
  Delete "$DESKTOP\${APPNAME}.lnk"
  Delete "$SMPROGRAMS\${APPNAME}.lnk"
  RMDir /r "$INSTDIR"
  DeleteRegKey HKCU "${UNKEY}"
  DeleteRegKey HKCU "Software\Finora"
  ; Os lançamentos (pasta AppData\Roaming\Finora) são mantidos de propósito.
SectionEnd
