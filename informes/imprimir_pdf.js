// Imprime el HTML del informe a PDF A4 con Chromium (Playwright).
// Uso: node imprimir_pdf.js entrada.html salida.pdf
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [entrada, salida] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(entrada), { waitUntil: 'load' });
  await page.pdf({
    path: salida,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate:
      '<div style="width:100%;font-family:Inter,sans-serif;font-size:7px;color:#888;padding:0 14mm;display:flex;justify-content:space-between">' +
      '<span>Hoja de ruta maestra · 3 canales · 2026</span>' +
      '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
    margin: { top: '14mm', bottom: '16mm', left: '14mm', right: '14mm' },
  });
  await browser.close();
})();
