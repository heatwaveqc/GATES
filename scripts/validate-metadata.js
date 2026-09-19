const fs = require("fs");
const path = require("path");

const ROOT = path.join(process.cwd(), "tiddlers");
const REQUIRED = ["gates-audience", "gates-section", "gates-kind"];
const AUDIENCES = new Set(["player", "gm", "ai"]);
const SECTIONS = new Set([
  "Campaigns",
  "System",
  "Design",
  "Domains",
  "Gods",
  "Monsters",
  "Setting",
  "Species",
  "Technology",
  "AI Instruction",
  "Art"
]);

function walk(dir) {
  return fs.readdirSync(dir, {withFileTypes:true}).flatMap(entry => {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) return walk(full);
    return entry.isFile() && entry.name.endsWith(".tid") ? [full] : [];
  });
}

function parseHeader(text) {
  const header = text.split(/\r?\n\r?\n/, 1)[0];
  const fields = {};
  for (const line of header.split(/\r?\n/)) {
    const idx = line.indexOf(":");
    if (idx < 1) continue;
    fields[line.slice(0, idx).trim()] = line.slice(idx + 1).trim();
  }
  return fields;
}

const errors = [];
let classified = 0;
let unclassified = 0;

for (const file of walk(ROOT)) {
  const fields = parseHeader(fs.readFileSync(file, "utf8"));
  const title = fields.title || "";
  if (title.startsWith("$:/")) continue;

  const hasClassification = REQUIRED.some(field => Boolean(fields[field]));
  if (!hasClassification) {
    unclassified += 1;
    continue;
  }

  classified += 1;

  for (const field of REQUIRED) {
    if (!fields[field]) errors.push(`${file}: missing ${field}`);
  }

  if (fields["gates-audience"] && !AUDIENCES.has(fields["gates-audience"])) {
    errors.push(`${file}: invalid gates-audience "${fields["gates-audience"]}"`);
  }

  if (fields["gates-section"] && !SECTIONS.has(fields["gates-section"])) {
    errors.push(`${file}: invalid gates-section "${fields["gates-section"]}"`);
  }
}

if (errors.length) {
  console.error("GATES metadata validation failed:");
  for (const error of errors) console.error(` - ${error}`);
  process.exit(1);
}

console.log(`Validated ${classified} classified tiddlers; ${unclassified} legacy tiddlers remain unclassified and will fail closed out of human builds.`);
