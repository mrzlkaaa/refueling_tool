<template>
    <input type="text" :class="[cls ? cls : 'form-control']">
</template>

<script>
export default {
    name: "Input",
    props: {
        cls: String,
    }
}
</script>