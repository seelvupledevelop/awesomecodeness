import { build } from "bun";
import { SolidPlugin } from "bun-plugin-solid";

await build({
  entrypoints: ["./index.tsx"],
  outdir: "./dist",
  plugins: [SolidPlugin({ generate: "universal", moduleName: "@opentui/solid" })],
  target: "bun",
  external: ["@opentui/solid", "@opentui/core", "solid-js"]
});

const { spawn } = require("child_process");
spawn("bun", ["dist/index.js"], { stdio: "inherit" });
