// Finora — processo principal do Electron
const { app, BrowserWindow, ipcMain, dialog, Menu, shell } = require('electron');
const path = require('path');
const fs = require('fs');

const DATA_NAME = 'finora.json';

// Datas, menus e caixas do sistema em português do Brasil.
app.commandLine.appendSwitch('lang', 'pt-BR');
const OLD_DIR_NAME = 'Caixa Diário';
const OLD_DATA_NAME = 'caixa-diario.json';
const KEEP_BACKUPS = 30;
let win = null;

const dataDir = () => app.getPath('userData');
const dataFile = () => path.join(dataDir(), DATA_NAME);
const backupDir = () => path.join(dataDir(), 'backups');

// Uma janela só: abrir o programa de novo traz a janela existente para a frente.
if (!app.requestSingleInstanceLock()) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (win) { if (win.isMinimized()) win.restore(); win.focus(); }
  });
}

function loadData() {
  try { return fs.readFileSync(dataFile(), 'utf8'); } catch { /* segue */ }
  // Primeira vez no Finora: aproveita os dados da versão anterior (Caixa Diário), se existirem.
  try {
    const old = path.join(app.getPath('appData'), OLD_DIR_NAME, OLD_DATA_NAME);
    if (fs.existsSync(old)) return fs.readFileSync(old, 'utf8');
  } catch { /* sem versão anterior */ }
  return null;
}

// Grava num arquivo temporário e depois troca, para nunca deixar o arquivo pela metade.
function saveData(json) {
  fs.mkdirSync(dataDir(), { recursive: true });
  const tmp = dataFile() + '.tmp';
  fs.writeFileSync(tmp, json, 'utf8');
  fs.renameSync(tmp, dataFile());
  dailyBackup(json);
}

// Uma cópia automática por dia (com o estado mais recente daquele dia), guardando as últimas 30.
function dailyBackup(json) {
  try {
    fs.mkdirSync(backupDir(), { recursive: true });
    const today = new Date();
    const stamp = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
    const file = path.join(backupDir(), `finora-${stamp}.json`);
    const tmp = file + '.tmp';
    fs.writeFileSync(tmp, json, 'utf8');
    fs.renameSync(tmp, file);
    const all = fs.readdirSync(backupDir()).filter(f => /^finora-\d{4}-\d{2}-\d{2}\.json$/.test(f)).sort();
    for (const old of all.slice(0, Math.max(0, all.length - KEEP_BACKUPS))) fs.unlinkSync(path.join(backupDir(), old));
  } catch { /* backup automático é opcional */ }
}

ipcMain.handle('data:load', () => loadData());
ipcMain.on('data:save', (event, json) => {
  try { saveData(json); event.returnValue = true; }
  catch (e) { event.returnValue = false; }
});
ipcMain.handle('file:save', async (event, name, data) => {
  const ext = path.extname(name).slice(1).toLowerCase();
  const labels = { sqlite: 'Banco de dados do Gastos Diários', json: 'Backup do Finora', csv: 'Planilha CSV' };
  const res = await dialog.showSaveDialog(win, {
    title: 'Salvar arquivo',
    defaultPath: path.join(app.getPath('documents'), name),
    filters: [{ name: labels[ext] || 'Arquivo', extensions: [ext || '*'] }, { name: 'Todos os arquivos', extensions: ['*'] }]
  });
  if (res.canceled || !res.filePath) return { saved: false };
  const buf = typeof data === 'string' ? Buffer.from(data, 'utf8') : Buffer.from(data);
  fs.writeFileSync(res.filePath, buf);
  return { saved: true, path: res.filePath };
});
ipcMain.handle('app:openDataFolder', () => shell.openPath(dataDir()));
ipcMain.handle('app:dataPath', () => dataFile());

function buildMenu() {
  const isMac = process.platform === 'darwin';
  const template = [
    ...(isMac ? [{ label: 'Finora', submenu: [
      { role: 'about', label: 'Sobre o Finora' }, { type: 'separator' },
      { role: 'hide', label: 'Ocultar' }, { role: 'hideOthers', label: 'Ocultar outros' }, { role: 'unhide', label: 'Mostrar todos' },
      { type: 'separator' }, { role: 'quit', label: 'Sair' }] }] : []),
    { label: 'Arquivo', submenu: [
      { label: 'Abrir pasta dos dados', click: () => shell.openPath(dataDir()) },
      { label: 'Abrir pasta das cópias automáticas', click: () => { fs.mkdirSync(backupDir(), { recursive: true }); shell.openPath(backupDir()); } },
      { type: 'separator' },
      isMac ? { role: 'close', label: 'Fechar janela' } : { role: 'quit', label: 'Sair' }] },
    { label: 'Editar', submenu: [
      { role: 'undo', label: 'Desfazer' }, { role: 'redo', label: 'Refazer' }, { type: 'separator' },
      { role: 'cut', label: 'Recortar' }, { role: 'copy', label: 'Copiar' }, { role: 'paste', label: 'Colar' },
      { role: 'selectAll', label: 'Selecionar tudo' }] },
    { label: 'Exibir', submenu: [
      { role: 'reload', label: 'Recarregar' }, { type: 'separator' },
      { role: 'resetZoom', label: 'Tamanho normal' }, { role: 'zoomIn', label: 'Aumentar' }, { role: 'zoomOut', label: 'Diminuir' },
      { type: 'separator' }, { role: 'togglefullscreen', label: 'Tela cheia' }] }
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

function createWindow() {
  win = new BrowserWindow({
    width: 1320, height: 860, minWidth: 380, minHeight: 500,
    title: 'Finora',
    icon: path.join(__dirname, 'build', 'icon.png'),
    backgroundColor: '#EEF3F1',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      spellcheck: false
    }
  });
  win.loadFile(path.join(__dirname, 'app', 'index.html'));
  // Links externos abrem no navegador; a janela do programa nunca sai do app.
  win.webContents.setWindowOpenHandler(({ url }) => { if (/^https?:/.test(url)) shell.openExternal(url); return { action: 'deny' }; });
  win.webContents.on('will-navigate', (e, url) => { if (!url.startsWith('file:')) { e.preventDefault(); if (/^https?:/.test(url)) shell.openExternal(url); } });
  win.on('closed', () => { win = null; });
}

app.whenReady().then(() => {
  buildMenu();
  createWindow();
  app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });
});
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
