<script lang="ts">
	import {
		onMount,
		afterUpdate,
		onDestroy,
		setContext,
	} from "svelte";
	import cytoscape from "cytoscape";
    import fcose from "cytoscape-fcose";
    import cxtmenu from "cytoscape-cxtmenu";
	import expandCollapse from "cytoscape-expand-collapse";


    import defaultStyle from "./style";
	import defaultLayout from "./layout";
	import defaultOptions from "./options";

	export let graph_data: any | null;

	setContext("graphSharedState", {
		getCyInstance: () => cyInstance,
	});

	let refElement = null;
	let cyInstance = null;

	onMount(() => {
		console.log(graph_data);
        cytoscape.use(fcose);
        cytoscape.use(cxtmenu);
		cytoscape.use(expandCollapse);
		initializeGraph();
	});

	afterUpdate(() => {
		if (cyInstance && graph_data) {
			cyInstance.add(graph_data.elements);
		}
	});

	onDestroy(() => {
		if (cyInstance) {
			cyInstance.destroy();
		}
	});

	function initializeGraph() {
		cyInstance = cytoscape({
			container: refElement,
            style: defaultStyle,
		});

        //cy.expandCollapse(defaultOptions);
		var expCol = cyInstance.expandCollapse("get");

		// ----------------------------
		//  Context menu configuration
		// ----------------------------

		// Core component
		cyInstance.cxtmenu({
			selector: "core",
			commands: [
				{
					content: "Tidy",
					select: function () {
						//applyFcose(false);
					},
				},
				{
					content: "Import model",
					select: function () {
						//setActiveTool('importModel');
					},
				},
				{
					content: "Add external source",
					select: function () {
						//setActiveTool('externalSource');
					},
				},
			],
		});
		const elementCommands = [
			{
				content: "Details",
				select: function (ele) {
					//setActiveTool('details');

					const nodeData = ele.json().data;
					console.log(nodeData);
					//setToolParams({ nodeData });
				},
			},
		];

		// Model nodes
		cyInstance.cxtmenu({
			selector: 'node[type="model"]',
			commands: [
				...elementCommands,
				{
					content: "Generate",
					select: function (ele) {
						//setActiveTool('generation');

						const nodeData = ele.json().data;
						//setToolParams({ nodeData });
					},
				},
			],
		});

		// Batch nodes
		const batchCommands = [
			{
				content: "Label",
				select: function (ele) {
					//setActiveTool('batchUpdateAttributes');

					const nodeData = ele.json().data;
					//setToolParams({ nodeData });
				},
			},
		];
		cyInstance.cxtmenu({
			selector: 'node[type="batch"][?isExpanded]',
			commands: [
				...elementCommands,
				...batchCommands,
				{
					content: "Collapse",
					select: function (ele) {
						expCol.collapse(ele);
						ele.data("isExpanded", false);
					},
				},
			],
		});
		cyInstance.cxtmenu({
			selector: 'node[type="batch"][!isExpanded]',
			commands: [
				...elementCommands,
				...batchCommands,
				{
					content: "Expand",
					select: function (ele) {
						expCol.expand(ele);
						ele.data("isExpanded", true);
					},
				},
			],
		});

		// Audio nodes
		cyInstance.cxtmenu({
			selector: 'node[type="audio"]',
			commands: [
				...elementCommands,
				{
					content: "Label",
					select: function (ele) {
						//setActiveTool('updateAttributes');

						const nodeData = ele.json().data;
						//setToolParams({ nodeData });
					},
				},
				{
					content: "Variation",
					select: function (ele) {
						//setActiveTool('variation');

						const nodeData = ele.json().data;
						//setToolParams({ nodeData });
					},
				},
				{
					content: "Export",
					select: function (ele) {
						//setActiveTool('exportSingle');

						const nodeData = ele.json().data;
						//setToolParams({ nodeData });
					},
				},
			],
		});

		// Edges
		cyInstance.cxtmenu({
			selector: "edge",
			commands: [...elementCommands],
		});

		// Model nodes
		cyInstance.cxtmenu({
			selector: 'node[type="model"]',
			commands: [
				...elementCommands,
				{
					content: "Generate",
					select: function (ele) {
						//setActiveTool('generation');

						const nodeData = ele.json().data;
						//setToolParams({ nodeData });
					},
				},
			],
		});

		// External source nodes
		cyInstance.cxtmenu({
			selector: 'node[type="external"]',
			commands: [
				...elementCommands,
				{
					content: "Rescan",
					select: function (ele) {
						//setActiveTool('rescanSource');

						const nodeData = ele.json().data;
						//setToolParams({ nodeData });
					},
				},
			],
		});
	}
</script>

<div class="graph" bind:this={refElement}>
	{#if cyInstance}
		<slot />
	{/if}
</div>

<style>
	.graph {
		width: var(--size-full);
		height: 400px;
	}
</style>
