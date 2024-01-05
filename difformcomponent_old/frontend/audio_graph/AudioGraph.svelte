<script lang="ts">
	import {
		onMount,
		afterUpdate,
		onDestroy,
		setContext,
	} from "svelte";
	import cytoscape from "cytoscape";

	export let graph_data: any | null;

	setContext("graphSharedState", {
		getCyInstance: () => cyInstance,
	});

	let refElement = null;
	let cyInstance = null;

	onMount(() => {
		console.log(graph_data);
		initializeGraph();
	});

	afterUpdate(() => {
		if (cyInstance && graph_data) {
			// Replace elements and restore positions
			//const positions = cyInstance.nodes().map((ele) => {
			//	return { id: ele.id(), pos: ele.position() };
			//});

			//cyInstance.remove("*");
			cyInstance.add(graph_data.elements);
			//positions.forEach((ele) => {
			//	cyInstance.$id(ele.id).position(ele.pos);
			//});

			// Apply layout if number of nodes has changed
			//cyInstance.nodes().length === positions.length || applyFcose();
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
			container: refElement
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
