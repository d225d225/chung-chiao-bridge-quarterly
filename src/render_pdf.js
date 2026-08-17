const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const inPath = process.argv[2];
  const outPath = process.argv[3];
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(inPath), { waitUntil: 'networkidle0', timeout: 120000 });
  await page.pdf({
    path: outPath,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: `<div style="width:100%; font-size:7.5px; font-family: 'PingFang TC','Heiti TC',sans-serif; color:#8a7a55; text-align:center; padding-top:2px;">中橋季刊．2026秋季號　－　<span class="pageNumber"></span> / <span class="totalPages"></span></div>`,
    margin: { top: '0mm', bottom: '12mm', left: '0mm', right: '0mm' },
  });
  await browser.close();
  console.log('PDF written to', outPath);
})();
