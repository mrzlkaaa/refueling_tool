<template>
    <button> {{msg ? `${msg} data` : "Add fields"}}</button>
    <!-- <div>{{$attrs}}</div> -->
</template>

<script>
export default {
    name: "Button",
    props: ["msg"],
}
</script>