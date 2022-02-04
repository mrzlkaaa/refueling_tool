<template>
     <button type="button" class="btn btn-primary" :style="width ? {width:width}:'width:50%'">{{text}}</button>
</template>

<script>
export default {
    name: "Button",
    props: ["text", "width"],
}
</script>
<style>
</style>