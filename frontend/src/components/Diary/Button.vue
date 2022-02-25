<template>
    <button> {{msg ? `${msg}` : ""}}</button>
    <!-- <div>{{$attrs}}</div> -->
</template>

<script>
export default {
    name: "Button",
    props: ["msg"],
}
</script>