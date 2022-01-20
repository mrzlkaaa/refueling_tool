<template>
    <button class="btn btn-primary"> {{msg ? `${msg} data` : "Add fields"}}</button>
</template>

<script>
export default {
    name: "Button",
    props: ["msg"],
}
</script>