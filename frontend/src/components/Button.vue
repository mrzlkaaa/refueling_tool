<template>
     <button type="button" :class='"btn " + cls' :style="width ? {width:width}:'width:50%'" :disabled="dis">{{text}}</button>
</template>

<script>
export default {
    name: "Button",
    props: ["dis", "cls", "text", "width"],
}
</script>
<style>
</style>