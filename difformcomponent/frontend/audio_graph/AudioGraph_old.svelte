<script lang="ts">
	import { BlockLabel } from "@gradio/atoms";
	import { Music } from "@gradio/icons";

	import {
		onMount,
		afterUpdate,
		onDestroy,
		setContext,
		createEventDispatcher,
	} from "svelte";
	import cytoscape from "cytoscape";
	import fcose from "cytoscape-fcose";
	import cxtmenu from "cytoscape-cxtmenu";
	import expandCollapse from "cytoscape-expand-collapse";

	import defaultStyle from "./Style";
	import defaultLayout from "./Layout";
	import defaultOptions from "./Options";

	export let value: string | null;
	export let label: string;
	export let show_label = true;

	setContext("graphSharedState", {
		getCyInstance: () => cyInstance,
	});

	let refElement = null;
	let cyInstance = null;

	onMount(() => {
		console.log(value);
		cytoscape.use(fcose);
		cytoscape.use(cxtmenu);
		cytoscape.use(expandCollapse);
		initializeGraph();
	});

	afterUpdate(() => {
		if (cyInstance && value) {
			// Replace elements and restore positions
			const positions = cyInstance.nodes().map((ele) => {
				return { id: ele.id(), pos: ele.position() };
			});

			cyInstance.remove("*");
			cyInstance.add(value.elements);
			positions.forEach((ele) => {
				cyInstance.$id(ele.id).position(ele.pos);
			});

			// Apply layout if number of nodes has changed
			cyInstance.nodes().length === positions.length || applyFcose();
			/*
            // Expand and collapse setup
            cyInstance.$('node[type="batch"]').data('isExpanded', true);

            // Audio select listener
            cyInstance.$('node[type="audio"]').on('select', (event) => {
                setCurrentSample(event.target.data());
            });

            // Retrieve node names (keyed by node type)
            var nodeMap = {}
            cyInstance.nodes().forEach((ele) => {
                if (!nodeMap.hasOwnProperty(ele.data('type'))) {
                    nodeMap[ele.data('type')] = [];
                }
                nodeMap[ele.data('type')].push(ele.data('name'));
            });
            setNodeNames(nodeMap);

            // Create a list of existing tags sorted by frequency
            var tagCounts = {};
            cyInstance.elements().forEach((ele) => {
                if (ele.data('tags')) {
                    ele.data('tags').split(',').forEach((tag) => {
                        if (tagCounts[tag]) {
                            tagCounts[tag] += 1;
                        } else {
                            tagCounts[tag] = 1;
                        }
                    })
                }
            })
            var tagListTemp = Object.entries(tagCounts).map(([tag, count]) => ({
                tag,
                count
            }));
            tagListTemp.sort((a, b) => b.count - a.count);
            setTagList(tagListTemp);

            // Signal active tool to update
            if (toolParams) {
                const nodeData = cyInstance.$id(toolParams.nodeData.id).json().data;
                setToolParams({ nodeData });
            };
			*/

			/*
            cy.nodes().on('mouseover', (event) => {
                cytoscapePopperRef.current = event.target.popper({
                    content: createContentFromComponent(<ReactButton />),
                    popper: {
                        placement: 'right',
                        removeOnDestroy: true,
                    },
                });
            });

            cy.nodes().on('mouseout', () => {
                if (cytoscapePopperRef) {
                    cytoscapePopperRef.current.destroy();
                }
            });
            */
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
						applyFcose(false);
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

	function applyFcose(randomize = false) {
		// Workaround tiling issues by temporarily removing audio source edges
		var audioSourceEdges = cyInstance.edges('[type="audio_source"]').remove();

		// Create and run layout
		var layout = cyInstance.layout({
			...defaultLayout,
			randomize,
			tilingCompareBy: (nodeId1, nodeId2) => {
				if (
					cyInstance.$id(nodeId1).data("type") === "audio" &&
					cyInstance.$id(nodeId2).data("type") === "audio"
				) {
					return (
						cyInstance.$id(nodeId1).data("batch_index") -
						cyInstance.$id(nodeId2).data("batch_index")
					);
				}
				return 0;
			},
		});
		layout.run();

		// Restore removed elements
		audioSourceEdges.restore();
	}
</script>

<BlockLabel {show_label} Icon={Music} label={label || "KGUI"} />

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
