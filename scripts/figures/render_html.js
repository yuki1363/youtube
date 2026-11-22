// 図解画像生成部門：HTML/SVGで描いた図を 1080x1920 のPNGにする（Chromiumで描画）
// 使い方: node scripts/figures/render_html.js <出力フォルダ> <図1.html> [<図2.html> ...]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [outDir, ...files] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  for (const f of files) {
    await page.goto('file://' + path.resolve(f));
    await page.evaluate(() => document.fonts.ready);
    const out = path.join(outDir, path.basename(f, '.html') + '.png');
    await page.screenshot({ path: out });
    console.log('出力:', out);
  }
  await browser.close();
})();
