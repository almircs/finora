// Ponte segura entre a janela e o disco: só estas funções ficam visíveis para a página.
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('finora', {
  load: () => ipcRenderer.invoke('data:load'),
  saveSync: (json) => ipcRenderer.sendSync('data:save', json),
  saveFile: (name, data) => ipcRenderer.invoke('file:save', name, data),
  openDataFolder: () => ipcRenderer.invoke('app:openDataFolder'),
  dataPath: () => ipcRenderer.invoke('app:dataPath')
});
