import path from "node:path";
import { app } from "electron";

if (process.env["VITE_DEV_SERVER_URL"] && typeof app?.getPath === "function") {
	const devUserDataPath = path.join(app.getPath("appData"), "RecoreAle-dev");
	app.setPath("userData", devUserDataPath);
	app.setPath("sessionData", path.join(devUserDataPath, "session"));
}

export const USER_DATA_PATH = typeof app?.getPath === "function" ? app.getPath("userData") : "";
export const RECORDINGS_DIR = path.join(USER_DATA_PATH, "recordings");
