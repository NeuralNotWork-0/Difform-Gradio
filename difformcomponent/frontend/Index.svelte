<svelte:options accessors={true} />

<script lang="ts">
	import type { Gradio } from "@gradio/utils";

	import { BlockTitle } from "@gradio/atoms";
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import { Empty } from "@gradio/atoms";
	import { Music } from "@gradio/icons";

	import type { WaveformOptions } from "@gradio/audio";
	import { BaseStaticAudio } from "@gradio/audio";
	import { normalise_file } from "@gradio/client";
	import type { FileData } from "@gradio/client";
	
	import AudioGraph from "./audio_graph/AudioGraph.svelte";

	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let interactive: boolean;
	export let value: null | any = null;
	export let sources:
		| ["microphone"]
		| ["upload"]
		| ["microphone", "upload"]
		| ["upload", "microphone"];
	export let label: string;
	export let root: string;
	export let show_label: boolean;
	export let proxy_url: null | string;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let autoplay = false;
	export let show_download_button = true;
	export let show_share_button = false;
	export let waveform_options: WaveformOptions = {};
	export let gradio: Gradio<{
		audio_select: string;
		error: string;
		warning: string;
		edit: never;
		play: never;
		pause: never;
		stop: never;
		share: ShareData;
	}>;

	let audio: null | FileData;
	$: if (value.audio !== null) {
		audio = normalise_file(value.audio, root, proxy_url);
	}

	let active_source: "microphone" | "upload";

	$: if (!active_source && sources) {
		active_source = sources[0];
	}

	let waveform_settings: Record<string, any>;

	$: waveform_settings = {
		height: 50,
		waveColor: waveform_options.waveform_color || "#9ca3af",
		progressColor: waveform_options.waveform_progress_color || "#f97316",
		barWidth: 2,
		barGap: 3,
		cursorWidth: 2,
		cursorColor: "#ddd5e9",
		autoplay: autoplay,
		barRadius: 10,
		dragToSeek: true,
		normalize: true,
		minPxPerSec: 20,
		mediaControls: waveform_options.show_controls
	};

	const trim_region_settings = {
		color: waveform_options.trim_region_color || "hsla(15, 85%, 40%, 0.4)",
		drag: true,
		resize: true
	};
</script>

<Block
	{visible}
	{elem_id}
	{elem_classes}
	{scale}
	{min_width}
	allow_overflow={false}
	padding={true}
>
	{#if loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
		/>
	{/if}

	<BlockTitle {show_label} info={undefined}>{label}</BlockTitle>
	<AudioGraph
		graph_data={value.graph_data}
		on:audio_select={(e) => gradio.dispatch("audio_select", e.detail)}
	/>
	{#if audio !== null}
		<BaseStaticAudio
			i18n={gradio.i18n}
			{show_label}
			{show_download_button}
			{show_share_button}
			value={audio}
			{label}
			{waveform_settings}
			{waveform_options}
			on:share={(e) => gradio.dispatch("share", e.detail)}
			on:error={(e) => gradio.dispatch("error", e.detail)}
			on:play={() => gradio.dispatch("play")}
			on:pause={() => gradio.dispatch("pause")}
			on:stop={() => gradio.dispatch("stop")}
		/>
	{:else}
		<Empty size="small">
			<Music />
		</Empty>
	{/if}
</Block>