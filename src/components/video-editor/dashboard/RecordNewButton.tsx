import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function RecordNewButton({
	busy,
	run,
	className,
	first = false,
}: {
	busy: boolean;
	run: (action: () => Promise<void>) => Promise<void>;
	className?: string;
	first?: boolean;
}) {
	return (
		<Button
			variant="default"
			disabled={busy}
			onClick={() => void run(() => window.electronAPI.showRecordingHud())}
			className={cn(
				"h-10 shrink-0 gap-2.5 text-[13px] font-medium transition-all duration-200 active:scale-[0.98] shadow-sm hover:shadow",
				className,
			)}
		>
			<span className="relative flex size-2.5">
				<span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-red-400 opacity-75" />
				<span className="relative inline-flex size-2.5 rounded-full bg-red-500" />
			</span>
			<span>{first ? "Record your first video" : "New Recording"}</span>
		</Button>
	);
}
