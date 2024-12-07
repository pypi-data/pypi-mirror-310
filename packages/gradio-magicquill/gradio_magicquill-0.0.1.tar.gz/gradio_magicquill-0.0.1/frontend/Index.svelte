<svelte:options accessors={true} />

<script lang="ts">
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import { onMount } from "svelte";
	import { embedMagicQuill } from "./lib/magicquill.es.js";

	export let value = {
		from_frontend: {
			img: null,
			original_image: null,
			add_edge_image: null,
			remove_edge_image: null,
			add_color_image: null,
			total_mask: null,
		},
		from_backend: {
			prompt: null,
			generated_image: null,
		},
	};

	export let loading_status: LoadingStatus | undefined = undefined;

	let generatedImageCache = null;

	export let theme: string | undefined = "system";
	export let url: string | undefined = undefined;

	let el: HTMLDivElement;
	let magicQuillObjID;

	function handle_change(): void {
		if (value["from_backend"] !== undefined) {
			if (
				value["from_backend"]["generated_image"] !== null &&
				value["from_backend"]["generated_image"] !== generatedImageCache
			) {
				if (window.updateGeneratedImg && window.updateGeneratedImg[magicQuillObjID]) {
					const updateGeneratedImg = window.updateGeneratedImg[magicQuillObjID];
					updateGeneratedImg(value["from_backend"]["generated_image"]);
					generatedImageCache =
						value["from_backend"]["generated_image"];
				}
			}
		}
	}

	$: if (value === null)
		value = {
			from_frontend: {
				img: null,
				original_image: null,
				add_edge_image: null,
				remove_edge_image: null,
				add_color_image: null,
				total_mask: null,
			},
			from_backend: {
				prompt: null,
				generated_image: null,
			},
		};

	$: value, handle_change();

	const blobToBase64 = (blob) => {
		return new Promise((resolve, _) => {
			const reader = new FileReader();
			reader.onloadend = () => resolve(reader.result);
			reader.readAsDataURL(blob);
		});
	};

	const changeDimensionCallBack = (e) => console.log(e);
	const uploadImgCallBack = async (e) => {
		const base64 = await blobToBase64(e);
		value.from_frontend.img = base64;
	};
	const uploadOriginalImgCallBack = async (e) => {
		const base64 = await blobToBase64(e);
		value.from_frontend.original_image = base64;
	};
	const uploadAddEdgeMaskCallBack = async (e) => {
		const base64 = await blobToBase64(e);
		value.from_frontend.add_edge_image = base64;
	};
	const uploadRemoveEdgeMaskCallBack = async (e) => {
		const base64 = await blobToBase64(e);
		value.from_frontend.remove_edge_image = base64;
	};
	const uploadColoredImgCallBack = async (e) => {
		const base64 = await blobToBase64(e);
		value.from_frontend.add_color_image = base64;
	};
	const uploadTotalMaskCallBack = async (e) => {
		const base64 = await blobToBase64(e);
		value.from_frontend.total_mask = base64;
	};
	const uploadBackgroundImgCallBack = async (e) => {
		const res = await fetch(`${url ? url : ""}/magic_quill/process_background_img`, {
			method: "POST",
			body: JSON.stringify(e),
			headers: {
				"content-type": "application/json",
			},
		}).then((res) => {
			return res.json();
		});
		return res;
	};

	const guessPromptCallBack = async (e) => {
		const res = await fetch(`${url ? url : ""}/magic_quill/guess_prompt`, {
			method: "POST",
			body: JSON.stringify(value.from_frontend),
			headers: {
				"content-type": "application/json",
			},
		}).then((res) => {
			return res.json();
		});
		value.from_backend.prompt = res;
		return {
			error: false,
			prompt: res,
		};
	};
	const updatePromptCallBack = (e) => {
		value.from_backend.prompt = e;
	};

	onMount(() => {
		magicQuillObjID = embedMagicQuill(el, {
			theme,
			changeDimensionCallBack,
			uploadImgCallBack,
			uploadOriginalImgCallBack,
			uploadAddEdgeMaskCallBack,
			uploadRemoveEdgeMaskCallBack,
			uploadColoredImgCallBack,
			uploadTotalMaskCallBack,
			uploadBackgroundImgCallBack,
			guessPromptCallBack,
			updatePromptCallBack,
		});
	});
</script>

<Block>
	{#if loading_status}
		<StatusTracker
			i18n=""
			autoscroll={true}
			translucent={true}
			{...loading_status}
		/>
	{/if}
	<div bind:this={el}></div>
</Block>

<style>
</style>
