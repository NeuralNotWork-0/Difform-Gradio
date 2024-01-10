<svelte:options accessors={true} />

<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import { BlockTitle } from "@gradio/atoms";
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import { Empty } from "@gradio/atoms";
	import { Download, Music } from "@gradio/icons";
	import type { I18nFormatter } from "@gradio/utils";
	import type { WaveformOptions } from "@gradio/audio";
	import { BasePlayer } from "@gradio/audio";
	import { tick } from "svelte";

	
	import AudioGraph from "./audio_graph/AudioGraph.svelte";

	export let gradio: Gradio<{
		change: never;
		submit: never;
		input: never;
	}>;
	export let label = "Difform";
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: any = null;
	export let placeholder = "";
	export let show_label: boolean;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus | undefined = undefined;
	export let value_is_output = false;
	export let interactive: boolean;
	export let rtl = false;

	export let i18n: I18nFormatter;
	export let waveform_options: WaveformOptions = {};

	let waveform_settings: Record<string, any>;

	$: waveform_settings = {
		height: 50,
		waveColor: waveform_options.waveform_color || "#9ca3af",
		progressColor: waveform_options.waveform_progress_color || "#f97316",
		barWidth: 2,
		barGap: 3,
		cursorWidth: 2,
		cursorColor: "#ddd5e9",
		autoplay: true,
		barRadius: 10,
		dragToSeek: true,
		normalize: true,
		minPxPerSec: 20,
		mediaControls: waveform_options.show_controls
	};

	const container = true;

	function handle_change(): void {
		gradio.dispatch("change");
		if (!value_is_output) {
			gradio.dispatch("input");
		}
	}

	async function handle_keypress(e: KeyboardEvent): Promise<void> {
		await tick();
		if (e.key === "Enter") {
			e.preventDefault();
			gradio.dispatch("submit");
		}
	}

	$: if (value === null) value = "";

	// When the value changes, dispatch the change event via handle_change()
	// See the docs for an explanation: https://svelte.dev/docs/svelte-components#script-3-$-marks-a-statement-as-reactive
	$: value, handle_change();
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
	<AudioGraph graph_data={value.graph_data}/>
	{#if value.audio !== null}
		<BasePlayer
			{value}
			{label}
			i18n={gradio.i18n}
			{waveform_settings}
			{waveform_options}
			on:pause
			on:play
			on:stop
		/>
	{:else}
		<Empty size="small">
			<Music />
		</Empty>
	{/if}
</Block>

<style>
	label {
		display: block;
		width: 100%;
	}

	input {
		display: block;
		position: relative;
		outline: none !important;
		box-shadow: var(--input-shadow);
		background: var(--input-background-fill);
		padding: var(--input-padding);
		width: 100%;
		color: var(--body-text-color);
		font-weight: var(--input-text-weight);
		font-size: var(--input-text-size);
		line-height: var(--line-sm);
		border: none;
	}
	.container > input {
		border: var(--input-border-width) solid var(--input-border-color);
		border-radius: var(--input-radius);
	}
	input:disabled {
		-webkit-text-fill-color: var(--body-text-color);
		-webkit-opacity: 1;
		opacity: 1;
	}

	input:focus {
		box-shadow: var(--input-shadow-focus);
		border-color: var(--input-border-color-focus);
	}

	input::placeholder {
		color: var(--input-placeholder-color);
	}
</style>
