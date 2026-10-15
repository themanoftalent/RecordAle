import { LibrarySkeleton } from "./LibrarySkeleton";
import { SharedRecordings } from "../cloud/SharedRecordings";
import { CLOUD_SHARE_ENDPOINT } from "../cloud/endpoint";
import { RecordNewButton } from "./RecordNewButton";
import { RawPreview } from "./RawRecordings";
import { Cloud, ImageSquare } from "@/components/ui/icons";

import { Button } from "@/components/ui/button";

import { DashboardSettings } from "./DashboardSettings";

import { ProjectCard } from "./ProjectCard";
import type { DashboardProps } from "./types";

import type { DashboardModel } from "./useDashboardModel";

export function DashboardGrid({
	onImportFile,
	loading,
	isRaw,
	rawPreview,
	setRawPreview,
	rawLoading,
	rawError,
	refreshRaw,
	error,
	section,
	accountLabel,
	authToken,
	onSignIn,
	onShareProject,
	visible,
	busy,
	selecting,
	toggleSelected,
	onRenameProject,
	folders,
	save,
	assignFolder,
	selected,
	openEntry,
	query,
	hasActiveFilters,
	setQuery,
	run,
	deleteEntries,
}: Pick<
	DashboardProps & DashboardModel,
	| "loading"
	| "onImportFile"
	| "isRaw"
	| "rawPreview"
	| "setRawPreview"
	| "rawLoading"
	| "rawError"
	| "refreshRaw"
	| "error"
	| "section"
	| "accountLabel"
	| "authToken"
	| "onSignIn"
	| "onShareProject"
	| "visible"
	| "busy"
	| "selecting"
	| "toggleSelected"
	| "onRenameProject"
	| "folders"
	| "save"
	| "assignFolder"
	| "selected"
	| "openEntry"
	| "query"
	| "hasActiveFilters"
	| "setQuery"
	| "deleteEntries"
	| "run"
>) {
	return (
		<>
			<main className="custom-scrollbar min-h-0 flex-1 overflow-y-auto px-7 pb-10 lg:px-10">
				{error && (
					<p role="alert" className="mb-4 text-sm text-danger">
						{error}
					</p>
				)}
				{section === "settings" ? (
					<DashboardSettings onImportFile={onImportFile} />
				) : section === "shared" ? (
					authToken && CLOUD_SHARE_ENDPOINT ? (
						<div>
							<SharedRecordings
								key={authToken}
								token={authToken}
								endpoint={CLOUD_SHARE_ENDPOINT}
								accountLabel={accountLabel}
								standalone
							/>
						</div>
					) : (
						<div className="flex h-64 flex-col items-center justify-center gap-3 text-sm text-muted-foreground">
							<Cloud weight="fill" className="size-8 opacity-40" />
							<p>
								{authToken
									? "Cloud sharing is not available in this build yet."
									: "Sign in to manage shared videos."}
							</p>
							{!authToken && (
								<Button variant="secondary" onClick={onSignIn}>
									Sign in
								</Button>
							)}
						</div>
					)
				) : (isRaw ? rawLoading : loading) ? (
					<LibrarySkeleton />
				) : visible.length ? (
					<ul
						aria-label={isRaw ? "Raw files" : "Your projects"}
						className="grid grid-cols-[repeat(auto-fill,minmax(min(100%,280px),1fr))] gap-x-7 gap-y-10 lg:gap-x-9"
					>
						{visible.map((entry) => (
							<ProjectCard
								key={entry.path}
								onDelete={() => void deleteEntries([entry.path])}
								{...{
									accountLabel,
									entry,
									busy,
									selecting,
									selected,
									toggleSelected,
									openEntry,
									run,
									onShareProject,
									onRenameProject,
									folders,
									save,
									assignFolder,
								}}
							/>
						))}
					</ul>
				) : (
					<div className="flex min-h-[380px] flex-1 flex-col items-center justify-center px-4 text-center">
						{!isRaw && !hasActiveFilters ? (
							<div className="flex max-w-md flex-col items-center gap-4 py-8">
								<div className="relative flex size-16 items-center justify-center rounded-2xl bg-gradient-to-br from-red-500/15 via-red-500/5 to-transparent ring-1 ring-red-500/25 shadow-lg shadow-red-500/10">
									<span className="relative flex size-5">
										<span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-red-400 opacity-60" />
										<span className="relative inline-flex size-5 rounded-full bg-red-500 shadow-sm" />
									</span>
								</div>
								<div className="space-y-1.5">
									<h3 className="text-lg font-semibold tracking-tight text-foreground">
										Ready to capture something great?
									</h3>
									<p className="text-xs leading-relaxed text-muted-foreground">
										Record your screen, camera, and microphone with smooth zoom animations, smart cursor tracking, and studio audio.
									</p>
								</div>
								<RecordNewButton busy={busy} run={run} first className="mt-2 h-11 px-6 text-sm shadow-md" />
								<div className="mt-4 flex flex-wrap items-center justify-center gap-2 text-[11px] text-muted-foreground/80">
									<span className="inline-flex items-center gap-1.5 rounded-full bg-foreground/5 px-2.5 py-1">
										⚡ 60 FPS & 4K
									</span>
									<span className="inline-flex items-center gap-1.5 rounded-full bg-foreground/5 px-2.5 py-1">
										🔒 100% Private On-Device
									</span>
									<span className="inline-flex items-center gap-1.5 rounded-full bg-foreground/5 px-2.5 py-1">
										🪄 Auto-Zoom Effects
									</span>
								</div>
							</div>
						) : (
							<div className="flex flex-col items-center justify-center gap-3 text-sm text-muted-foreground">
								<ImageSquare weight="fill" className="size-8 opacity-30" />
								<p>
									{isRaw
										? rawLoading
											? "Loading recordings…"
											: rawError ||
												(hasActiveFilters
													? "No matching raw files"
													: "No raw recordings yet")
										: "No matching projects"}
								</p>
								{isRaw && rawError && (
									<Button onClick={() => void refreshRaw()}>Retry</Button>
								)}
								{query && (
									<Button variant="ghost" size="sm" onClick={() => setQuery("")}>
										Clear search
									</Button>
								)}
							</div>
						)}
					</div>
				)}
				<RawPreview entry={rawPreview} onClose={() => setRawPreview(null)} />
			</main>
		</>
	);
}
