import Handlebars from "handlebars";
import fs from "fs";

const template = fs.readFileSync("index.html.handlebars", "utf8");

/** @type {{ name: string, version: string, updated: string, url: string, censored: string | boolean}[]} */
let raw_mods = JSON.parse(fs.readFileSync("censorship.json", "utf8"));
let mods = raw_mods
    .map((mod) => ({ ...mod, version: parseFloat(mod.version) }))
    .sort((a, b) => {
        if (a.censored != b.censored) {
            if (a.censored) {
                return -1;
            } else {
                return 1;
            }
        }

        if (a.version != b.version) {
            return b.version - a.version;
        }

        return a.name.localeCompare(b.name);
    });

let latest_version = mods.reduce((max, mod) => Math.max(max, mod.version), 0);
mods.forEach((mod) => {
    mod.outdated = mod.version < latest_version;
});

const render = Handlebars.compile(template);
const summary = Handlebars.compile(
    "{{#each mods}}{{#if censored}}{{name}}: {{censored}} ({{{url}}})\n{{/if}}{{/each}}"
)({ mods });
const content = render({
    mods,
    any_censorship: mods.some((mod) => mod.censored),
    summary,
});

if (!fs.existsSync("_site")) {
    fs.mkdirSync("_site");
}

fs.writeFileSync("_site/index.html", content, "utf8");
fs.writeFileSync("_site/censorship.txt", summary, "utf8");
