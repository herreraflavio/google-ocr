const fs = require("fs").promises;
const path = require("path");

const rootDir = "./data/arpa-orders-sample/";
let totalfiles = 0;

async function findPdfFiles(dirPath) {
  try {
    const files = await fs.readdir(dirPath);

    for (const file of files) {
      const filePath = path.join(dirPath, file);
      const stats = await fs.stat(filePath);

      if (stats.isDirectory()) {
        // Recursive call if it's a directory
        await findPdfFiles(filePath);
      } else if (stats.isFile() && file.endsWith(".pdf")) {
        // Increment and log PDF file
        totalfiles++;
        console.log(`PDF File: ${file} (Path: ${filePath})`);
      }
    }
  } catch (err) {
    console.error(`Error accessing ${dirPath}:`, err);
  }
}

(async () => {
  // Start the search
  await findPdfFiles(rootDir);
  console.log(`Total PDF files found: ${totalfiles}`);
})();
